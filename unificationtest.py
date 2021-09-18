import lnmu
from term import Term
from cpparser import ParseTerm

tv1 = ParseTerm('p(u(X)n(Zm(Y))s(S))')
tg1 = ParseTerm('p(n(m(1)m(2)m(3))s()u())')
uni2 = lnmu.UnifyTerms(tv1, tg1)
tv1.Print()
tg1.Print()
if len(uni2) > 0:
  for x in uni2:
    lnmu.PrintBinding(x)