"""
http://docs.python-guide.org/en/latest/writing/structure
"""
import sys
import site
from pathlib import Path
this_dir=Path(__file__).resolve().parent
sys.path.insert(0, str(this_dir))
sep='*'*30
print(f'{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n{sys.path[1]}\n{sep}\n')
site.removeduppaths()

