import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpsystem import CPSystem
from cpparser import ParseTerms
from cpparser import ParseRule

rule1 = ParseRule('s1 ->+ s2 b(X) | a(X)')
rule2 = ParseRule('s2 b(XY1) ->+ s3 | a(X)')

sys1 = CPSystem('s1')
sys1.AddRule(rule1)
sys1.AddRule(rule2)
sys1.AddSystemMultiset(ParseTerms('a(7) a(11) a(9) a(8) a(10)'))
sys1.SetDetailLevel(2)

sys1.Snapshot()
sys1.Run()