import os, shutil, tempfile
import pandas as pd
from pathlib import Path
import importlib
from modules import storage

def test_path_routing_demo_vs_nick(monkeypatch):
    tmp = tempfile.mkdtemp()
    monkeypatch.setenv("DATA_DIR", tmp)

    # demo path
    storage.st.session_state.clear()
    assert storage._path().name == "demo.csv"

    # nickname path
    storage.st.session_state["nickname"] = "alice"
    assert storage._path().name == "alice.csv"

    shutil.rmtree(tmp)

def test_upsert_creates_file(monkeypatch):
    import importlib, modules
    tmp = tempfile.mkdtemp()
    monkeypatch.setenv("DATA_DIR", tmp)

    # reload storage so it picks up new DATA_DIR
    storage = importlib.reload(modules.storage)

    storage.st.session_state["nickname"] = "bob"
    storage.upsert_entry(pd.Timestamp("2025-05-19"), 5, 4, "")

    assert (Path(tmp) / "bob.csv").exists()
    
    shutil.rmtree(tmp)
