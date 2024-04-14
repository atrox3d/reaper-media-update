from pathlib import Path
import os

from atrox3d.simplegit import git, repos


SCRIPT_DIR = Path(__file__).parent
JSON_PATH = SCRIPT_DIR / 'projects.json'

os.chdir(SCRIPT_DIR)
BASE_DIR = '..'

repos.backup(BASE_DIR, json_path=JSON_PATH, recurse=True)