import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpparser import ParseTerm
from cpparser import ParseRule

t1 = ParseTerm('a')
t2 = ParseTerm('p(u()n(M) s())')
t3 = ParseTerm('f(g(a) h(k(b 1 3)))')
t4 = ParseTerm('p(u(Xm(Y)) n(Z)s(SY ))')

print(t1,t2,t3,t4)
t2.Print()
t3.Print()
t4.Print()

rule1 = ParseRule('s0 ->1 s1 p(u()n(M)s()) | m(M)')
rule2 = ParseRule('s1 ->1 s2 o(X) | p(u(X)s(T)A)) t(T)')
rule3 = ParseRule('s1 ->1 s3 o() |  p(n()A)')
rule4 = ParseRule('s1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))')
rule5 = ParseRule('s1 p(A) ->+ s1')

rule1.Print()
rule2.Print()
rule3.Print()
rule4.Print()
rule5.Print()
