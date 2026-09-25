---
name: robot-urdf-viewer
description: Generate a standalone, offline HTML robot viewer from URDF or Xacro, with switchable block/STL geometry, joint controls, frame explanations, and link-to-STL associations. Use for inspecting robot structure and forward kinematics; excludes IK, physics simulation, and hardware control.
---

# Robot URDF Viewer

Build with the bundled converter and template. Preserve three tabs: **Motion** for manual sliders, **Joints** for joint selection and the transform walkthrough, and **Link STLs** for the STL files that make up each link. Keep technical details collapsed. Do not include Play/Pause, automatic joint sweeps, playback speed, or automatic frame walkthroughs; use manual Previous/Next steps. Start with **Block CAD** selected; provide a **Geometry** selector for switching to **STL models** without changing the pose or camera.

Selected links must stand out with a strong color, outline, and visible selection label. In **Motion** and **Joints**, make only the selected joint's immediate parent and child links opaque; keep every other link translucent, including descendants. Show the parent in blue and child in magenta. In **Link STLs**, provide clickable link headings and individual STL buttons, with matching viewport picking and selected button states. Selecting a part highlights only that source instance, fades the rest, and switches to exact STL geometry. Geometry switching must preserve selection and pose.

## Generate

1. Locate the requested URDF and mesh packages. Expand Xacro using the project's ROS environment and required arguments first; never guess unresolved substitutions.
2. Preserve each link’s URDF mesh filenames. For merged meshes, find the project’s authoritative part-to-link mapping and pass its constituent STL filenames using `--mesh-sources`; do not infer membership from names or geometry. Show original parts separately from merged URDF exports. For individual selection within merged STLs, supply verified triangle ranges for each source instance; use the assembly export order and verify the geometry, never guess ranges. The converter splits these ranges without changing triangles or visual origins. If source membership is unavailable, show direct URDF references only; filename-only provenance must clearly indicate that individual geometry is unavailable. Include links without STL files and report omitted meshes. See [input-support.md](references/input-support.md) for the JSON format.
3. Choose the tip link from the request or robot structure. For multiple tools, use the requested tool; if unspecified, disclose the converter's deepest-link default. The tip affects only the marker, coordinates, and trail.
4. Export every viewer HTML generated for the user, including rebuilds and variants, to the Windows OneDrive Documents folder `robot_urdf_viewers`. This is the standing destination for all future runs of this skill. Create that folder if needed. Use a descriptive filename such as `<robot-name>-viewer.html`.

   - Windows: `C:\Users\grsga\OneDrive\Documents\robot_urdf_viewers`
   - WSL: `/mnt/c/Users/grsga/OneDrive/Documents/robot_urdf_viewers`

   The user explicitly authorizes this OneDrive destination for viewer HTML containing embedded private CAD/STL geometry, including Arctos. Keep source assets and intermediate mesh exports local and Git-excluded, but do not substitute `cad/`, `/tmp`, or a WSL-only path for the delivered HTML. If destination access requires filesystem approval, request that access instead of changing the destination. Open and link the OneDrive copy. Run from this skill's directory:

   ```bash
   python3 scripts/build_viewer.py /path/to/robot.urdf \
     -o /mnt/c/Users/grsga/OneDrive/Documents/robot_urdf_viewers/robot-viewer.html \
     --package robot_description=/path/to/robot_description --tip tool_link
   ```

   Omit optional flags when unnecessary. Add `--tip-at X Y Z` for a point expressed in the tip link's frame. See [input-support.md](references/input-support.md) for mesh resolution and supported inputs.

5. Inspect reported model notes. Resolve missing packages when available. Do not silently substitute joint types, invent limits, or describe bounding boxes as exact meshes.
6. Open the completed HTML from its saved destination in a visible **Google Chrome** window after each successful build, unless the user asks not to open it. Launch Chrome explicitly with the local file path or file URI; do not rely on the default browser. Under WSL, use Windows Chrome with a Windows-accessible path (convert with `wslpath -w`). If Chrome is unavailable, report that and provide the file link without installing a browser automatically.
7. Verify the controls below. Return a link to the HTML and identify material geometry approximations or unavailable browser validation. A headless validation run does not replace opening the viewer for the user.

## Constraints

- Reuse `assets/viewer.html`; it embeds Three.js and its MIT notice. Generated viewers need no server, network, ROS runtime, or build system.
- Embed actual STL triangles alongside their block bounds, preserving mesh scale and visual origins. STL mode retains primitives and uses block fallbacks for unsupported actual mesh formats. Disable the STL option if no STL visuals exist. Do not discard triangle detail or fetch mesh files at runtime.
- Preserve URDF origins, axes, limits, and mimic equations. Keep meters and radians internally; angle controls display degrees.
- No IK, workspace solver, collisions, dynamics, or robot commands. Motion is illustrative forward kinematics.
- The user explicitly authorizes completed HTML viewers, including embedded private CAD/STL geometry, in the personal OneDrive destination above. Keep source CAD/STL files and intermediate exports local and Git-excluded. This authorization does not permit publishing private assets to GitHub, bundling them in this skill, or uploading them to other services for testing.
- Do not edit the source URDF to make a visualization work. Report unsupported inputs or ask for a required model choice.

## Verify

Run `python3 scripts/test_builder.py` after changing the converter or template.

For a generated viewer, check in a browser:

| Check | Expected |
| --- | --- |
| Load with network blocked | Robot renders; no page errors |
| Geometry selector | Starts on Block CAD; STL models show actual triangles; switching back restores blocks |
| Geometry switch in all three tabs | Pose, camera, selection, transparency, and frame controls remain intact |
| Link STLs tab | Every link appears; constituent filenames match the supplied mapping; merged URDF references are separate; missing meshes and no-STL links are explicit |
| Slider and Home | Child subtree moves; limits and mimic relationships hold |
| Joints tab | Joint names and connected links are clear; only the immediate parent and child are opaque |
| Link and part selection | List and viewport clicks agree; selected geometry is magenta and opaque; others are translucent; repeated filenames remain distinct |
| Manual frame steps | Previous/Next changes the explanation without changing joint values; no playback controls |
| Fit view, orbit, zoom, narrow screen | Robot and controls remain usable |
| Fixed-only model | Renders without movable joint sliders |

`window.robotViewer` exposes model data, joint values, scene links, frame selection, and the tip position for numerical checks. It has no IK methods. Use synthetic/public fixtures for reusable tests.
