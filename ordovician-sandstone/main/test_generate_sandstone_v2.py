#!/usr/bin/env python3
"""Regression tests for the detail-preserving sandstone lamp v2 generator."""

from __future__ import annotations

import math
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile

import generate_sandstone_v2 as v2


class SandstoneV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = v2.read_source_rings(v2.DEFAULT_SOURCE)
        cls.resampled = v2.source_preserving_resample(cls.source, v2.DEFAULT_LAYERS)
        cls.outer = v2.scale_rings_to_height(cls.resampled, v2.DEFAULT_HEIGHT)
        cls.mesh, cls.metadata = v2.build_lamp_mesh(
            cls.outer,
            v2.DEFAULT_WALL,
            v2.DEFAULT_BASE,
            v2.DEFAULT_HOLE,
            v2.DEFAULT_TOP_LIP_SEGMENTS,
        )
        cls.report = v2.ensure_outward_orientation(cls.mesh)

    def test_default_mesh_is_single_watertight_component(self) -> None:
        self.assertTrue(self.report.watertight)
        self.assertEqual(self.report.boundary_edges, 0)
        self.assertEqual(self.report.nonmanifold_edges, 0)
        self.assertEqual(self.report.connected_components, 1)
        self.assertEqual(self.report.degenerate_faces, 0)

    def test_requested_dimensions_and_floor_are_exact(self) -> None:
        self.assertAlmostEqual(self.report.size_mm[2], v2.DEFAULT_HEIGHT, places=7)
        self.assertAlmostEqual(self.metadata["floor_z_mm"], v2.DEFAULT_BASE, places=7)
        self.assertAlmostEqual(
            self.metadata["hole_diameter_mm"], v2.DEFAULT_HOLE, places=7
        )
        self.assertGreater(
            self.metadata["first_organic_inner_min_z_mm"], v2.DEFAULT_BASE
        )

    def test_every_source_xy_ring_is_retained(self) -> None:
        # Every source control ring must appear verbatim in the resampled list.
        resampled_xy = {
            tuple((point[0], point[1]) for point in ring) for ring in self.resampled
        }
        for ring in self.source:
            source_xy = tuple((point[0], point[1]) for point in ring)
            self.assertIn(source_xy, resampled_xy)

    def test_rounded_top_lip_has_inward_return_and_exact_crest(self) -> None:
        self.assertEqual(
            self.metadata["top_lip_segments"], v2.DEFAULT_TOP_LIP_SEGMENTS
        )
        self.assertAlmostEqual(
            self.metadata["top_lip_crest_z_mm"], v2.DEFAULT_HEIGHT, places=7
        )
        self.assertAlmostEqual(
            self.metadata["top_lip_radius_mm"], v2.DEFAULT_WALL / 2.0, places=7
        )
        self.assertAlmostEqual(
            self.metadata["top_lip_join_z_mm"],
            v2.DEFAULT_HEIGHT - v2.DEFAULT_WALL / 2.0,
            places=7,
        )

    def test_written_3mf_contains_one_indexed_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp.3mf"
            v2.write_3mf(path, self.mesh)
            with ZipFile(path) as archive:
                self.assertIn("3D/3dmodel.model", archive.namelist())
                model = archive.read("3D/3dmodel.model")
                self.assertEqual(model.count(b"<vertex "), len(self.mesh.points))
                self.assertEqual(model.count(b"<triangle "), len(self.mesh.faces))

    def test_connector_matches_lamp_base_and_thread_opening(self) -> None:
        connector = v2.read_binary_stl(v2.DEFAULT_CONNECTOR)
        minimums, maximums = v2.mesh_bounds(connector)
        radii = [math.hypot(x, y) for x, y, _ in connector.points]
        self.assertAlmostEqual(minimums[2], 0.0, places=5)
        self.assertAlmostEqual(maximums[2], v2.DEFAULT_BASE, places=4)
        self.assertAlmostEqual(max(radii) * 2.0, 80.0, places=3)
        self.assertLess(min(radii), v2.DEFAULT_HOLE / 2.0)

    def test_written_connected_3mf_is_one_multipart_build_item(self) -> None:
        connector = v2.read_binary_stl(v2.DEFAULT_CONNECTOR)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "connected-lamp.3mf"
            v2.write_3mf(path, self.mesh, connector)
            with ZipFile(path) as archive:
                model = archive.read("3D/3dmodel.model")
            root = ElementTree.fromstring(model)
            namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
            self.assertEqual(len(root.findall("./m:resources/m:object", namespace)), 3)
            self.assertEqual(len(root.findall("./m:build/m:item", namespace)), 1)
            self.assertEqual(len(root.findall(".//m:components/m:component", namespace)), 2)
            self.assertEqual(
                len(root.findall(".//m:vertex", namespace)),
                len(self.mesh.points) + len(connector.points),
            )

    def test_release_height_layer_presets_are_valid(self) -> None:
        for height, layers in ((120.0, 111), (150.0, 139), (180.0, 166)):
            with self.subTest(height=height):
                rings = v2.scale_rings_to_height(
                    v2.source_preserving_resample(self.source, layers), height
                )
                mesh, _ = v2.build_lamp_mesh(
                    rings,
                    v2.DEFAULT_WALL,
                    v2.DEFAULT_BASE,
                    v2.DEFAULT_HOLE,
                    v2.DEFAULT_TOP_LIP_SEGMENTS,
                )
                report = v2.ensure_outward_orientation(mesh)
                self.assertTrue(report.watertight)
                self.assertAlmostEqual(report.size_mm[2], height, places=7)


if __name__ == "__main__":
    unittest.main()
