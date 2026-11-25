"""Reproducible local experiment; does not write to cloud services."""
import os
os.environ['FIREBASE_ENABLED'] = 'false'
import sys, json, csv, hashlib, platform, importlib.metadata
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import networkx as nx
from app.models.benchmark import BenchmarkRequest
from app.services import benchmark_service as service
from app.services.dataset_service import get_graph

out = Path(__file__).resolve().parents[2] / 'artifacts' / 'bab5'
out.mkdir(parents=True, exist_ok=True)
request = BenchmarkRequest(datasetId='kota-bandung-osm-drive', testCaseCount=10,
    pairMode='random', repeatCount=3, warmupRuns=1, randomSeed=42, tolerance=1e-9)
graph = get_graph(request.dataset_id)
pairs = service.build_test_cases(graph, request)
dataset_path = Path(__file__).resolve().parents[1] / 'app/data/datasets/kota-bandung-osm-drive.json'
manifest = {'startedAt': datetime.now(timezone.utc).isoformat(),
    'request': request.model_dump(by_alias=True),
    'pairs': [p.model_dump(by_alias=True) for p in pairs],
    'datasetSha256': hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
    'platform': platform.platform(), 'python': sys.version,
    'versions': {p: importlib.metadata.version(p) for p in ['fastapi','uvicorn','networkx','osmnx','firebase-admin']},
    'order': 'standard then optimized; fixed order', 'persistence': 'memory; local JSON and CSV export'}
(out/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
original = service.dijkstra_standard
counter = 0
def logged(*args, **kwargs):
    global counter
    result = original(*args, **kwargs)
    counter += 1
    print(f'Standard call {counter}/40: {result.execution_time_ms:.2f} ms', flush=True)
    return result
service.dijkstra_standard = logged
response = service.run_benchmark(request)
payload = response.model_dump(mode='json', by_alias=True)
(out/'benchmark.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
rows = payload['runs']
with (out/'raw-runs.csv').open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows([{**r, 'path': json.dumps(r['path'])} for r in rows])
reference = nx.MultiDiGraph()
reference.add_nodes_from(graph.node_ids)
for u, neighbors in graph.adjacency.items():
    for v, weight in neighbors:
        reference.add_edge(u, v, weight=weight)
checks = []
for pair in pairs:
    try:
        expected = nx.shortest_path_length(reference, pair.source_id, pair.destination_id, weight='weight', method='dijkstra')
    except nx.NetworkXNoPath:
        expected = None
    matching = [r for r in rows if r['sourceId']==pair.source_id and r['destinationId']==pair.destination_id]
    valid = True
    for r in matching:
        if expected is None:
            valid &= r['status']=='unreachable' and not r['path'] and r['totalCost'] is None
        else:
            path = r['path']
            valid &= bool(path) and path[0]==pair.source_id and path[-1]==pair.destination_id
            path_cost = 0.0
            for u,v in zip(path, path[1:]):
                weights = [w for n,w in graph.adjacency[u] if n==v]
                if not weights:
                    valid = False
                    break
                path_cost += min(weights)
            valid &= r['status']=='success' and abs(r['totalCost']-expected)<=request.tolerance and abs(path_cost-expected)<=request.tolerance
    checks.append({'sourceId':pair.source_id, 'destinationId':pair.destination_id,
        'referenceCost':expected, 'valid':bool(valid), 'runCount':len(matching)})
(out/'correctness.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
manifest['finishedAt'] = datetime.now(timezone.utc).isoformat()
(out/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(payload['summary'], indent=2), flush=True)
assert all(c['valid'] for c in checks)
