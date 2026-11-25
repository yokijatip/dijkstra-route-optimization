from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_firebase_status_endpoint():
    response = client.get("/api/firebase/status")

    assert response.status_code == 200
    assert response.json()["mode"] in {"memory", "firestore"}


def test_compare_endpoint():
    response = client.post(
        "/api/routes/compare",
        json={
            "datasetId": "small-demo",
            "sourceId": "soreang",
            "destinationId": "baleendah",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["correctnessMatch"] is True
    assert payload["standard"]["totalCost"] == payload["optimized"]["totalCost"]


def test_unknown_node_returns_validation_error():
    response = client.post(
        "/api/routes/standard",
        json={
            "sourceId": "unknown",
            "destinationId": "baleendah",
        },
    )

    assert response.status_code == 422


def test_dataset_list_and_benchmark_endpoint():
    datasets_response = client.get("/api/datasets")
    assert datasets_response.status_code == 200
    assert "small-demo" in {dataset["id"] for dataset in datasets_response.json()}

    benchmark_response = client.post(
        "/api/benchmarks",
        json={
            "datasetId": "small-demo",
            "testCaseCount": 2,
            "pairMode": "preset",
            "repeatCount": 1,
            "warmupRuns": 0,
        },
    )

    assert benchmark_response.status_code == 201
    payload = benchmark_response.json()
    assert payload["summary"]["testCaseCount"] == 2
    assert payload["summary"]["correctnessMismatchCount"] == 0
    assert len(payload["runs"]) == 4

    experiment_id = payload["summary"]["experimentId"]
    csv_response = client.get(f"/api/experiments/{experiment_id}/export.csv")
    assert csv_response.status_code == 200
    assert "executionTimeNs" in csv_response.text.splitlines()[0]
