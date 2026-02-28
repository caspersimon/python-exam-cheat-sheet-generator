from __future__ import annotations

from pathlib import Path
import re
import unittest


class RoadmapSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.roadmap = cls.root / "docs" / "ROADMAP.md"
        cls.lines = cls.roadmap.read_text(encoding="utf-8").splitlines()

    def test_roadmap_rows_have_unique_ids_and_valid_status(self) -> None:
        rows = [line for line in self.lines if line.startswith("| RM-")]
        self.assertGreater(len(rows), 0, "Roadmap should contain at least one tracked item.")

        allowed_status = {"planned", "in_progress", "blocked", "done"}
        ids: list[str] = []
        for row in rows:
            parts = [part.strip() for part in row.strip("|").split("|")]
            self.assertEqual(6, len(parts), f"Unexpected roadmap row shape: {row}")
            item_id, _, status, _, _, _ = parts
            self.assertRegex(item_id, r"^RM-\d{3}$")
            self.assertIn(status, allowed_status)
            ids.append(item_id)

        self.assertEqual(len(ids), len(set(ids)), "Roadmap item IDs must be unique.")

    def test_roadmap_spec_links_exist(self) -> None:
        link_pattern = re.compile(r"\(([^)]+)\)")
        rows = [line for line in self.lines if line.startswith("| RM-")]
        for row in rows:
            parts = [part.strip() for part in row.strip("|").split("|")]
            spec_cell = parts[-1]
            match = link_pattern.search(spec_cell)
            self.assertIsNotNone(match, f"Missing spec link in row: {row}")
            rel = match.group(1)
            target = (self.roadmap.parent / rel).resolve()
            self.assertTrue(target.exists(), f"Spec link target missing: {rel}")


if __name__ == "__main__":
    unittest.main()
