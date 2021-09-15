from term import Term

a1 = Term('b')
a1.AddAtoms('apple')
a1.AddVariables('XY')
b1 = Term('b')
a2 = Term('a')
a2.AddAtoms('pleap')
b1.AddSubterm(a1)
b1.AddSubterm(a2)

a1.Print()
b1.Print()
c1 = Term('c')
c1.Print()