import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpparser import ParsecPVJSON
import sys

sys1 = ParsecPVJSON('.\examples\SAT-tree.json')
#sys1.DetailOn()
sys1.Run()