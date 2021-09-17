import lnmu
from term import Term

a1 = Term('a')
a1.AddAtoms('1a')
a1.AddVariables('XXY')
a1k = Term('c')
a1k.AddVariables('XZ')
a1.AddSubterm(a1k, 2)

a2 = Term('a')
a2.AddAtoms('aagpp1p')
a1p = Term('b')
a1p.AddAtoms('11')
a1q = Term('c')
a1q.AddAtoms('pa11')
a2.AddSubterm(a1q, 2)
a2.AddSubterm(a1p, 3)

uni1 = lnmu.UnifyTerms(a1, a2)
a1.Print()
a2.Print()
if len(uni1) > 0:
  for x in uni1:
    lnmu.PrintBinding(x)






