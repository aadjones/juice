# tests/test_storage.py
from pathlib import Path
import tempfile
import importlib, modules
import pandas as pd
import streamlit as st

def _reload_with_tmp(monkeypatch, tmp):
    monkeypatch.setenv("DATA_DIR", tmp)
    # replace the proxy with a plain dict *before* re‑importing storage
    monkeypatch.setattr(st, "session_state", {}, raising=False)
    return importlib.reload(modules.storage)

def test_path_routing_demo_vs_nick(monkeypatch):
    tmp = tempfile.mkdtemp()
    storage = _reload_with_tmp(monkeypatch, tmp)

    assert storage._path().name == "demo.csv"

    storage.st.session_state["nickname"] = "alice"
    assert storage._path().name == "alice.csv"

def test_upsert_creates_file(monkeypatch):
    tmp = tempfile.mkdtemp()
    storage = _reload_with_tmp(monkeypatch, tmp)

    storage.st.session_state["nickname"] = "bob"
    storage.upsert_entry(pd.Timestamp("2025-05-19"), 5, 4, "")

    assert (Path(tmp) / "bob.csv").exists()
