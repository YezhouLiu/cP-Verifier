from term import Term
from rule import Rule
from cpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
import sys
#sys.stdout = open('out.txt', 'w')

def CPSubsetSum(original_set, target_number): 
    rule4 = ParseRule('s1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))')
    #system
    t = ParseTerm('t('+str(target_number)+')')
    string_m = 'm('
    for i in original_set:
        string_m += 'm(' + str(i) + ')'
    string_m += ')'
    m = ParseTerm(string_m)
    p = ParseTerm('p(n(m(1)m(2)m(3))s()u())')

    sys = CPSystem('s1')
    sys.AddRule(rule4)
    sys.AddSystemTerm(t)
    sys.AddSystemTerm(m)
    sys.AddSystemTerm(p)
    sys.DetailOn()

    #Initial state of the cP system
    sys.Snapshot()
    sys.Run()

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