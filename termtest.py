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


a1p = Term('a')
a1p.AddAtoms('banana')
a1q = Term('a')
a1q.AddAtoms('bnnaaa')

c = Term('c')
c.AddSubterm(a1p)
c.AddSubterm(a1q)
c.Print()
print(c.Subterms())