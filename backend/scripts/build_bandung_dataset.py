"""Build the research dataset from the verified Kota Bandung OSM boundary."""
import csv
import hashlib
import json
import platform
from pathlib import Path

import geopandas as gpd
import networkx as nx
import osmnx as ox

from build_osm_dataset import convert_graph

root = Path(__file__).resolve().parents[2]
out = root / 'artifacts' / 'kota-bandung'
out.mkdir(parents=True, exist_ok=True)
boundary = gpd.read_file(root / 'artifacts' / 'kota-bandung-boundary.geojson')
assert int(boundary.iloc[0]['osm_id']) == 13290062
ox.settings.use_cache = True
ox.settings.cache_folder = root / 'backend' / 'cache'
ox.settings.requests_timeout = 180
print('Downloading Kota Bandung drive network...', flush=True)
graph = ox.graph_from_polygon(boundary.geometry.iloc[0], network_type='drive', simplify=True, retain_all=True, truncate_by_edge=False)
ox.save_graphml(graph, out / 'network.graphml')
dataset = convert_graph(graph, dataset_id='kota-bandung-osm-drive', version='1.0.0', place='Kota Bandung, Jawa Barat, Indonesia', network_type='drive')
path = root / 'backend/app/data/datasets/kota-bandung-osm-drive.json'
path.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding='utf-8')
for key in ('nodes', 'edges'):
    with (out / f'{key}.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(dataset[key][0]))
        writer.writeheader()
        writer.writerows(dataset[key])
import sys
sys.path.insert(0, str(root / 'backend'))
from app.models.graph import GraphDataset
GraphDataset.model_validate(dataset)
report = dict(datasetId=dataset['id'], extractedAt=dataset['extractedAt'], boundaryRelation=13290062, boundaryName=boundary.iloc[0]['display_name'], nodeCount=len(dataset['nodes']), directedEdgeCount=len(dataset['edges']), weakComponents=nx.number_weakly_connected_components(graph), strongComponents=nx.number_strongly_connected_components(graph), simplify=True, retainAll=True, truncateByEdge=False, networkType='drive', weightUnit='meter', osmnx=ox.__version__, python=platform.python_version(), sha256=hashlib.sha256(path.read_bytes()).hexdigest(), validation='Passed GraphDataset schema, unique IDs, finite nonnegative weights and endpoint references', attribution='© OpenStreetMap contributors', licenseUrl='https://www.openstreetmap.org/copyright')
(out / 'metadata.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
