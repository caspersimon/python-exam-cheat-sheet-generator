from pathlib import Path
import os
import unittest


class MaterialsByWeekSymlinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.by_week = cls.root / "materials" / "by_week"

    def test_by_week_leaf_entries_are_symlinks_with_existing_targets(self) -> None:
        entries = []
        for path in self.by_week.rglob("*"):
            if path.name.startswith("."):
                continue
            if path.is_dir() and not path.is_symlink():
                continue
            entries.append(path)

        self.assertGreater(len(entries), 0, "Expected materials/by_week to contain linked material entries")

        for entry in entries:
            self.assertTrue(entry.is_symlink(), f"{entry}: expected by_week entry to be a symlink")
            target = (entry.parent / os.readlink(entry)).resolve()
            self.assertTrue(target.exists(), f"{entry}: symlink target does not exist: {target}")


if __name__ == "__main__":
    unittest.main()
