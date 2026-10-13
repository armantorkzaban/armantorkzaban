"""Replace a marked README block with stdin: splice.py NAME README.md < block"""

import sys


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
    name, path = sys.argv[1], sys.argv[2]
    with open(path, encoding="utf-8") as f:
        readme = f.read()
    updated = splice(readme, name, sys.stdin.read().rstrip("\n"))
    if updated != readme:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)


if __name__ == "__main__":
    main()
