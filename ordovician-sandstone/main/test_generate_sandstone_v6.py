#!/usr/bin/env python3
"""Regression tests for the smooth inner-rim sandstone lamp v6."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile

import generate_sandstone_v6 as v6
from generate_sandstone_v2 import inspect_mesh, read_binary_stl
import generate_sandstone_v5 as v5


class SandstoneV6Tests(unittest.TestCase):
    @staticmethod
    def build(height: float = 120.0, layers: int = 111):
        return v6.build_v6(
            height=height,
            layers=layers,
            wall=v6.DEFAULT_WALL,
            base=v6.DEFAULT_BASE,
            hole=v6.DEFAULT_HOLE,
            top_lip_segments=v6.DEFAULT_TOP_LIP_SEGMENTS,
            connector_top_clearance=v6.DEFAULT_CONNECTOR_TOP_CLEARANCE,
            smooth_lead_in_depth=v6.DEFAULT_SMOOTH_LEAD_IN_DEPTH,
            bore_radial_clearance=v6.DEFAULT_BORE_RADIAL_CLEARANCE,
            source=v6.DEFAULT_SOURCE,
            connector=v6.DEFAULT_CONNECTOR,
        )

    def test_release_presets_are_manifold_and_have_no_dashed_zone(self) -> None:
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
                self.assertTrue(report.smooth_lead_in.clean)
                self.assertEqual(
                    report.smooth_lead_in.connector_intruding_vertices, 0
                )
                self.assertEqual(report.smooth_lead_in.exact_dash_cap_vertices, 0)
                self.assertEqual(report.smooth_lead_in.exact_dash_cap_faces, 0)
                self.assertEqual(report.smooth_lead_in.dashed_zone_faces, 0)
                self.assertFalse(construction["connector_geometry_in_smooth_lead_in"])
                self.assertAlmostEqual(report.final.size_mm[2], height, places=5)

    def test_lead_in_preserves_lower_thread_engagement(self) -> None:
        _, construction, report = self.build()
        self.assertAlmostEqual(
            report.smooth_lead_in.depth_mm,
            v6.DEFAULT_SMOOTH_LEAD_IN_DEPTH,
            places=7,
        )
        self.assertAlmostEqual(
            report.smooth_lead_in.bottom_z_mm,
            v6.DEFAULT_BASE - v6.DEFAULT_SMOOTH_LEAD_IN_DEPTH,
            places=7,
        )
        self.assertAlmostEqual(
            construction["smooth_inner_lead_in_bottom_z_mm"], 7.96, places=7
        )
        source = read_binary_stl(v6.DEFAULT_CONNECTOR)
        smoothed = v6.smooth_connector_lead_in(
            source,
            base=v6.DEFAULT_BASE,
            hole=v6.DEFAULT_HOLE,
            depth=v6.DEFAULT_SMOOTH_LEAD_IN_DEPTH,
            radial_clearance=v6.DEFAULT_BORE_RADIAL_CLEARANCE,
            top_clearance=v6.DEFAULT_CONNECTOR_TOP_CLEARANCE,
        )

        def lower_triangles(mesh):
            result = set()
            for face in mesh.faces:
                points = [mesh.points[index] for index in face]
                if max(point[2] for point in points) >= 7.95:
                    continue
                result.add(
                    tuple(
                        sorted(
                            tuple(round(value, 6) for value in point)
                            for point in points
                        )
                    )
                )
            return result

        source_lower = lower_triangles(source)
        smoothed_lower = lower_triangles(smoothed)
        self.assertEqual(len(source_lower), 5996)
        self.assertEqual(smoothed_lower, source_lower)

    def test_lead_in_validator_detects_the_v5_dashed_geometry(self) -> None:
        old_mesh, _, _ = v5.build_v5(
            height=120.0,
            layers=111,
            wall=v5.DEFAULT_WALL,
            base=v5.DEFAULT_BASE,
            hole=v5.DEFAULT_HOLE,
            top_lip_segments=v5.DEFAULT_TOP_LIP_SEGMENTS,
            connector_top_clearance=v5.DEFAULT_CONNECTOR_TOP_CLEARANCE,
            source=v5.DEFAULT_SOURCE,
            connector=v5.DEFAULT_CONNECTOR,
        )
        old_report = v6.inspect_lead_in(
            old_mesh,
            base=v6.DEFAULT_BASE,
            hole=v6.DEFAULT_HOLE,
            depth=v6.DEFAULT_SMOOTH_LEAD_IN_DEPTH,
            radial_clearance=v6.DEFAULT_BORE_RADIAL_CLEARANCE,
        )
        self.assertFalse(old_report.clean)
        self.assertEqual(old_report.connector_intruding_vertices, 1372)
        self.assertEqual(old_report.exact_dash_cap_vertices, 209)
        self.assertEqual(old_report.exact_dash_cap_faces, 179)
        self.assertEqual(old_report.dashed_zone_faces, 511)

    def test_gentle_top_lip_is_unchanged(self) -> None:
        _, construction, _ = self.build()
        self.assertEqual(
            construction["top_lip_segments"], v6.DEFAULT_TOP_LIP_SEGMENTS
        )
        self.assertAlmostEqual(
            construction["top_lip_radius_mm"], v6.DEFAULT_WALL / 2.0, places=7
        )
        self.assertAlmostEqual(construction["top_lip_crest_z_mm"], 120.0, places=7)

    def test_stl_round_trip_preserves_smooth_lead_in(self) -> None:
        mesh, _, _ = self.build()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp.stl"
            v6.write_binary_stl_v6(path, mesh)
            round_trip = read_binary_stl(path)
        mesh_report = inspect_mesh(round_trip)
        lead_in = v6.inspect_lead_in(
            round_trip,
            base=v6.DEFAULT_BASE,
            hole=v6.DEFAULT_HOLE,
            depth=v6.DEFAULT_SMOOTH_LEAD_IN_DEPTH,
            radial_clearance=v6.DEFAULT_BORE_RADIAL_CLEARANCE,
        )
        self.assertTrue(mesh_report.watertight)
        self.assertTrue(lead_in.clean)

    def test_3mf_is_one_v6_mesh_object(self) -> None:
        mesh, _, _ = self.build()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp.3mf"
            v6.write_3mf_v6(path, mesh)
            with ZipFile(path) as archive:
                model = archive.read("3D/3dmodel.model")
        root = ElementTree.fromstring(model)
        namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        title = root.find('./m:metadata[@name="Title"]', namespace)
        self.assertEqual(title.text, "Illinois Sandstone Lamp v6")
        self.assertEqual(len(root.findall("./m:resources/m:object", namespace)), 1)
        self.assertEqual(len(root.findall("./m:build/m:item", namespace)), 1)
        self.assertEqual(len(root.findall(".//m:component", namespace)), 0)


if __name__ == "__main__":
    unittest.main()
