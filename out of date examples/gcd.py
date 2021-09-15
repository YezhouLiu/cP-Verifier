from compoundterm import CPTerm
from compoundrule import CPRule
from compoundcpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule

rule1 = ParseRule('s1 a(XY1) ->+ s1 a(Y1) | a(X)')
rule2 = ParseRule('s1 a(X) a(X) ->1 s2 b(X)')

sys1 = CPSystem('s1')
sys1.AddRule(rule1)
sys1.AddRule(rule2)

sys1.AddTerm(ParseTerm('a(144)'))
sys1.AddTerm(ParseTerm('a(88)'))

sys1.SystemSnapshot()
sys1.Run()