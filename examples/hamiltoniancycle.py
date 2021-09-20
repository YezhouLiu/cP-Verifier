import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpsystem import CPSystem
from cpparser import ParseTerms
from cpparser import ParseRule
import sys

rule1 = ParseRule('s1 v(v(R)Y) ->1 s2 s(r(R)u(Y)p(h(R)p()))')
rule2 = ParseRule('s2 s(r(R)u()p(h(F)p(P))) ->+ s3 z(p(h(R)p(h(F)p(P)))) | e(f(F)t(R))')
rule3 = ParseRule('s2 ->+ s2 s(r(R)u(Z)p(h(T)p(h(F)p(P)))) | s(r(R)u(v(T)Z)p(h(F)p(P))) e(f(F)t(T))')
rule4 = ParseRule('s2 s(A) ->+ s2')
rule5 = ParseRule('s3 ->1 s4 q(P) | z(p(P))')

sys1 = CPSystem('s1')
sys1.AddRuleset([rule1, rule2, rule3, rule4, rule5])

sys1.AddSystemMultiset(ParseTerms('e(f(1)t(2)) e(f(2)t(5)) e(f(5)t(4)) e(f(3)t(4)) e(f(4)t(3)) e(f(3)t(6)) e(f(6)t(1)) v(v(1)v(2)v(3)v(4)v(5)v(6))'))
#The example graph, 6 vertices:
#1->2 2->5 5->4 3->4 4->3 3->6 6->1

sys1.DetailOn()

sys1.Snapshot()
sys1.Run()


