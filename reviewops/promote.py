"""Atomically promote a locally validated model bundle; no registry credentials."""

import json
import shutil
import tempfile
from pathlib import Path

from .pipeline import predict


def promote(candidate, registry, minimum_f1=0.6):
    candidate, registry = Path(candidate), Path(registry)
    report = json.loads((candidate / "metrics.json").read_text())
    if not 0 <= minimum_f1 <= 1:
        raise ValueError("minimum_f1 must be in [0,1]")
    predict(candidate / "model.joblib", ["integrity check"])
    if report["test_macro_f1"] < minimum_f1:
        return False
    version = report["model_sha256"]
    registry.mkdir(parents=True, exist_ok=True)
    target = registry / version
    if not target.exists():
        with tempfile.TemporaryDirectory(dir=registry) as temp:
            bundle = Path(temp) / "bundle"
            shutil.copytree(candidate, bundle)
            bundle.rename(target)
    pointer = registry / "champion.tmp"
    pointer.write_text(json.dumps({"version": version, "path": str(target)}))
    pointer.replace(registry / "champion.json")
    return True
