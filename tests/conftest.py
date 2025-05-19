# tests/conftest.py
import types, sys

import streamlit as st

if not hasattr(st, "session_state"):
    st.session_state = {}  # plain dict is enough for unit tests
