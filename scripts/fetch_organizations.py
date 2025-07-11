#!/usr/bin/env python3
"""Download organization names (office, shop, craft, club, industrial) from OSM."""

import argparse
import overpy

TAGS = ["office", "shop", "craft", "club", "industrial"]


def main(output_path: str) -> None:
    api = overpy.Overpass()

    query = """
    [out:json];
    area["ISO3166-1"="DE"][admin_level=2]->.de;
    (
"""
    for tag in TAGS:
        query += f"  node[\"{tag}\"][\"name\"](area.de);\n"
    query += ")\nout tags;"

    result = api.query(query)

    names = set()
    for node in result.nodes:
        name = node.tags.get("name")
        if name and name.lower() != "no name":
            names.add(name.strip())

    with open(output_path, "w", encoding="utf-8") as fh:
        for n in sorted(names):
            fh.write(n + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Output text file")
    args = parser.parse_args()
    main(args.output)
