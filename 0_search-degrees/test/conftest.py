import os
import sys
from pathlib import Path

project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))
os.chdir(project_dir)
