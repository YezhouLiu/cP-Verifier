import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpparser import ParsecPVJSON
import sys
import json

sys1 = ParsecPVJSON('gcd.json')
sys1.DetailOn()
sys1.Run()