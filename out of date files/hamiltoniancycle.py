from compoundterm import CPTerm
from compoundrule import CPRule
from compoundcpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
import sys

rule1 = ParseRule('s1 v(v(R)Y) ->1 s2 s(r(R)u(Y)p(h(R)p()))')
rule2 = ParseRule('s2 s(r(R)u()p(h(F)p(P))) ->+ s3 z(p(h(R)p(h(F)p(P)))) | e(f(F)t(R))')
rule3 = ParseRule('s2 ->+ s2 s(r(R)u(Z)p(h(T)p(h(F)p(P)))) | s(r(R)u(v(T)Z)p(h(F)p(P))) e(f(F)t(T))')
rule4 = ParseRule('s2 s(A) ->+ s2')
rule5 = ParseRule('s3 ->1 s4 q(P) | z(p(P))')

sys1 = CPSystem('s1')
sys1.AddRule(rule1)
sys1.AddRule(rule2)
sys1.AddRule(rule3)
sys1.AddRule(rule4)
sys1.AddRule(rule5)

size = 5
#size = 6
#size = 7
for i in range(1,size):
    for j in range(1,size):
        temp_term = ParseTerm('e(f(' + str(i) + ')t(' + str(j) + '))')
        sys1.AddTerm(temp_term)

#sys.stdout = open('4.txt', 'w')
#sys.stdout = open('5.txt', 'w')
#sys.stdout = open('6.txt', 'w')

sys1.AddTerm(ParseTerm('v(v(1)v(2)v(3)v(4))'))
#sys1.AddTerm(ParseTerm('v(v(1)v(2)v(3)v(4)v(5))'))
#sys1.AddTerm(ParseTerm('v(v(1)v(2)v(3)v(4)v(5)v(6))'))

sys1.SystemSnapshot()
sys1.Run()
#sys1.RunProfile()