import sys
import unittest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import activity  # noqa: E402

START, END = "<!-- activity:start -->", "<!-- activity:end -->"


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


class HabitsTest(unittest.TestCase):
    def test_utc_commit_lands_in_local_hour_and_day(self):
        # 23:30 UTC on Sunday 2026-01-04 is 00:30 Monday in Berlin (UTC+1 in winter).
        t = datetime(2026, 1, 4, 23, 30, tzinfo=timezone.utc)
        hours, weekdays = activity.habits([t], ZoneInfo("Europe/Berlin"))
        self.assertEqual(hours.index(1), 0)
        self.assertEqual(weekdays.index(1), 0)

    def test_summer_offset(self):
        t = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
        hours, _ = activity.habits([t], ZoneInfo("Europe/Berlin"))
        self.assertEqual(hours.index(1), 14)

    def test_spark_max_is_tallest_zero_is_dot(self):
        self.assertEqual(activity.spark([0, 1]), "·█")
        self.assertEqual(activity.spark([0, 1, 8]), "·▁█")

    def test_spark_all_zero(self):
        self.assertEqual(activity.spark([0, 0, 0]), "···")

    def test_hour_axis_and_spark_line_up(self):
        hours = [0] * 24
        hours[12] = 3
        lines = activity.render_habits(hours, [0, 0, 3, 0, 0, 0, 0], 365, "Europe/Berlin").splitlines()
        self.assertEqual(lines[1].index("12"), lines[2].index("█"))
        self.assertIn("peak 12:00", lines[2])
        self.assertIn("peak Wed", lines[5])

    def test_no_commits(self):
        self.assertIn("No public commits", activity.render_habits([0] * 24, [0] * 7, 365, "UTC"))


class PublicReposTest(unittest.TestCase):
    def test_private_names_never_queried(self):
        c = collection(entry("hugad/hugad-ops", 5, private=True), entry("jomhoor/.github", 1, language=None))
        self.assertEqual(activity.public_repos(c), ["jomhoor/.github"])


class SpliceTest(unittest.TestCase):
    def test_replaces_only_between_markers(self):
        readme = f"top\n{START}\nold\n{END}\nbottom\n"
        out = activity.splice(readme, "activity", "new")
        self.assertEqual(out, f"top\n{START}\nnew\n{END}\nbottom\n")

    def test_idempotent(self):
        readme = f"a\n{START}\n{END}\nb"
        once = activity.splice(readme, "activity", "t")
        self.assertEqual(activity.splice(once, "activity", "t"), once)

    def test_missing_end_marker_raises(self):
        with self.assertRaises(ValueError):
            activity.splice(f"a\n{START}\nold\n", "activity", "new")


if __name__ == "__main__":
    unittest.main()
