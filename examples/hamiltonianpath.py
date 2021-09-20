import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
import sys

rule1 = ParseRule('s1 v(v(R)Y) ->1 s2 s(u(Y)p(h(R)p()))')
rule2 = ParseRule('s2 ->1 s3 q(P) | s(u()p(P))')
rule3 = ParseRule('s2 ->+ s2 s(u(Z)p(h(T)p(h(F)p(P)))) | s(u(v(T)Z)p(h(F)p(P)))')
rule4 = ParseRule('s2 s(A) ->+ s2')

sys1 = CPSystem('s1')
sys1.AddRuleset([rule1, rule2, rule3, rule4])
sys1.DetailOn()
size = 4

for i in range(1, size):
    for j in range(1, size):
        temp_term = ParseTerm('e(f(' + str(i) + ')t(' + str(j) + '))')
        sys1.AddSystemTerm(temp_term)

sys1.AddSystemTerm(ParseTerm('v(v(1)v(2)v(3)v(4))'))
sys1.Snapshot()
sys1.Run()