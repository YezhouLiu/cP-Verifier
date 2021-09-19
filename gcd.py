from term import Term
from rule import Rule
from cpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
import sys
#sys.stdout = open('out.txt', 'w')

rule1 = ParseRule('s1 a(XY1) ->+ s1 a(Y1) | a(X)')
rule2 = ParseRule('s1 a(X) a(X) ->1 s2 b(X)')

sys1 = CPSystem('s1')
sys1.AddRule(rule1)
sys1.AddRule(rule2)

sys1.AddSystemTerm(ParseTerm('a(144)'))
sys1.AddSystemTerm(ParseTerm('a(88)'))
sys1.DetailOn()

sys1.Snapshot()
sys1.Run()