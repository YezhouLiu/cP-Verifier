import lnmu
from term import Term

a1 = Term('b')
a1.AddAtoms('apple')
a1.AddVariables('XXY')
b1 = Term('b')
a2 = Term('a')
a2.AddAtoms('pleap')
b1.AddSubterm(a1)
b1.AddSubterm(a2)

c1 = Term('c')
c1.AddAtoms('de')
d1 = Term('d')
d1.AddSubterm(c1)
c2 = Term('c')
c2.AddVariables('XYY')
d1.AddSubterm(c2)
d1.AddSubterm(c2)

b1.AddSubterm(d1)

print('*****************b1*****************')
b1.Print()

ms1 = {'b':1, c1: 2}
ms2 = {'a':1, 'c': 2, 'b': 2}
binding1 = {'X':ms1, 'Y': ms2}
print('*****************binding1*****************')
lnmu.PrintBinding(binding1)

b1p = lnmu.ApplyBindingTerm(b1, binding1)
print('*****************b1p*****************')
b1p.Print()

ms3 = {'X':2, 'Y': 3, c2: 2, 'a': 5}
print('*****************ms3*****************')
lnmu.PrintMultiset(ms3)

ms3p = lnmu.ApplyBindingMultiset(ms3, binding1)
print('*****************ms3p*****************')
lnmu.PrintMultiset(ms3p)