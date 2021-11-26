import os, sys
from typing import OrderedDict
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
from cpverifier import CPVerifier

def CPSubsetSum(original_set, target_number):
    #rule0 = ParseRule('s0 ->1 s4')
    rule1 = ParseRule('s0 ->1 s1 p(u()n(M)s()) | m(M)')
    rule2 = ParseRule('s1 ->1 s2 o(X) | p(u(X)s(T)A)) t(T)')
    rule3 = ParseRule('s1 ->1 s3 o() | p(n()A)')
    rule4 = ParseRule('s1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))')
    rule5 = ParseRule('s1 p(A) ->+ s1')

    #system
    t = ParseTerm('t('+str(target_number)+')')
    string_m = 'm('
    for i in original_set:
        string_m += 'm(' + str(i) + ')'
    string_m += ')'
    m = ParseTerm(string_m)

    sys = CPSystem('s0')
    #sys.AddRule(rule0)
    sys.AddRule(rule1)
    sys.AddRule(rule2)
    sys.AddRule(rule3)
    sys.AddRule(rule4)
    sys.AddRule(rule5)
    sys.AddSystemTerm(t)
    sys.AddSystemTerm(m)
    #sys.DetailOn()

    #Initial state of the cP syst em
    #sys.Snapshot()
    #sys.Run()
    #print(sys.ToString())
    
    cpv = CPVerifier(sys)
    cpv.SetSearchMethod('BFS')
    cpv.SetTerminations(['s2','s3'])
    cpv.SetGoalTerms({ParseTerm('o(m(2)m(3))'):1})
    cpv.SetGoalState('s2')
    cpv.Verify(0)
    
CPSubsetSum({1,2,3},5)

