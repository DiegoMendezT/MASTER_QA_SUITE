# BACKUP: ui/controls.py
# This is a backup of the original file before deletion.
# ---
import os
import subprocess
import sys
import streamlit as st
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.task_prioritizer import Task, prioritize, _load_tasks
# ...existing code from controls.py...

