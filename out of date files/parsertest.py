from cpparser import ParseTerm
from cpparser import ParseRule

'''
x = ParseTerm('p(u() n(M) s())')
print(x)
print(x.ToString())

x = ParseTerm('p(u() X Y 166 n(M) s())')
print(x)
print(x.ToString())
print(x.value)

x = ParseTerm('t(38)')
print(x.ToString())
'''

rule4 = ParseRule('s1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))')
print(rule4.ToString())