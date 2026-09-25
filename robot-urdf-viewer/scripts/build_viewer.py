#!/usr/bin/env python3
"""Build an offline, simplified robot viewer from expanded URDF (stdlib only)."""

import argparse
import base64
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import xml.etree.ElementTree as ET


def numbers(text, count):
    values = [float(x) for x in text.split()]
    if len(values) != count or not all(math.isfinite(x) for x in values):
        raise ValueError(f"Expected {count} finite numbers: {text!r}")
    return values


def scalar(text):
    return numbers(text, 1)[0]


def name(text):
    if not text or not re.fullmatch(r"[\w./:\-]+", text):
        raise ValueError(f"Invalid link/joint identifier: {text!r}")
    return text


def origin(element):
    item = element.find("origin")
    return {
        key: numbers(item.get(key, "0 0 0") if item is not None else "0 0 0", 3)
        for key in ("xyz", "rpy")
    }


def resolve_mesh(uri, source, packages):
    if uri.startswith("package://"):
        package, sep, relative = uri[10:].partition("/")
        if not sep:
            raise ValueError(f"Invalid mesh URI: {uri}")
        if package in packages:
            return packages[package] / relative
        for prefix in os.environ.get("AMENT_PREFIX_PATH", "").split(os.pathsep):
            if prefix:
                candidate = Path(prefix) / "share" / package / relative
                if candidate.is_file():
                    return candidate
        for ancestor in source.parents:
            for candidate in (ancestor / relative if ancestor.name == package else None,
                              ancestor / package / relative,
                              ancestor / "src" / package / relative):
                if candidate is not None and candidate.is_file():
                    return candidate
        raise ValueError(f"Cannot resolve {uri}; supply --package {package}=/path/to/{package}")
    if uri.startswith("file://"):
        return Path(uri[7:])
    if "://" in uri:
        raise ValueError(f"Only local mesh files are supported: {uri}")
    path = Path(uri)
    return path if path.is_absolute() else source.parent / path


def mesh_vertices(path):
    """Read local STL triangles or OBJ vertices without external dependencies."""
    data = path.read_bytes()
    vertices = []
    if path.suffix.lower() == ".stl":
        count = struct.unpack_from("<I", data, 80)[0] if len(data) >= 84 else 0
        if len(data) == 84 + count * 50:
            for offset in range(84, len(data), 50):
                vertices.extend(struct.unpack_from("<3f", data, offset + 12 + i * 12) for i in range(3))
        else:
            for line in data.decode("ascii").splitlines():
                fields = line.split()
                if fields and fields[0] == "vertex":
                    vertices.append(numbers(" ".join(fields[1:]), 3))
    elif path.suffix.lower() == ".obj":
        for line in data.decode("utf-8").splitlines():
            fields = line.split()
            if fields and fields[0] == "v":
                vertices.append(numbers(" ".join(fields[1:4]), 3))
    else:
        raise ValueError(f"Unsupported mesh format {path.suffix}; bounding boxes support STL and OBJ")
    if not vertices or not all(math.isfinite(v) for p in vertices for v in p):
        raise ValueError(f"No finite mesh vertices in {path.name}")
    if path.suffix.lower() == ".stl" and len(vertices) % 3:
        raise ValueError(f"Incomplete STL triangle in {path.name}")
    return vertices


def vertex_bounds(vertices, scale):
    """Keep mesh bounds in visual coordinates, before the URDF visual origin."""
    lo = [min(p[i] * scale[i] for p in vertices) for i in range(3)]
    hi = [max(p[i] * scale[i] for p in vertices) for i in range(3)]
    return {"box": [max(b - a, 1e-6) for a, b in zip(lo, hi)],
            "center": [(a + b) / 2 for a, b in zip(lo, hi)]}


def mesh_bounds(path, scale):
    return vertex_bounds(mesh_vertices(path), scale)


def mesh_visual(path, scale):
    """Embed both block bounds and actual STL triangles for an offline switch."""
    vertices = mesh_vertices(path)
    result = vertex_bounds(vertices, scale)
    if path.suffix.lower() == ".stl":
        payload = bytearray()
        # Reverse winding for a reflected scale so exterior faces remain exterior.
        order = (0, 2, 1) if math.prod(scale) < 0 else (0, 1, 2)
        for start in range(0, len(vertices), 3):
            for offset in order:
                point = vertices[start + offset]
                payload.extend(struct.pack("<3f", *(point[i] * scale[i] for i in range(3))))
        result["stl"] = base64.b64encode(payload).decode("ascii")
    return result


# Split known merged triangle ranges into independently selectable source parts.
def assign_parts(data, entries, link):
    # Preserve the legacy filename-only format as non-selectable provenance.
    if all(isinstance(entry, str) and entry.lower().endswith('.stl') for entry in entries):
        # Keep original names without inventing their geometry membership.
        data['sourceStls'] = entries
        # Finish when no verified triangle mapping was supplied.
        return
    # Require explicit geometry membership for each selectable source part.
    if not all(isinstance(entry, dict) and isinstance(entry.get('file'), str)
               and entry['file'].lower().endswith('.stl') for entry in entries):
        # Reject ambiguous mixtures of names and range specifications.
        raise ValueError(f'Invalid mesh sources for link: {link}')
    # Group source parts by their zero-based URDF mesh reference index.
    groups = {}
    # Validate all ranges before modifying the link geometry.
    for index, entry in enumerate(entries):
        # Read the source mesh and its contiguous triangle interval.
        mesh, start, count = (entry.get(key) for key in ('mesh', 'start', 'count'))
        # Require nonnegative indices and nonempty integer triangle counts.
        if any(type(value) is not int for value in (mesh, start, count)) or mesh < 0 or start < 0 or count <= 0:
            # Identify the invalid source-part mapping.
            raise ValueError(f'{link}: invalid triangle range for {entry["file"]}')
        # Retain the source list index to identify repeated filenames separately.
        groups.setdefault(mesh, []).append((start, count, index))
    # Map each mesh reference to its supported visual geometry.
    visuals = {block['meshIndex']: block for block in data['blocks'] if 'meshIndex' in block}
    # Collect validated replacement blocks by their mesh reference.
    replacements = {}
    # Split only visuals with an explicit, complete source-part mapping.
    for mesh, ranges in groups.items():
        # Require actual embedded STL geometry for selectable parts.
        if mesh not in visuals or 'stl' not in visuals[mesh]:
            # Refuse to imply geometry membership for unavailable meshes.
            raise ValueError(f'{link}: source parts require an available STL mesh {mesh}')
        # Decode the already scaled URDF geometry without rereading private assets.
        payload = base64.b64decode(visuals[mesh]['stl'])
        # Start at the first triangle to detect gaps or overlapping ranges.
        cursor = 0
        # Prepare individual blocks for this visual.
        replacements[mesh] = []
        # Follow geometry order independently of the source list's presentation order.
        for start, count, index in sorted(ranges):
            # Require an exact partition with no out-of-bounds triangle ranges.
            if start != cursor or (start + count) * 36 > len(payload):
                # Reject mappings that would hide or duplicate robot triangles.
                raise ValueError(f'{link}: source triangle ranges must partition mesh {mesh}')
            # Retain the original triangle coordinates, winding, and detail.
            part = payload[start * 36:(start + count) * 36]
            # Preserve the URDF visual origin and material for each constituent.
            block = dict(visuals[mesh])
            # Compute a separate block bound around the selected source part.
            block.update(vertex_bounds(list(struct.iter_unpack('<3f', part)), [1, 1, 1]))
            # Embed the source part without duplicating the merged geometry.
            block.update(stl=base64.b64encode(part).decode('ascii'), sourcePart=index)
            # Keep the constituent in its original visual's position in the model.
            replacements[mesh].append(block)
            # Advance to the end of the verified triangle interval.
            cursor = start + count
        # Require every original triangle to survive the split.
        if cursor * 36 != len(payload):
            # Reject incomplete mappings instead of losing geometry silently.
            raise ValueError(f'{link}: source triangle ranges must cover mesh {mesh}')
    # Retain unmapped primitives and visuals unchanged.
    data['blocks'] = [part for block in data['blocks'] for part in replacements.get(block.get('meshIndex'), [block])]
    # Store human-readable source names in their requested display order.
    data['sourceStls'] = [entry['file'] for entry in entries]


def convert(source, packages=None, tip=None, tip_at=None, strict_meshes=False, mesh_sources=None):
    source = Path(source).resolve()
    robot = ET.parse(source).getroot()
    if robot.tag != "robot":
        raise ValueError("Input must have a <robot> root")
    if any("xacro" in e.tag for e in robot.iter()) or "${" in ET.tostring(robot, encoding="unicode"):
        raise ValueError("Expand Xacro first: xacro robot.urdf.xacro -o /tmp/robot.urdf")
    model = {"name": robot.get("name", source.stem), "source": {"kind": "urdf", "file": source.name},
             "links": {}, "joints": [], "warnings": []}
    materials = {}
    for material in robot.findall("material"):
        color = material.find("color")
        if color is not None:
            materials[material.get("name")] = numbers(color.get("rgba", "0.6 0.6 0.6 1"), 4)[:3]
    for link in robot.findall("link"):
        key = name(link.get("name"))
        if key in model["links"]:
            raise ValueError(f"Duplicate link: {key}")
        blocks = []
        # Retain mesh references even when their geometry cannot be displayed.
        meshes = []
        for visual in link.findall("visual"):
            geometry = visual.find("geometry")
            if geometry is None or len(geometry) != 1:
                raise ValueError(f"{key}: visual needs one geometry")
            shape = geometry[0]
            pose = origin(visual)
            block = {"at": pose["xyz"], "rpy": pose["rpy"]}
            if shape.tag == "box":
                block["box"] = numbers(shape.get("size", ""), 3)
            elif shape.tag == "cylinder":
                block["cyl"] = [scalar(shape.get("radius", "")), scalar(shape.get("length", ""))]
            elif shape.tag == "sphere":
                block["sphere"] = scalar(shape.get("radius", ""))
            elif shape.tag == "mesh":
                # Preserve the URDF filename separately from resolved local paths.
                reference = {"file": shape.get("filename", ""), "status": "omitted"}
                # Associate each visual mesh with its owning link.
                meshes.append(reference)
                # Associate rendered geometry with its original URDF mesh reference.
                block['meshIndex'] = len(meshes) - 1
                try:
                    mesh = resolve_mesh(shape.get("filename", ""), source, packages or {})
                    block.update(mesh_visual(mesh, numbers(shape.get("scale", "1 1 1"), 3)))
                    # Distinguish embedded triangles from bounding-box approximations.
                    reference["status"] = "STL" if "stl" in block else "bounding box"
                    if mesh.suffix.lower() == ".obj":
                        model["warnings"].append(f"{key}: OBJ visual remains a bounding box in STL mode.")
                except (OSError, ValueError, UnicodeError, struct.error) as exc:
                    if strict_meshes:
                        raise ValueError(f"{key}: {exc}") from exc
                    model["warnings"].append(f"{key}: mesh omitted. {exc}")
                    continue
            else:
                raise ValueError(f"{key}: unsupported geometry {shape.tag}")
            dimensions = block.get("box", block.get("cyl", [block.get("sphere", 1)]))
            if any(d <= 0 for d in dimensions):
                raise ValueError(f"{key}: geometry dimensions must be positive")
            material = visual.find("material")
            if material is not None:
                color = material.find("color")
                rgb = (numbers(color.get("rgba", ""), 4)[:3] if color is not None
                       else materials.get(material.get("name")))
                if rgb is not None:
                    block["color"] = rgb
            blocks.append(block)
        # Keep the file inventory independent of the current geometry mode.
        model["links"][key] = {"blocks": blocks, "meshes": meshes}
        if not blocks:
            model["warnings"].append(f"{key}: no usable visual; showing a frame connector.")
    if not model["links"]:
        raise ValueError("Robot has no links")
    # Accept explicit constituent filenames for meshes assembled from multiple parts.
    if mesh_sources is not None:
        # Require a link-to-filenames mapping instead of guessing assembly membership.
        if not isinstance(mesh_sources, dict):
            # Explain the supported provenance format.
            raise ValueError("Mesh sources must map link names to lists of STL filenames")
        # Validate each supplied association against the actual robot links.
        for link, files in mesh_sources.items():
            # Reject misspelled links and malformed filename lists.
            if link not in model["links"] or not isinstance(files, list) or not files:
                # Identify the association that cannot be used.
                raise ValueError(f"Invalid mesh sources for link: {link}")
            # Preserve component instances and their original filenames in order.
            assign_parts(model["links"][link], files, link)
    by_name, parents, children = {}, {}, {}
    for item in robot.findall("joint"):
        key, kind = name(item.get("name")), item.get("type")
        if key in by_name:
            raise ValueError(f"Duplicate joint: {key}")
        if kind not in {"fixed", "revolute", "continuous", "prismatic"}:
            raise ValueError(f"{key}: unsupported joint type {kind}; use fixed, revolute, continuous or prismatic")
        if item.find("parent") is None or item.find("child") is None:
            raise ValueError(f"{key}: missing parent or child")
        parent, child = name(item.find("parent").get("link")), name(item.find("child").get("link"))
        if parent not in model["links"] or child not in model["links"]:
            raise ValueError(f"{key}: parent or child is not a declared link")
        if child in parents:
            raise ValueError(f"{child}: multiple parent joints")
        parents[child] = parent
        children.setdefault(parent, []).append(child)
        joint = dict(name=key, type=kind, parent=parent, child=child, **origin(item))
        if kind != "fixed":
            axis = item.find("axis")
            joint["axis"] = numbers(axis.get("xyz", "1 0 0") if axis is not None else "1 0 0", 3)
            if math.hypot(*joint["axis"]) == 0:
                raise ValueError(f"{key}: axis must be nonzero")
            limit = item.find("limit")
            if kind == "continuous":
                joint.update(lower=-math.pi, upper=math.pi)
            else:
                if limit is None or any(k not in limit.attrib for k in ("lower", "upper")):
                    raise ValueError(f"{key}: explicit lower and upper limits are required")
                joint.update({k: scalar(limit.get(k)) for k in ("lower", "upper")})
                if joint["lower"] > joint["upper"]:
                    raise ValueError(f"{key}: lower limit exceeds upper limit")
            if limit is not None:
                for field in ("velocity", "effort"):
                    if field in limit.attrib:
                        joint[field] = scalar(limit.get(field))
            mimic = item.find("mimic")
            if mimic is not None:
                joint["mimic"] = {"joint": name(mimic.get("joint")),
                                  "multiplier": scalar(mimic.get("multiplier", "1")),
                                  "offset": scalar(mimic.get("offset", "0"))}
        by_name[key] = joint
        model["joints"].append(joint)
    roots = set(model["links"]) - set(parents)
    if len(roots) != 1:
        raise ValueError("URDF must form one connected tree with one root")
    model["root"] = roots.pop()
    queue, visited, depths = [model["root"]], set(), {model["root"]: 0}
    while queue:
        link = queue.pop()
        if link in visited:
            raise ValueError("Cycle in link tree")
        visited.add(link)
        for child in children.get(link, []):
            depths[child] = depths[link] + 1
            queue.append(child)
    if visited != set(model["links"]):
        raise ValueError("Disconnected links or a cycle in the URDF")
    for joint in model["joints"]:
        current, seen = joint, set()
        while "mimic" in current:
            if current["name"] in seen:
                raise ValueError(f"{joint['name']}: cyclic mimic relationship")
            seen.add(current["name"])
            target = current["mimic"]["joint"]
            if target not in by_name or by_name[target]["type"] == "fixed":
                raise ValueError(f"{joint['name']}: missing or fixed mimic source {target}")
            current = by_name[target]
    if tip is not None and tip not in model["links"]:
        raise ValueError(f"Unknown tip link: {tip}")
    chosen = tip or max(depths, key=depths.get)
    model["tip"] = {"link": chosen, "at": tip_at or [0, 0, 0]}
    if tip is None:
        model["warnings"].append(f"Tip marker uses {chosen}'s origin; set --tip and --tip-at to override.")
    return model


def render(model, output):
    template = Path(__file__).resolve().parents[1] / "assets" / "viewer.html"
    encoded = json.dumps(model, ensure_ascii=True, allow_nan=False, separators=(",", ":"))
    # Prevent URDF strings from terminating the JSON script element.
    encoded = encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = template.read_text().replace("__ROBOT_MODEL__", encoded)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urdf", type=Path, help="Expanded URDF file")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--package", action="append", default=[], metavar="NAME=PATH")
    parser.add_argument("--tip", help="Link for the tip marker and optional trail")
    parser.add_argument("--tip-at", nargs=3, type=float, default=[0, 0, 0], metavar=("X", "Y", "Z"))
    parser.add_argument("--strict-meshes", action="store_true", help="Fail instead of omitting unresolved/unsupported meshes")
    # Allow callers to document the source parts of merged link meshes.
    parser.add_argument("--mesh-sources", type=Path, help="JSON mapping link names to constituent STL filenames")
    args = parser.parse_args()
    try:
        if args.output.resolve() == args.urdf.resolve():
            raise ValueError("Output must differ from the source URDF")
        packages = {}
        for mapping in args.package:
            key, sep, value = mapping.partition("=")
            if not sep or not key or not value:
                raise ValueError("--package must be NAME=PATH")
            packages[key] = Path(value).expanduser().resolve()
        if not all(math.isfinite(v) for v in args.tip_at):
            raise ValueError("Tip coordinates must be finite")
        # Load optional provenance without adding a YAML dependency to the converter.
        mesh_sources = json.loads(args.mesh_sources.read_text()) if args.mesh_sources else None
        # Include the supplied source associations in the offline model.
        model = convert(args.urdf, packages, args.tip, args.tip_at, args.strict_meshes, mesh_sources)
        render(model, args.output)
    except (OSError, ValueError, ET.ParseError) as exc:
        parser.exit(2, f"error: {exc}\n")
    for warning in model["warnings"]:
        print(f"note: {warning}", file=sys.stderr)
    print(f"Built {args.output} ({len(model['links'])} links, {len(model['joints'])} joints)")


if __name__ == "__main__":
    main()
