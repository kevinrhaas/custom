#!/usr/bin/env python3
"""Regression tests for the gently tapered sandstone lamp v7."""

from __future__ import annotations

import math
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from zipfile import ZipFile

import generate_sandstone_v7 as v7
from generate_sandstone_v2 import (
    build_lamp_mesh,
    inspect_mesh,
    radial_offset_inward,
    read_binary_stl,
    read_source_rings,
    scale_rings_to_height,
    source_preserving_resample,
)


class SandstoneV7Tests(unittest.TestCase):
    @staticmethod
    def build(height: float = 120.0, layers: int = 111):
        return v7.build_v7(
            height=height,
            layers=layers,
            wall=v7.DEFAULT_WALL,
            base=v7.DEFAULT_BASE,
            hole=v7.DEFAULT_HOLE,
            top_lip_segments=v7.DEFAULT_TOP_LIP_SEGMENTS,
            connector_top_clearance=v7.v6.DEFAULT_CONNECTOR_TOP_CLEARANCE,
            smooth_lead_in_depth=v7.v6.DEFAULT_SMOOTH_LEAD_IN_DEPTH,
            bore_radial_clearance=v7.v6.DEFAULT_BORE_RADIAL_CLEARANCE,
            top_taper_height=v7.DEFAULT_TOP_TAPER_HEIGHT,
            top_taper_inset=v7.DEFAULT_TOP_TAPER_INSET,
            source=v7.DEFAULT_SOURCE,
            connector=v7.DEFAULT_CONNECTOR,
        )

    @staticmethod
    def source_rings(height: float = 120.0, layers: int = 111):
        source = read_source_rings(v7.DEFAULT_SOURCE)
        return scale_rings_to_height(
            source_preserving_resample(source, layers),
            height - v7.DEFAULT_WALL / 2.0,
        )

    def test_raised_cosine_is_gentle_and_monotone(self) -> None:
        values = [v7.raised_cosine(step / 100.0) for step in range(101)]
        self.assertEqual(values[0], 0.0)
        self.assertEqual(values[-1], 1.0)
        self.assertAlmostEqual(values[50], 0.5, places=12)
        self.assertTrue(all(left <= right for left, right in zip(values, values[1:])))
        self.assertAlmostEqual(v7.raised_cosine(0.000001), 0.0, places=10)
        self.assertAlmostEqual(v7.raised_cosine(0.999999), 1.0, places=10)

    def test_taper_preserves_every_point_below_its_start(self) -> None:
        original = self.source_rings()
        tapered, report = v7.apply_top_taper(
            original,
            height=120.0,
            wall=v7.DEFAULT_WALL,
            taper_height=v7.DEFAULT_TOP_TAPER_HEIGHT,
            radial_inset=v7.DEFAULT_TOP_TAPER_INSET,
        )
        unchanged = 0
        changed = 0
        for source_ring, tapered_ring in zip(original, tapered):
            for source_point, tapered_point in zip(source_ring, tapered_ring):
                if source_point[2] <= report.taper_start_z_mm:
                    self.assertEqual(tapered_point, source_point)
                    unchanged += 1
                elif tapered_point != source_point:
                    changed += 1
        self.assertGreater(unchanged, 12_000)
        self.assertGreater(changed, 0)

    def test_default_transition_and_rounded_lip_geometry(self) -> None:
        original = self.source_rings()
        tapered, taper = v7.apply_top_taper(
            original,
            height=120.0,
            wall=v7.DEFAULT_WALL,
            taper_height=v7.DEFAULT_TOP_TAPER_HEIGHT,
            radial_inset=v7.DEFAULT_TOP_TAPER_INSET,
        )
        body_rings = [list(ring) for ring in tapered]
        body_rings[-1] = [(x, y, 120.0) for x, y, _ in body_rings[-1]]
        _, construction = build_lamp_mesh(
            body_rings,
            v7.DEFAULT_WALL,
            v7.DEFAULT_BASE,
            v7.DEFAULT_HOLE,
            v7.DEFAULT_TOP_LIP_SEGMENTS,
        )
        self.assertEqual(taper.curve, "raised cosine")
        self.assertAlmostEqual(taper.taper_start_z_mm, 111.0, places=7)
        self.assertAlmostEqual(taper.rounded_lip_join_z_mm, 119.0, places=7)
        self.assertAlmostEqual(taper.crest_z_mm, 120.0, places=7)
        self.assertAlmostEqual(taper.taper_height_mm, 8.0, places=7)
        self.assertAlmostEqual(taper.radial_inset_mm, 1.5, places=7)
        self.assertAlmostEqual(taper.total_transition_height_to_crest_mm, 9.0)
        self.assertAlmostEqual(
            taper.top_outer_radius_before_min_mm
            - taper.top_outer_radius_after_min_mm,
            1.5,
            places=7,
        )
        self.assertEqual(construction["top_lip_segments"], 8)
        self.assertAlmostEqual(construction["top_lip_radius_mm"], 1.0, places=7)
        self.assertAlmostEqual(construction["top_lip_join_z_mm"], 119.0, places=7)
        self.assertAlmostEqual(construction["top_lip_crest_z_mm"], 120.0, places=7)
        inner_top = radial_offset_inward(tapered[-1], v7.DEFAULT_WALL)
        for outer_point, inner_point in zip(tapered[-1], inner_top):
            radial_wall = math.hypot(outer_point[0], outer_point[1]) - math.hypot(
                inner_point[0], inner_point[1]
            )
            self.assertAlmostEqual(radial_wall, v7.DEFAULT_WALL, places=10)

    def test_default_transition_is_support_free(self) -> None:
        _, _, report = self.build()
        taper = report.top_taper
        expected_slope = 1.5 * math.pi / (2.0 * 8.0)
        self.assertAlmostEqual(taper.maximum_slope_mm_per_mm, expected_slope)
        self.assertLess(taper.maximum_angle_from_vertical_degrees, 17.0)
        self.assertLess(taper.maximum_radial_shift_per_layer_mm, 0.05)
        self.assertGreater(taper.last_organic_segment_height_mm, 1.0)
        self.assertLess(
            taper.maximum_last_segment_angle_from_vertical_degrees, 25.0
        )
        self.assertLess(
            taper.maximum_last_segment_radial_shift_per_layer_mm, 0.08
        )
        self.assertGreater(taper.minimum_line_overlap_percent, 82.0)
        self.assertGreaterEqual(taper.minimum_inner_rim_diameter_mm, 70.9)
        self.assertTrue(taper.printable_without_support)

    def test_release_presets_are_single_manifold_solids(self) -> None:
        for height, layers in ((120.0, 111), (150.0, 139), (180.0, 166)):
            with self.subTest(height=height):
                _, construction, report = self.build(height, layers)
                self.assertTrue(report.final.watertight)
                self.assertEqual(report.final.boundary_edges, 0)
                self.assertEqual(report.final.nonmanifold_edges, 0)
                self.assertEqual(report.final.degenerate_faces, 0)
                self.assertEqual(report.final.duplicate_faces, 0)
                self.assertEqual(report.final.connected_components, 1)
                self.assertAlmostEqual(report.final.size_mm[2], height, places=5)
                self.assertTrue(report.finish_plane.clean)
                self.assertEqual(report.finish_plane.faces, 240)
                self.assertTrue(report.smooth_lead_in.clean)
                self.assertEqual(report.smooth_lead_in.dashed_zone_faces, 0)
                self.assertTrue(report.top_taper.printable_without_support)
                self.assertTrue(construction["continuous_interior_floor"])
                self.assertTrue(construction["geometry_only_3mf"])

    def test_stl_round_trip_remains_watertight(self) -> None:
        mesh, _, report = self.build()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp-v7.stl"
            v7.write_binary_stl_v7(path, mesh)
            round_trip = read_binary_stl(path)
        round_trip_report = inspect_mesh(round_trip)
        self.assertEqual(round_trip_report.faces, report.final.faces)
        self.assertTrue(round_trip_report.watertight)
        self.assertEqual(round_trip_report.boundary_edges, 0)
        self.assertEqual(round_trip_report.nonmanifold_edges, 0)

    def test_3mf_contains_geometry_and_no_slicer_settings(self) -> None:
        mesh, _, _ = self.build()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lamp-v7.3mf"
            v7.write_3mf_v7(path, mesh)
            with ZipFile(path) as archive:
                self.assertEqual(
                    set(archive.namelist()),
                    {"[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model"},
                )
                model = archive.read("3D/3dmodel.model")
        root = ElementTree.fromstring(model)
        namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        title = root.find('./m:metadata[@name="Title"]', namespace)
        description = root.find('./m:metadata[@name="Description"]', namespace)
        self.assertEqual(title.text, "Illinois Sandstone Lamp v7")
        self.assertEqual(description.text, "Geometry only - no slicer settings")
        self.assertEqual(len(root.findall("./m:resources/m:object", namespace)), 1)
        self.assertEqual(len(root.findall("./m:build/m:item", namespace)), 1)
        self.assertEqual(len(root.findall(".//m:component", namespace)), 0)


if __name__ == "__main__":
    unittest.main()
