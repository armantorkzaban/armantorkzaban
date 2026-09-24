"""Rewrite the activity block in README.md from the GitHub GraphQL API."""

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com/graphql"
START = "<!-- activity:start -->"
END = "<!-- activity:end -->"

QUERY = """
query($login: String!, $from: DateTime!) {
  user(login: $login) {
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


def fetch(login, token, days):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    body = json.dumps({"query": QUERY, "variables": {"login": login, "from": since.isoformat()}})
    req = urllib.request.Request(
        API, data=body.encode(), headers={"Authorization": f"bearer {token}"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]["contributionsCollection"]


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


def splice(readme, block):
    # Fail instead of appending: a README that lost its markers means someone
    # edited it by hand, and silently tacking a table onto the end hides that.
    head, sep, rest = readme.partition(START)
    if not sep or END not in rest:
        raise ValueError("activity markers missing from README")
    _, _, tail = rest.partition(END)
    return f"{head}{START}\n{block}\n{END}{tail}"


def main():
    login = os.environ.get("GH_LOGIN", "armantorkzaban")
    days = int(os.environ.get("ACTIVITY_DAYS", "90"))
    token = os.environ["GH_TOKEN"]
    path = sys.argv[1] if len(sys.argv) > 1 else "README.md"

    rows, private = select(fetch(login, token, days), login, 6)
    with open(path, encoding="utf-8") as f:
        readme = f.read()
    updated = splice(readme, render(rows, private, days))
    if updated != readme:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)


if __name__ == "__main__":
    main()
