#!/usr/bin/env python3
"""Download healthcare facility names from OSM via the Overpass API."""

import argparse
import overpy


def main(output_path: str) -> None:
    api = overpy.Overpass()

    query = """
    [out:json][timeout:180];
    area["ISO3166-1"="DE"][admin_level=2]->.de;
    (
      node["healthcare"](area.de);
      way["healthcare"](area.de);
      relation["healthcare"](area.de);
    );
    out body;
    """

    result = api.query(query)

    names = set()
    for elem in result.nodes + result.ways + result.relations:
        name = elem.tags.get("name")
        if name:
            names.add(name.strip())

    with open(output_path, "w", encoding="utf-8") as fh:
        for n in sorted(names):
            fh.write(n + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Output text file")
    args = parser.parse_args()
    main(args.output)
