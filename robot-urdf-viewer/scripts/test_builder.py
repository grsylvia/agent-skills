#!/usr/bin/env python3
"""Synthetic tests for URDF semantics, mesh bounds, and offline output."""
import base64
import json
import math
from pathlib import Path
import re
import struct
import tempfile
import unittest
from build_viewer import convert, mesh_bounds, mesh_visual, render

ROBOT = '''<robot name="Test robot">
  <material name="orange"><color rgba="1 0.5 0 1"/></material>
  <link name="base"><visual><geometry><box size="0.4 0.4 0.1"/></geometry></visual></link>
  <link name="arm"><visual><origin xyz="0 0 0.5" rpy="0 0.2 0"/>
    <geometry><cylinder radius="0.04" length="1"/></geometry><material name="orange"/></visual></link>
  <link name="tool"><visual><geometry><sphere radius="0.08"/></geometry></visual></link>
  <link name="finger"/><link name="copy"/><link name="copy2"/>
  <joint name="shoulder" type="revolute"><parent link="base"/><child link="arm"/>
    <origin xyz="0 0 0.1" rpy="0 0 1.5707963267948966"/><axis xyz="0 1 0"/>
    <limit lower="-1" upper="1" velocity="0.4" effort="10"/></joint>
  <joint name="tool_mount" type="fixed"><parent link="arm"/><child link="tool"/><origin xyz="0 0 1"/></joint>
  <joint name="grip" type="prismatic"><parent link="tool"/><child link="finger"/>
    <axis xyz="1 0 0"/><limit lower="0" upper="0.1"/></joint>
  <joint name="follower" type="prismatic"><parent link="tool"/><child link="copy"/>
    <axis xyz="1 0 0"/><limit lower="-0.2" upper="0.1"/><mimic joint="grip" multiplier="-2" offset="0.01"/></joint>
  <joint name="follower2" type="prismatic"><parent link="tool"/><child link="copy2"/>
    <axis xyz="1 0 0"/><limit lower="-0.1" upper="0.1"/><mimic joint="follower" multiplier="0.5" offset="0.02"/></joint>
</robot>'''

class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / 'robot.urdf'

    def tearDown(self):
        self.temp.cleanup()

    def load(self, xml=ROBOT, **kwargs):
        self.source.write_text(xml)
        return convert(self.source, **kwargs)

    def test_transforms_limits_mimic_material(self):
        model = self.load(tip='tool', tip_at=[0, 0, 0.2])
        self.assertEqual(model['root'], 'base')
        joint = model['joints'][0]
        self.assertEqual(joint['axis'], [0, 1, 0])
        self.assertEqual(joint['xyz'], [0, 0, 0.1])
        self.assertAlmostEqual(joint['rpy'][2], math.pi / 2)
        self.assertEqual((joint['lower'], joint['upper']), (-1, 1))
        self.assertEqual(model['joints'][3]['mimic'], {'joint': 'grip', 'multiplier': -2, 'offset': 0.01})
        self.assertEqual(model['links']['arm']['blocks'][0]['color'], [1, 0.5, 0])
        self.assertEqual(model['tip'], {'link': 'tool', 'at': [0, 0, 0.2]})

    def test_fixed_only_and_continuous(self):
        self.assertEqual(self.load('<robot name="Fixed"><link name="base"/></robot>')['joints'], [])
        joint = self.load(ROBOT.replace('type="revolute"', 'type="continuous"'))['joints'][0]
        self.assertEqual(joint['lower'], -math.pi)
        self.assertEqual(joint['type'], 'continuous')

    def test_invalid_models(self):
        replacements = [('type="revolute"', 'type="floating"'), ('axis xyz="0 1 0"', 'axis xyz="0 0 0"'),
                        ('lower="-1"', 'lower="2"'), ('lower="-1"', 'lower="nan"'), ('lower="-1"', 'other="-1"'),
                        ('mimic joint="grip"', 'mimic joint="follower2"'), ('mimic joint="grip"', 'mimic joint="missing"'),
                        ('parent link="base"', 'parent link="finger"'), ('</robot>', '<link name="extra"/></robot>'),
                        ('</robot>', '<link name="base"/></robot>'), ('child link="arm"', 'child link="absent"')]
        for before, after in replacements:
            with self.subTest(after=after), self.assertRaises(ValueError):
                self.load(ROBOT.replace(before, after))

    def test_ascii_binary_and_obj_bounds(self):
        ascii_stl = self.root / 'part.stl'
        ascii_stl.write_text('solid test\nvertex 1 2 3\nvertex 3 4 5\nvertex 2 3 4\nendsolid test')
        obj = self.root / 'part.obj'
        obj.write_text('v 1 2 3\nv 3 4 5\nv 2 3 4\n')
        binary_stl = self.root / 'binary.stl'
        binary_stl.write_bytes(b'solid' + b' ' * 75 + struct.pack('<I12fH', 1, 0, 0, 1, 1, 2, 3, 3, 4, 5, 2, 3, 4, 0))
        for path in [ascii_stl, binary_stl, obj]:
            self.assertEqual(mesh_bounds(path, [2, -1, 0.5]), {'box': [4, 2, 1], 'center': [4, -3, 2]})

    def test_package_mesh_visual_origin(self):
        (self.root / 'part.obj').write_text('v 1 2 3\nv 3 4 5\n')
        xml = '''<robot name="Mesh"><link name="base"><visual><origin xyz="1 0 0" rpy="0 0 1.57"/>
          <geometry><mesh filename="package://test_pkg/part.obj" scale="2 1 1"/></geometry></visual></link></robot>'''
        block = self.load(xml, packages={'test_pkg': self.root}, strict_meshes=True)['links']['base']['blocks'][0]
        self.assertEqual(block['center'], [4, 3, 4])
        self.assertEqual(block['at'], [1, 0, 0])
        self.assertEqual(block['rpy'], [0, 0, 1.57])

    def test_stl_payload_scale_winding_and_origin(self):
        vertices = [(1, 2, 3), (3, 2, 3), (1, 4, 3)]
        ascii_stl = self.root / 'triangle.stl'
        ascii_stl.write_text('solid triangle\n' + '\n'.join('vertex ' + ' '.join(map(str, p)) for p in vertices) + '\nendsolid')
        binary_stl = self.root / 'binary.stl'
        binary_stl.write_bytes(b' ' * 80 + struct.pack('<I12fH', 1, 0, 0, 1, *[v for p in vertices for v in p], 0))
        for path in [ascii_stl, binary_stl]:
            visual = mesh_visual(path, [2, -1, 0.5])
            self.assertEqual(struct.unpack('<9f', base64.b64decode(visual['stl'])),
                             (2, -2, 1.5, 2, -4, 1.5, 6, -2, 1.5))
        xml = '''<robot name="STL"><link name="base"><visual><origin xyz="1 2 3" rpy="0 0 1.57"/>
          <geometry><mesh filename="triangle.stl" scale="0.5 0.5 0.5"/></geometry></visual></link></robot>'''
        block = self.load(xml, strict_meshes=True)['links']['base']['blocks'][0]
        self.assertEqual(block['at'], [1, 2, 3])
        self.assertEqual(block['rpy'], [0, 0, 1.57])
        self.assertEqual(struct.unpack('<9f', base64.b64decode(block['stl']))[:3], (0.5, 1, 1.5))
        output = self.root / 'embedded.html'
        render(self.load(xml), output)
        encoded = re.search(r'id="robot-model">(.*?)</script>', output.read_text(), re.S).group(1)
        self.assertEqual(json.loads(encoded)['links']['base']['blocks'][0]['stl'], block['stl'])

    def test_missing_mesh_reported_or_fails(self):
        xml = '<robot><link name="base"><visual><geometry><mesh filename="missing.dae"/></geometry></visual></link></robot>'
        self.assertIn('mesh omitted', ' '.join(self.load(xml)['warnings']))
        with self.assertRaises(ValueError):
            self.load(xml, strict_meshes=True)

    # Verify ownership and provenance survive conversion and offline serialization.
    def test_link_mesh_membership(self):
        # Provide a minimal local mesh used twice by one link.
        (self.root / 'part.stl').write_text('solid test\nvertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\nendsolid')
        # Include repeated visuals, an omitted mesh, and a primitive-only link.
        xml = '''<robot name="Parts"><link name="base">
          <visual><geometry><mesh filename="package://parts/part.stl"/></geometry></visual>
          <visual><geometry><mesh filename="package://parts/part.stl"/></geometry></visual>
          <visual><geometry><mesh filename="missing.stl"/></geometry></visual></link>
          <link name="tool"><visual><geometry><box size="1 1 1"/></geometry></visual></link>
          <joint name="mount" type="fixed"><parent link="base"/><child link="tool"/></joint></robot>'''
        # Include literal markup to exercise safe filename serialization.
        sources = {'base': ['left & right.stl', '</script><b>part.stl']}
        # Convert with both package resolution and explicit source membership.
        model = self.load(xml, packages={'parts': self.root}, mesh_sources=sources)
        # Verify every visual reference retains its owning link and status.
        self.assertEqual(model['links']['base']['meshes'], [
            {'file': 'package://parts/part.stl', 'status': 'STL'},
            {'file': 'package://parts/part.stl', 'status': 'STL'},
            {'file': 'missing.stl', 'status': 'omitted'}])
        # Verify primitive-only links do not acquire invented source membership.
        self.assertEqual(model['links']['tool']['meshes'], [])
        # Verify supplied constituents remain separate from merged visual references.
        self.assertEqual(model['links']['base']['sourceStls'], sources['base'])
        # Render an offline fixture for metadata round-trip validation.
        output = self.root / 'parts.html'
        # Embed all associations in the standalone document.
        render(model, output)
        # Extract the model without evaluating any scripts.
        encoded = re.search(r'id="robot-model">(.*?)</script>', output.read_text(), re.S).group(1)
        # Require complete preservation of the model and literal filename characters.
        self.assertEqual(json.loads(encoded), model)
        # Exercise invalid mappings that would otherwise mislabel robot parts.
        for invalid in ([], {'unknown': ['part.stl']}, {'base': 'part.stl'}, {'base': []}, {'base': ['part.obj']}):
            # Require a useful failure rather than silently dropping associations.
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                # Apply each malformed mapping to the same valid robot.
                self.load(xml, packages={'parts': self.root}, mesh_sources=invalid)

    # Verify selectable constituents preserve triangles, visual poses, and materials.
    def test_selectable_source_ranges(self):
        # Create two disjoint triangles with distinct bounds.
        vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (2, 0, 0), (3, 0, 0), (2, 1, 0)]
        # Write a synthetic merged STL without private source assets.
        (self.root / 'merged.stl').write_text('solid test\n' + '\n'.join('vertex ' + ' '.join(map(str, v)) for v in vertices) + '\nendsolid')
        # Include a primitive before the mesh to test stable mesh-reference indices.
        xml = '''<robot><link name="base"><visual><geometry><box size="1 1 1"/></geometry></visual>
          <visual><origin xyz="1 2 3" rpy="0 0 1"/><geometry><mesh filename="merged.stl" scale="2 1 1"/></geometry>
          <material><color rgba="0.2 0.3 0.4 1"/></material></visual></link></robot>'''
        # Give identical filenames distinct source-instance indices.
        parts = [{'file': 'part.stl', 'mesh': 0, 'start': 0, 'count': 1},
                 {'file': 'part.stl', 'mesh': 0, 'start': 1, 'count': 1}]
        # Capture the unsplit triangle payload for exact comparison.
        original = self.load(xml)['links']['base']['blocks'][1]
        # Split the same visual using the explicit constituent mapping.
        blocks = self.load(xml, mesh_sources={'base': parts})['links']['base']['blocks']
        # Keep the primitive and both separately selectable source parts.
        self.assertEqual(len(blocks), 3)
        # Require exact triangle preservation without duplicate merged geometry.
        self.assertEqual(b''.join(base64.b64decode(b['stl']) for b in blocks[1:]), base64.b64decode(original['stl']))
        # Preserve distinct source-instance identity despite repeated filenames.
        self.assertEqual([b['sourcePart'] for b in blocks[1:]], [0, 1])
        # Verify scale was applied before computing individual bounds.
        self.assertEqual([b['center'][0] for b in blocks[1:]], [1, 5])
        # Ensure splitting did not move or recolor the visual.
        for block in blocks[1:]:
            # Preserve the parent visual's coordinate transform and material.
            for key in ('at', 'rpy', 'color', 'meshIndex'):
                # Compare each retained property with the original visual.
                self.assertEqual(block[key], original[key])
        # Reject overlaps, gaps, truncation, nonexistent meshes, and fractional counts.
        for change in ({'start': 0}, {'start': 2}, {'count': 2}, {'mesh': 1}, {'count': 0.5}):
            # Exercise a malformed second source part.
            with self.subTest(change=change), self.assertRaises(ValueError):
                # Keep the robot valid so failure is attributable to the mapping.
                self.load(xml, mesh_sources={'base': [parts[0], dict(parts[1], **change)]})
        # Require complete coverage even when the supplied subset is otherwise valid.
        with self.assertRaises(ValueError):
            # Reject a mapping that would omit the second triangle.
            self.load(xml, mesh_sources={'base': parts[:1]})

    def test_offline_output_and_script_escaping(self):
        model = self.load()
        model['name'] = '</script><script>alert(1)</script>'
        output = self.root / 'viewer.html'
        render(model, output)
        html = output.read_text()
        self.assertNotIn('<script src=', html)
        encoded = re.search(r'id="robot-model">(.*?)</script>', html, re.S).group(1)
        self.assertEqual(json.loads(encoded)['name'], model['name'])
        self.assertNotIn('</script>', encoded)
        self.assertNotIn('id="tab-ik"', html)
        self.assertNotIn('function solveIK', html)
        self.assertNotIn('id="play"', html)
        self.assertNotIn('id="stepPlay"', html)

if __name__ == '__main__':
    unittest.main()
