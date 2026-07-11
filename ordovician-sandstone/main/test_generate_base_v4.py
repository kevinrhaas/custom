#!/usr/bin/env python3
"""Regression tests for the smooth-shoulder sandstone screw base v4."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile

import generate_base_v4 as v4
from generate_sandstone_v2 import ensure_outward_orientation, mesh_bounds


class BaseV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "base-v4.3mf"
        cls.report_path = Path(cls.temp.name) / "base-v4.report.json"
        cls.report = v4.build_v4(
            v4.DEFAULT_SOURCE,
            cls.output,
            cls.report_path,
            outer_radius=v4.DEFAULT_OUTER_RADIUS,
            inner_radius=v4.DEFAULT_INNER_RADIUS,
            flat_top_radius=v4.DEFAULT_FLAT_TOP_RADIUS,
            body_height=v4.DEFAULT_BODY_HEIGHT,
            side_height=v4.DEFAULT_SIDE_HEIGHT,
            bottom_fillet=v4.DEFAULT_BOTTOM_FILLET,
            circumference_segments=v4.DEFAULT_CIRCUMFERENCE_SEGMENTS,
            shoulder_segments=v4.DEFAULT_SHOULDER_SEGMENTS,
            bottom_fillet_segments=v4.DEFAULT_BOTTOM_FILLET_SEGMENTS,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_outer_component_isolated_without_functional_geometry(self) -> None:
        positive = self.report["positive_mesh"]
        self.assertEqual(positive["source_faces"], 81_722)
        self.assertEqual(positive["old_outer_faces_removed"], 15_092)
        self.assertEqual(positive["functional_faces_preserved"], 66_630)
        self.assertEqual(self.report["functional_geometry"]["components_preserved"], 5)

    def test_new_outer_body_is_watertight_and_exactly_sized(self) -> None:
        profile = v4.smooth_profile(
            -11.0707216,
            outer_radius=v4.DEFAULT_OUTER_RADIUS,
            inner_radius=v4.DEFAULT_INNER_RADIUS,
            flat_top_radius=v4.DEFAULT_FLAT_TOP_RADIUS,
            body_height=v4.DEFAULT_BODY_HEIGHT,
            side_height=v4.DEFAULT_SIDE_HEIGHT,
            bottom_fillet=v4.DEFAULT_BOTTOM_FILLET,
            shoulder_segments=v4.DEFAULT_SHOULDER_SEGMENTS,
            bottom_fillet_segments=v4.DEFAULT_BOTTOM_FILLET_SEGMENTS,
        )
        mesh = v4.revolve_profile(profile, v4.DEFAULT_CIRCUMFERENCE_SEGMENTS)
        report = ensure_outward_orientation(mesh)
        minimums, maximums = mesh_bounds(mesh)
        self.assertTrue(report.watertight)
        self.assertAlmostEqual(maximums[0] - minimums[0], 115.0, places=6)
        self.assertAlmostEqual(maximums[2] - minimums[2], 15.0, places=6)

    def test_shoulder_meets_flat_top_tangentially(self) -> None:
        profile = v4.smooth_profile(
            0.0,
            outer_radius=v4.DEFAULT_OUTER_RADIUS,
            inner_radius=v4.DEFAULT_INNER_RADIUS,
            flat_top_radius=v4.DEFAULT_FLAT_TOP_RADIUS,
            body_height=v4.DEFAULT_BODY_HEIGHT,
            side_height=v4.DEFAULT_SIDE_HEIGHT,
            bottom_fillet=v4.DEFAULT_BOTTOM_FILLET,
            shoulder_segments=v4.DEFAULT_SHOULDER_SEGMENTS,
            bottom_fillet_segments=v4.DEFAULT_BOTTOM_FILLET_SEGMENTS,
        )
        top_join = profile[-2]
        top_inner = profile[-1]
        previous = profile[-3]
        self.assertEqual(top_join, (v4.DEFAULT_FLAT_TOP_RADIUS, v4.DEFAULT_BODY_HEIGHT))
        self.assertEqual(top_inner[1], v4.DEFAULT_BODY_HEIGHT)
        # The final shoulder step rises only a few hundredths of a millimeter,
        # numerically confirming the horizontal tangent into the flat top.
        self.assertLess(top_join[1] - previous[1], 0.02)

    def test_negative_drill_geometry_and_subtype_are_unchanged(self) -> None:
        namespace = {"m": v4.CORE_NS}

        def negative_data(path: Path):
            with ZipFile(path) as archive:
                model_name = next(
                    name
                    for name in archive.namelist()
                    if name.startswith("3D/Objects/") and name.endswith(".model")
                )
                root = ElementTree.fromstring(archive.read(model_name))
                config = ElementTree.fromstring(
                    archive.read("Metadata/model_settings.config")
                )
            negative = root.find('.//m:object[@id="2"]', namespace)
            vertices = [
                tuple(vertex.attrib[key] for key in ("x", "y", "z"))
                for vertex in negative.findall("./m:mesh/m:vertices/m:vertex", namespace)
            ]
            faces = [
                tuple(face.attrib[key] for key in ("v1", "v2", "v3"))
                for face in negative.findall("./m:mesh/m:triangles/m:triangle", namespace)
            ]
            subtype = config.find('.//part[@id="2"]').get("subtype")
            return vertices, faces, subtype

        source_negative = negative_data(v4.DEFAULT_SOURCE)
        output_negative = negative_data(self.output)
        self.assertEqual(source_negative, output_negative)
        self.assertEqual(output_negative[2], "negative_part")


if __name__ == "__main__":
    unittest.main()
