import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import OrderedDict
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
    
    
t1 = ParseTerm('p(n(Z)s(SY)u(Xm(Y)))')

unifier = OrderedDict()
d1 = OrderedDict()
d1['1'] = 1
unifier['Y'] = d1
unifier['S'] = OrderedDict()
unifier['X'] = OrderedDict()
m1 = ParseTerm('m(2)')
d2 = OrderedDict()
d2[m1] = 1
unifier['Z'] = d2

t3 = lnmu.ApplyBindingMultiset(t1.Subterms(), unifier)
lnmu.PrintMultiset(t3)