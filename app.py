
import streamlit as st
import importlib.util
import sys
from pathlib import Path

# Load and execute the home.py file
def load_home_page():
    home_path = Path("home.py")
    if home_path.exists():
        spec = importlib.util.spec_from_file_location("home", home_path)
        home_module = importlib.util.module_from_spec(spec)
        sys.modules["home"] = home_module
        spec.loader.exec_module(home_module)
    else:
        st.error("home.py file not found!")

if __name__ == "__main__":
    load_home_page()
