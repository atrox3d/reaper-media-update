import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))
print(sys.path)
from python_argparse import main

main.main()

