#!/usr/bin/env python3
"""Regression tests for the clean-finish sandstone lamp v5 generator."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile

import generate_sandstone_v5 as v5
from generate_sandstone_v2 import inspect_mesh, mesh_bounds, read_binary_stl


class SandstoneV5Tests(unittest.TestCase):
    @staticmethod
    def build(height: float = 120.0, layers: int = 111):
        return v5.build_v5(
            height=height,
            layers=layers,
            wall=v5.DEFAULT_WALL,
            base=v5.DEFAULT_BASE,
            hole=v5.DEFAULT_HOLE,
            top_lip_segments=v5.DEFAULT_TOP_LIP_SEGMENTS,
            connector_top_clearance=v5.DEFAULT_CONNECTOR_TOP_CLEARANCE,
            source=v5.DEFAULT_SOURCE,
            connector=v5.DEFAULT_CONNECTOR,
        )

    def test_connector_is_recessed_below_finish_plane(self) -> None:
        connector = read_binary_stl(v5.DEFAULT_CONNECTOR)
        trimmed = v5.trim_connector_top(
            connector, v5.DEFAULT_BASE, v5.DEFAULT_CONNECTOR_TOP_CLEARANCE
        )
        report = inspect_mesh(trimmed)
        self.assertTrue(report.watertight)
        self.assertAlmostEqual(
            mesh_bounds(trimmed)[1][2],
            v5.DEFAULT_BASE - v5.DEFAULT_CONNECTOR_TOP_CLEARANCE,
            places=5,
        )

    def test_release_presets_have_clean_finish_and_manifold_mesh(self) -> None:
        for height, layers in ((120.0, 111), (150.0, 139), (180.0, 166)):
            with self.subTest(height=height):
                _, construction, report = self.build(height, layers)
                self.assertTrue(report.final.watertight)
                self.assertEqual(report.final.boundary_edges, 0)
                self.assertEqual(report.final.nonmanifold_edges, 0)
                self.assertEqual(report.final.degenerate_faces, 0)
                self.assertEqual(report.final.connected_components, 1)
                self.assertTrue(report.finish_plane.clean)
                self.assertEqual(report.finish_plane.faces, 240)
                self.assertEqual(report.finish_plane.micro_triangles, 0)
                self.assertGreater(
                    report.finish_plane.minimum_triangle_area_mm2, 5.0
                )
                self.assertFalse(construction["connector_geometry_on_finish_plane"])
                self.assertAlmostEqual(report.final.size_mm[2], height, places=5)

    def test_gentle_top_lip_is_unchanged(self) -> None:
        _, construction, _ = self.build()
        self.assertEqual(
            construction["top_lip_segments"], v5.DEFAULT_TOP_LIP_SEGMENTS
        )
        self.assertAlmostEqual(
            construction["top_lip_radius_mm"], v5.DEFAULT_WALL / 2.0, places=7
        )
        self.assertAlmostEqual(construction["top_lip_crest_z_mm"], 120.0, places=7)

    def test_stl_round_trip_preserves_clean_finish(self) -> None:
        mesh, _, _ = self.build()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp.stl"
            v5.write_binary_stl_v5(path, mesh)
            round_trip = read_binary_stl(path)
        mesh_report = inspect_mesh(round_trip)
        finish = v5.inspect_finish_plane(
            round_trip, z=v5.DEFAULT_BASE, expected_faces=240
        )
        self.assertTrue(mesh_report.watertight)
        self.assertTrue(finish.clean)

    def test_3mf_is_one_mesh_object(self) -> None:
        mesh, _, _ = self.build()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp.3mf"
            v5.write_3mf_v5(path, mesh)
            with ZipFile(path) as archive:
                model = archive.read("3D/3dmodel.model")
        root = ElementTree.fromstring(model)
        namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        self.assertEqual(len(root.findall("./m:resources/m:object", namespace)), 1)
        self.assertEqual(len(root.findall("./m:build/m:item", namespace)), 1)
        self.assertEqual(len(root.findall(".//m:component", namespace)), 0)


if __name__ == "__main__":
    unittest.main()
