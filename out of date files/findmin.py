from compoundterm import CPTerm
from compoundrule import CPRule
from compoundcpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule

rule1 = ParseRule('s1 ->+ s2 b(X) | a(X)')
rule2 = ParseRule('s2 b(XY1) ->+ s3 | a(X)')

sys1 = CPSystem('s1')
sys1.AddRule(rule1)
sys1.AddRule(rule2)

sys1.AddTerm(ParseTerm('a(7)'))
sys1.AddTerm(ParseTerm('a(19)'))
sys1.AddTerm(ParseTerm('a(11)'))
sys1.AddTerm(ParseTerm('a(87)'))
sys1.AddTerm(ParseTerm('a(7)'))

sys1.SystemSnapshot()
sys1.Run()