"""Convert an OpenStreetMap street network into the project's JSON graph format.

This script is an offline preprocessing step. The FastAPI benchmark never calls
OpenStreetMap or NetworkX to calculate a route; it only loads the generated JSON
into memory and runs the project's own algorithms.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import osmnx as ox


BACKEND_DIRECTORY = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIRECTORY = BACKEND_DIRECTORY / "app" / "data" / "datasets"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and convert an OSM street network to graph JSON."
    )
    parser.add_argument(
        "--place",
        required=True,
        help="Place name understood by OpenStreetMap Nominatim.",
    )
    parser.add_argument(
        "--dataset-id",
        required=True,
        help="Dataset id and output filename stem, for example kab-bandung-small.",
    )
    parser.add_argument(
        "--version",
        default="1.0.0",
        help="Dataset version recorded in the generated JSON.",
    )
    parser.add_argument(
        "--network-type",
        default="drive",
        choices=["all", "all_public", "bike", "drive", "drive_service", "walk"],
        help="OSMnx network type to download.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path. Defaults to app/data/datasets/{dataset-id}.json.",
    )
    parser.add_argument(
        "--retain-all",
        action="store_true",
        help="Keep all weakly connected components instead of the largest one.",
    )
    parser.add_argument(
        "--no-simplify",
        action="store_true",
        help="Keep raw geometry nodes. Usually not recommended for routing research.",
    )
    return parser.parse_args()


def convert_graph(
    graph: Any,
    *,
    dataset_id: str,
    version: str,
    place: str,
    network_type: str,
) -> dict[str, Any]:
    nodes = []
    for node_id, data in graph.nodes(data=True):
        longitude = data.get("x")
        latitude = data.get("y")
        if longitude is None or latitude is None:
            raise ValueError(f"Node {node_id} tidak memiliki koordinat x/y")
        nodes.append(
            {
                "id": str(node_id),
                "name": f"Intersection {node_id}",
                "latitude": float(latitude),
                "longitude": float(longitude),
            }
        )

    edges = []
    for source, target, _key, data in graph.edges(keys=True, data=True):
        length = data.get("length")
        if length is None:
            raise ValueError(f"Edge {source}->{target} tidak memiliki length")
        edges.append(
            {
                "from": str(source),
                "to": str(target),
                "weight": float(length),
                # OSMnx already represents one-way and two-way roads as
                # directed edges. Do not turn every edge into a two-way edge.
                "bidirectional": False,
            }
        )

    extracted_at = datetime.now(timezone.utc).isoformat()
    return {
        "id": dataset_id,
        "name": f"{place} - {network_type}",
        "version": version,
        "description": (
            f"Jaringan jalan {network_type} dari OpenStreetMap untuk wilayah {place}. "
            "Dataset diproses offline sebelum dimuat ke backend."
        ),
        "source": "OpenStreetMap",
        "region": place,
        "networkType": network_type,
        "weightUnit": "meter",
        "extractedAt": extracted_at,
        "attribution": "\u00a9 OpenStreetMap contributors",
        "nodes": nodes,
        "edges": edges,
    }


def main() -> None:
    arguments = parse_arguments()
    output_path = arguments.output or (
        DEFAULT_OUTPUT_DIRECTORY / f"{arguments.dataset_id}.json"
    )
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    ox.settings.use_cache = True
    ox.settings.log_console = False
    ox.settings.requests_timeout = 180

    print(f"Mengambil jaringan {arguments.network_type}: {arguments.place}")
    graph = ox.graph.graph_from_place(
        arguments.place,
        network_type=arguments.network_type,
        simplify=not arguments.no_simplify,
        retain_all=arguments.retain_all,
    )
    dataset = convert_graph(
        graph,
        dataset_id=arguments.dataset_id,
        version=arguments.version,
        place=arguments.place,
        network_type=arguments.network_type,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as dataset_file:
        json.dump(dataset, dataset_file, ensure_ascii=False, indent=2)
        dataset_file.write("\n")

    print(f"Dataset tersimpan: {output_path}")
    print(f"Nodes: {len(dataset['nodes'])}")
    print(f"Edges: {len(dataset['edges'])}")


if __name__ == "__main__":
    main()
