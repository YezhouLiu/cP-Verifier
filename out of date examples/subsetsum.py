from compoundterm import CPTerm
from compoundrule import CPRule
from compoundcpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
import sys
#sys.stdout = open('out.txt', 'w')

def CPSubsetSum(original_set, target_number): #{1,2,3,4}, 10
    rule1 = ParseRule('s0 ->1 s1 p(u()n(M)s()) | m(M)')
    rule2 = ParseRule('s1 ->1 s2 o(X) | p(u(X)s(T)A)) t(T)')
    rule3 = ParseRule('s1 ->1 s3 o() | p(n()A)')
    rule4 = ParseRule('s1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))')
    rule5 = ParseRule('s1 p(A) ->+ s1')

    #system
    #t = ParseTerm('t(10)'), when target_number = 10
    t = ParseTerm('t('+str(target_number)+')')
    string_m = 'm('
    for i in original_set:
        string_m += 'm(' + str(i) + ')'
    string_m += ')'
    #m = ParseTerm('m(m(1)m(2)m(3)m(4))'), when original_set = {1,2,3,4}
    m = ParseTerm(string_m)

    sys = CPSystem('s0')
    sys.AddRule(rule1)
    sys.AddRule(rule2)
    sys.AddRule(rule3)
    sys.AddRule(rule4)
    sys.AddRule(rule5)
    sys.AddTerm(t)
    sys.AddTerm(m)

    #Initial state of the cP system
    sys.SystemSnapshot()
    #sys.Run()
    sys.RunProfile() #if use this, need to run: python -m memory_profiler subsetsum_fullparser.py

#sys.stdout = open('subsetsum.txt', 'w')
CPSubsetSum({1,2,3},6)
#CPSubsetSum({1,2,3,4},10)
#CPSubsetSum({1,2,3,4},11)
#sys.stdout = open('6.txt', 'w')
#CPSubsetSum({1,2,3,4,5,6},21)
#CPSubsetSum({1,2,3,4,5,6},22)
#sys.stdout = open('8.txt', 'w')
#CPSubsetSum({1,2,3,4,5,6,7,8},36)
#sys.stdout = open('10.txt', 'w')
#CPSubsetSum({1,2,3,4,5,6,7,8,9,10},55)
