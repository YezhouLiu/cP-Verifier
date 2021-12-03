import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpparser import ParseSystem
from cpparser import ParseTerm
from cpverifier import CPVerifier

ruleset = ['s1 v(v(R)Y) ->1 s2 s(r(R)u(Y)p(h(R)p()))',
           's2 s(r(R)u()p(h(F)p(P))) ->+ s3 z(p(h(R)p(h(F)p(P)))) | e(f(F)t(R))',
           's2 ->+ s2 s(r(R)u(Z)p(h(T)p(h(F)p(P)))) | s(r(R)u(v(T)Z)p(h(F)p(P))) e(f(F)t(T))',
           's2 s(A) ->+ s2',
           's3 ->1 s4 q(P) | z(p(P))']
system_terms = {'e(f(1)t(2))': 1, 'e(f(2)t(5))': 1, 
                'e(f(5)t(4))': 1, 'e(f(3)t(4))': 1,
                'e(f(4)t(3))': 1, 'e(f(3)t(6))': 1,
                'e(f(6)t(1))': 1, 'v(v(1)v(2)v(3)v(4)v(5)v(6))': 1}
system_state = 's1'
system_name = 'HCP' #optional

#The example graph, 6 vertices:
#1->2 2->5 5->4 3->4 4->3 3->6 6->1

sys1 = ParseSystem(ruleset, system_terms, system_state, system_name)
#sys1.DetailOn()
#sys1.Snapshot()
#sys1.Run()

cpv = CPVerifier(sys1)
cpv.SetTerminations(['s4','s3'])
cpv.SetTargetTerms({ParseTerm('o(m(2)m(3))'):1})
cpv.SetTargetState('s3')
cpv.Verify(9)

