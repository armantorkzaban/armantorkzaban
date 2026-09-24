import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import activity  # noqa: E402


def entry(name, count, private=False, fork=False, description=None, language="Go"):
    return {
        "repository": {
            "nameWithOwner": name,
            "url": f"https://github.com/{name}",
            "description": description,
            "isPrivate": private,
            "isFork": fork,
            "primaryLanguage": {"name": language} if language else None,
        },
        "contributions": {"totalCount": count},
    }


def names(rows):
    return [r["nameWithOwner"] for r, _ in rows]


def collection(*entries, restricted=0):
    return {"restrictedContributionsCount": restricted, "commitContributionsByRepository": list(entries)}


class SelectTest(unittest.TestCase):
    def test_private_repo_folded_into_count_not_named(self):
        c = collection(entry("hugad/hugad-ops", 500, private=True), entry("jomhoor/Platform", 3), restricted=40)
        rows, private = activity.select(c, "arman", 6)
        self.assertEqual(names(rows), ["jomhoor/Platform"])
        self.assertEqual(private, 540)

    def test_private_repo_without_language_still_counted(self):
        _, private = activity.select(collection(entry("tcfev/secrets", 4, private=True, language=None)), "arman", 6)
        self.assertEqual(private, 4)

    def test_forks_profile_repo_and_repos_without_code_skipped(self):
        c = collection(
            entry("jomhoor/Taraaz-Deliberation", 40, fork=True),
            entry("arman/arman", 90),
            entry("jomhoor/.github", 7, language=None),
            entry("jomhoor/Jomhoor.org", 5, language="HTML"),
        )
        rows, private = activity.select(c, "arman", 6)
        self.assertEqual(names(rows), ["jomhoor/Jomhoor.org"])
        self.assertEqual(private, 0)

    def test_sorted_by_commits_then_name_and_limited(self):
        c = collection(entry("b/x", 5), entry("a/x", 5), entry("c/x", 9), entry("d/x", 1))
        rows, _ = activity.select(c, "arman", 3)
        self.assertEqual(names(rows), ["c/x", "a/x", "b/x"])


class RenderTest(unittest.TestCase):
    def test_pipe_in_description_escaped(self):
        repo = entry("a/x", 2, description="en | fa")["repository"]
        row = activity.render([(repo, 2)], 0, 90).splitlines()[-1]
        self.assertIn("en \\| fa", row)
        self.assertEqual(row.count("|") - row.count("\\|"), 4)

    def test_private_summary(self):
        self.assertEqual(activity.render([], 12, 90), "Plus 12 contributions to private repositories.")

    def test_empty(self):
        self.assertIn("No activity", activity.render([], 0, 30))


class SpliceTest(unittest.TestCase):
    def test_replaces_only_between_markers(self):
        readme = f"top\n{activity.START}\nold\n{activity.END}\nbottom\n"
        out = activity.splice(readme, "new")
        self.assertEqual(out, f"top\n{activity.START}\nnew\n{activity.END}\nbottom\n")

    def test_idempotent(self):
        readme = f"a\n{activity.START}\n{activity.END}\nb"
        once = activity.splice(readme, "t")
        self.assertEqual(activity.splice(once, "t"), once)

    def test_missing_end_marker_raises(self):
        with self.assertRaises(ValueError):
            activity.splice(f"a\n{activity.START}\nold\n", "new")


if __name__ == "__main__":
    unittest.main()
