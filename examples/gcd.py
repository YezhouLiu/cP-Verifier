import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpparser import ParsecPVJSON
import sys
import json

sys1 = ParsecPVJSON('./examples/gcd2.json')
sys1.SetDetailLevel(2)
sys1.Run()