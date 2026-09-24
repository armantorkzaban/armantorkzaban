"""Rewrite the activity and habits blocks in README.md from the GitHub GraphQL API."""

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

API = "https://api.github.com/graphql"
SPARKS = "▁▂▃▄▅▆▇█"
WEEKDAYS = "MTWTFSS"

QUERY = """
query($login: String!, $from: DateTime!) {
  user(login: $login) {
    id
    contributionsCollection(from: $from) {
      restrictedContributionsCount
      commitContributionsByRepository(maxRepositories: 50) {
        repository { nameWithOwner url description isPrivate isFork primaryLanguage { name } }
        contributions { totalCount }
      }
    }
  }
}
"""

HISTORY = """
  r{i}: repository(owner: "{owner}", name: "{name}") {{
    defaultBranchRef {{ target {{ ... on Commit {{
      history(first: 100, since: $from, author: {{id: $id}}) {{ nodes {{ authoredDate }} }}
    }} }} }}
  }}"""


def graphql(token, query, variables):
    body = json.dumps({"query": query, "variables": variables})
    req = urllib.request.Request(
        API, data=body.encode(), headers={"Authorization": f"bearer {token}"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    return payload["data"]


def fetch(login, token, days):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    return graphql(token, QUERY, {"login": login, "from": since.isoformat()})["user"]


def commit_times(token, user_id, repos, days):
    # One aliased query for all repos instead of one request each. Default branch
    # only, and at most 100 commits per repo: enough for a shape, not an audit.
    if not repos:
        return []
    since = datetime.now(timezone.utc) - timedelta(days=days)
    fields = "".join(
        HISTORY.format(i=i, owner=r.split("/")[0], name=r.split("/")[1]) for i, r in enumerate(repos)
    )
    query = f"query($id: ID!, $from: GitTimestamp!) {{{fields}\n}}"
    data = graphql(token, query, {"id": user_id, "from": since.isoformat()})
    times = []
    for repo in data.values():
        target = ((repo or {}).get("defaultBranchRef") or {}).get("target") or {}
        for node in target.get("history", {}).get("nodes", []):
            times.append(datetime.fromisoformat(node["authoredDate"].replace("Z", "+00:00")))
    return times


def public_repos(collection):
    return [
        e["repository"]["nameWithOwner"]
        for e in collection["commitContributionsByRepository"]
        if not e["repository"]["isPrivate"]
    ]


def select(collection, login, limit):
    # Private work arrives as restrictedContributionsCount, with no repo names. If a
    # private repo is ever listed by name anyway, it is folded into that count so
    # its name cannot reach the public README.
    private = collection["restrictedContributionsCount"]
    rows = []
    for e in collection["commitContributionsByRepository"]:
        repo, count = e["repository"], e["contributions"]["totalCount"]
        if repo["isPrivate"]:
            private += count
            continue
        # Forks, this profile repo, and repos without code (org .github profiles, docs) aren't listed.
        if repo["isFork"] or repo["nameWithOwner"] == f"{login}/{login}" or repo["primaryLanguage"] is None:
            continue
        rows.append((repo, count))
    rows.sort(key=lambda p: (-p[1], p[0]["nameWithOwner"]))
    return rows[:limit], private


def render(rows, private, days):
    lines = []
    if rows:
        lines += [f"| Repository | Commits ({days}d) | About |", "|---|--:|---|"]
    for repo, count in rows:
        about = (repo["description"] or "").replace("|", "\\|").strip()
        lines.append(f"| [{repo['nameWithOwner']}]({repo['url']}) | {count} | {about} |")
    if private:
        lines += ["", f"Plus {private} contributions to private repositories."]
    return "\n".join(lines).strip() or f"_No activity in the last {days} days._"


def habits(times, tz):
    hours, weekdays = [0] * 24, [0] * 7
    for t in times:
        local = t.astimezone(tz)
        hours[local.hour] += 1
        weekdays[local.weekday()] += 1
    return hours, weekdays


def spark(counts):
    top = max(counts)
    if not top:
        return "·" * len(counts)
    # Zero gets its own glyph so a quiet hour can't be mistaken for a light one.
    return "".join("·" if c == 0 else SPARKS[(c * len(SPARKS) - 1) // top] for c in counts)


def render_habits(hours, weekdays, days, tz_name):
    total = sum(hours)
    if not total:
        return f"_No public commits in the last {days} days._"
    peak_hour = hours.index(max(hours))
    peak_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][weekdays.index(max(weekdays))]
    axis = "".join(f"{h:02d}  " for h in range(0, 24, 4)).rstrip()
    return "\n".join([
        "```text",
        f"hour  {axis}",
        f"      {spark(hours)}   peak {peak_hour:02d}:00",
        "",
        f"day   {' '.join(WEEKDAYS)}",
        f"      {' '.join(spark(weekdays))}   peak {peak_day}",
        "```",
        f"<sub>{total} public commits over the last {days} days, by author time in {tz_name}.</sub>",
    ])


def splice(readme, name, block):
    # Fail instead of appending: a README that lost its markers means someone
    # edited it by hand, and silently tacking a block onto the end hides that.
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    head, sep, rest = readme.partition(start)
    if not sep or end not in rest:
        raise ValueError(f"{name} markers missing from README")
    _, _, tail = rest.partition(end)
    return f"{head}{start}\n{block}\n{end}{tail}"


def main():
    login = os.environ.get("GH_LOGIN", "armantorkzaban")
    days = int(os.environ.get("ACTIVITY_DAYS", "90"))
    habit_days = int(os.environ.get("HABITS_DAYS", "365"))
    tz_name = os.environ.get("HABITS_TZ", "Europe/Berlin")
    token = os.environ["GH_TOKEN"]
    path = sys.argv[1] if len(sys.argv) > 1 else "README.md"

    rows, private = select(fetch(login, token, days)["contributionsCollection"], login, 6)
    year = fetch(login, token, habit_days)
    times = commit_times(token, year["id"], public_repos(year["contributionsCollection"]), habit_days)
    hours, weekdays = habits(times, ZoneInfo(tz_name))

    with open(path, encoding="utf-8") as f:
        readme = f.read()
    updated = splice(readme, "activity", render(rows, private, days))
    updated = splice(updated, "habits", render_habits(hours, weekdays, habit_days, tz_name))
    if updated != readme:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)


if __name__ == "__main__":
    main()
