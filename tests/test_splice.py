import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import splice  # noqa: E402

START, END = "<!-- cluster:start -->", "<!-- cluster:end -->"


class SpliceTest(unittest.TestCase):
    def test_replaces_only_between_markers(self):
        readme = f"top\n{START}\nold\n{END}\nbottom\n"
        out = splice.splice(readme, "cluster", "new")
        self.assertEqual(out, f"top\n{START}\nnew\n{END}\nbottom\n")

    def test_idempotent(self):
        readme = f"a\n{START}\n{END}\nb"
        once = splice.splice(readme, "cluster", "t")
        self.assertEqual(splice.splice(once, "cluster", "t"), once)

    def test_missing_end_marker_raises(self):
        with self.assertRaises(ValueError):
            splice.splice(f"a\n{START}\nold\n", "cluster", "new")


if __name__ == "__main__":
    unittest.main()
