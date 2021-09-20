from typing import OrderedDict
from term import Term
from rule import Rule
from cpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
import sys
#sys.stdout = open('out.txt', 'w')

rule1 = ParseRule('s1 a b ->+ s1 b')
rule2 = ParseRule('s1 b ->+ s1 a')

sys1 = CPSystem('s1')
sys1.AddRule(rule1)
sys1.AddRule(rule2)

ms1 = {'a': 144, 'b': 88}
sys1.AddSystemMultiset(ms1)
sys1.DetailOn()

sys1.Snapshot()
sys1.Run()