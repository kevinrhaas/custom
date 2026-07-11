#!/usr/bin/env python3
"""Regression tests for the single-body sandstone lamp v4 generator."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile

import generate_sandstone_v4 as v4
from generate_sandstone_v2 import inspect_mesh, mesh_bounds, read_binary_stl


class SandstoneV4Tests(unittest.TestCase):
    def test_prepared_connector_is_one_watertight_component(self) -> None:
        connector = read_binary_stl(v4.DEFAULT_CONNECTOR)
        report = inspect_mesh(connector)
        minimums, maximums = mesh_bounds(connector)
        self.assertTrue(report.watertight)
        self.assertEqual(report.boundary_edges, 0)
        self.assertEqual(report.nonmanifold_edges, 0)
        self.assertEqual(report.connected_components, 1)
        self.assertAlmostEqual(minimums[2], 0.0, places=5)
        self.assertAlmostEqual(maximums[2], v4.DEFAULT_BASE, places=4)

    def test_release_presets_are_single_manifold_boolean_solids(self) -> None:
        for height, layers in ((120.0, 111), (150.0, 139), (180.0, 166)):
            with self.subTest(height=height):
                mesh, construction, report = v4.build_v4(
                    height=height,
                    layers=layers,
                    wall=v4.DEFAULT_WALL,
                    base=v4.DEFAULT_BASE,
                    hole=v4.DEFAULT_HOLE,
                    top_lip_segments=v4.DEFAULT_TOP_LIP_SEGMENTS,
                    source=v4.DEFAULT_SOURCE,
                    connector=v4.DEFAULT_CONNECTOR,
                )
                self.assertTrue(report.final.watertight)
                self.assertEqual(report.final.boundary_edges, 0)
                self.assertEqual(report.final.nonmanifold_edges, 0)
                self.assertEqual(report.final.degenerate_faces, 0)
                self.assertEqual(report.final.connected_components, 1)
                self.assertTrue(report.single_body_boolean_union)
                self.assertEqual(report.internal_floor_coplanar_duplicate_faces, 0)
                self.assertTrue(construction["continuous_interior_floor"])
                self.assertAlmostEqual(report.final.size_mm[2], height, places=5)
                self.assertLess(
                    len(mesh.faces),
                    report.lamp_body.faces + report.connector.faces,
                    "a true Boolean must remove overlapping interior triangles",
                )

    def test_gentle_top_lip_is_retained(self) -> None:
        _, construction, _ = v4.build_v4(
            height=120.0,
            layers=111,
            wall=v4.DEFAULT_WALL,
            base=v4.DEFAULT_BASE,
            hole=v4.DEFAULT_HOLE,
            top_lip_segments=v4.DEFAULT_TOP_LIP_SEGMENTS,
            source=v4.DEFAULT_SOURCE,
            connector=None,
        )
        self.assertEqual(
            construction["top_lip_segments"], v4.DEFAULT_TOP_LIP_SEGMENTS
        )
        self.assertAlmostEqual(
            construction["top_lip_radius_mm"], v4.DEFAULT_WALL / 2.0, places=7
        )
        self.assertAlmostEqual(construction["top_lip_crest_z_mm"], 120.0, places=7)

    def test_stl_round_trip_remains_watertight(self) -> None:
        mesh, _, _ = v4.build_v4(
            height=120.0,
            layers=111,
            wall=v4.DEFAULT_WALL,
            base=v4.DEFAULT_BASE,
            hole=v4.DEFAULT_HOLE,
            top_lip_segments=v4.DEFAULT_TOP_LIP_SEGMENTS,
            source=v4.DEFAULT_SOURCE,
            connector=v4.DEFAULT_CONNECTOR,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp.stl"
            v4.write_binary_stl_v4(path, mesh)
            report = inspect_mesh(read_binary_stl(path))
        self.assertTrue(report.watertight)
        self.assertEqual(report.nonmanifold_edges, 0)
        self.assertEqual(report.degenerate_faces, 0)

    def test_3mf_contains_one_mesh_and_no_multipart_components(self) -> None:
        mesh, _, _ = v4.build_v4(
            height=120.0,
            layers=111,
            wall=v4.DEFAULT_WALL,
            base=v4.DEFAULT_BASE,
            hole=v4.DEFAULT_HOLE,
            top_lip_segments=v4.DEFAULT_TOP_LIP_SEGMENTS,
            source=v4.DEFAULT_SOURCE,
            connector=v4.DEFAULT_CONNECTOR,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp.3mf"
            v4.write_3mf_v4(path, mesh)
            with ZipFile(path) as archive:
                model = archive.read("3D/3dmodel.model")
        root = ElementTree.fromstring(model)
        namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        self.assertEqual(len(root.findall("./m:resources/m:object", namespace)), 1)
        self.assertEqual(len(root.findall("./m:build/m:item", namespace)), 1)
        self.assertEqual(len(root.findall(".//m:component", namespace)), 0)
        self.assertEqual(len(root.findall(".//m:vertex", namespace)), len(mesh.points))
        self.assertEqual(len(root.findall(".//m:triangle", namespace)), len(mesh.faces))


if __name__ == "__main__":
    unittest.main()
