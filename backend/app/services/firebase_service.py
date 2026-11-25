"""Optional Firestore persistence for benchmark experiments.

The routing graph and algorithm timing stay in memory. Firestore is used only
after a benchmark has completed, so database/network latency is not included
in the algorithm metrics.
"""

from __future__ import annotations

import logging
import json
import os
from pathlib import Path
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

from app.models.benchmark import (
    BenchmarkResponse,
    ExperimentHistoryItem,
)


logger = logging.getLogger(__name__)

BACKEND_DIRECTORY = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIRECTORY / ".env")

_firestore_client: firestore.Client | None = None
_initialization_attempted = False
_initialization_error: str | None = None


def _is_enabled() -> bool:
    return os.getenv("FIREBASE_ENABLED", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _collection_name() -> str:
    return os.getenv("FIREBASE_EXPERIMENT_COLLECTION", "experiments").strip() or "experiments"


def _initialize_client() -> firestore.Client | None:
    global _firestore_client, _initialization_attempted, _initialization_error

    if _initialization_attempted:
        return _firestore_client

    _initialization_attempted = True
    if not _is_enabled():
        _initialization_error = "FIREBASE_ENABLED belum diaktifkan"
        return None

    try:
        if not firebase_admin._apps:
            project_id = os.getenv("FIREBASE_PROJECT_ID", "").strip()
            options: dict[str, Any] = {"projectId": project_id} if project_id else {}
            service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
            credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
            if service_account_json:
                firebase_admin.initialize_app(
                    credentials.Certificate(json.loads(service_account_json)),
                    options=options,
                )
            elif credential_path:
                firebase_admin.initialize_app(
                    credentials.Certificate(credential_path),
                    options=options,
                )
            else:
                firebase_admin.initialize_app(options=options)

        _firestore_client = firestore.client()
        return _firestore_client
    except Exception as error:  # Firebase errors must not break local fallback mode.
        _initialization_error = str(error)
        logger.warning("Firebase Firestore tidak tersedia; memakai memory fallback: %s", error)
        return None


def get_firestore_status() -> dict[str, str | bool]:
    client = _initialize_client()
    if client is not None:
        return {
            "enabled": True,
            "connected": True,
            "mode": "firestore",
            "message": "Firestore aktif",
        }
    return {
        "enabled": _is_enabled(),
        "connected": False,
        "mode": "memory",
        "message": _initialization_error or "Firebase belum dikonfigurasi",
    }


def _summary_data(response: BenchmarkResponse) -> dict[str, Any]:
    return response.summary.model_dump(by_alias=True, mode="json")


def save_benchmark(response: BenchmarkResponse) -> bool:
    client = _initialize_client()
    if client is None:
        return False

    try:
        collection = client.collection(_collection_name())
        experiment_id = response.summary.experiment_id
        collection.document(experiment_id).set(_summary_data(response))

        runs_collection = collection.document(experiment_id).collection("runs")
        # Firestore batches are limited; use small chunks so larger experiments
        # remain persistable without changing the benchmark API contract.
        runs = response.runs
        for start in range(0, len(runs), 400):
            batch = client.batch()
            for run in runs[start : start + 400]:
                batch.set(
                    runs_collection.document(run.id),
                    run.model_dump(by_alias=True, mode="json"),
                )
            batch.commit()
        return True
    except Exception as error:
        logger.warning("Gagal menyimpan eksperimen ke Firestore: %s", error)
        return False


def _run_sort_key(run_data: dict[str, Any]) -> int:
    try:
        return int(str(run_data.get("id", "")).rsplit("-", 1)[-1])
    except (TypeError, ValueError):
        return 0


def get_benchmark(experiment_id: str) -> BenchmarkResponse | None:
    client = _initialize_client()
    if client is None:
        return None

    try:
        collection = client.collection(_collection_name())
        snapshot = collection.document(experiment_id).get()
        if not snapshot.exists:
            return None
        summary = snapshot.to_dict() or {}
        runs = [
            run_snapshot.to_dict() or {}
            for run_snapshot in collection.document(experiment_id)
            .collection("runs")
            .stream()
        ]
        runs.sort(key=_run_sort_key)
        return BenchmarkResponse.model_validate({"summary": summary, "runs": runs})
    except Exception as error:
        logger.warning("Gagal membaca eksperimen dari Firestore: %s", error)
        return None


def get_experiment_history() -> list[ExperimentHistoryItem] | None:
    client = _initialize_client()
    if client is None:
        return None

    try:
        snapshots = (
            client.collection(_collection_name())
            .order_by("createdAt", direction=firestore.Query.DESCENDING)
            .limit(100)
            .stream()
        )
        return [
            ExperimentHistoryItem.model_validate(snapshot.to_dict() or {})
            for snapshot in snapshots
        ]
    except Exception as error:
        logger.warning("Gagal membaca riwayat Firestore: %s", error)
        return None
