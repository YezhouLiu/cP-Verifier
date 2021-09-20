import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpsystem import CPSystem
from cpparser import ParseRule

rule1 = ParseRule('s1 a b ->+ s1 b')
rule2 = ParseRule('s1 b ->+ s1 a')

sys1 = CPSystem('s1')
sys1.AddRuleset([rule1, rule2])

ms1 = {'a': 144, 'b': 88}
sys1.AddSystemMultiset(ms1)
sys1.DetailOn()

sys1.Snapshot()
sys1.Run()