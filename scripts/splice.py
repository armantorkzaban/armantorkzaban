"""Replace a marked README block with stdin: splice.py NAME README.md < block"""

import sys

from activity import splice

name, path = sys.argv[1], sys.argv[2]
with open(path, encoding="utf-8") as f:
    readme = f.read()
updated = splice(readme, name, sys.stdin.read().rstrip("\n"))
if updated != readme:
    with open(path, "w", encoding="utf-8") as f:
        f.write(updated)
