import lnmu
from term import Term

a1 = Term('a')
a1.AddAtoms('a')
a1.AddVariables('XXY')

a2 = Term('a')
a2.AddAtoms('pleaapp')
a1p = Term('a')
a1p.AddAtoms('banana')
a1q = Term('a')
a1q.AddAtoms('pear')
a2.AddSubterm(a1q, 3)
a2.AddSubterm(a1p, 5)

uni1 = lnmu.UnifyTerms(a1, a2)
if len(uni1) > 0:
  for x in uni1:
    lnmu.PrintBinding(x)




