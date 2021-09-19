from simpleterm import CPSimpleTerm
from simplerule import CPSimpleRule
from simplecpsystem import CPSystemSimple

# x := y * z
# rule 1: S0 ->1 S2 x(0) | z(0)
rhs1_1 = CPSimpleTerm('x') #x(0)
pmt1_1 = CPSimpleTerm('z') #z(0)
rule1 = CPSimpleRule('S0', 'S2', '1') #S0 -> S2, application model 1
rule1.AddR(rhs1_1)
rule1.AddPM(pmt1_1)

# rule 2: S0 ->1 S1 x(0) w(Y) | y(Y)
rhs2_1 = CPSimpleTerm('x') #x(0)
rhs2_2 = CPSimpleTerm('w', 0, 'Y') #w(Y)
pmt2_1 = CPSimpleTerm('y', 0, 'Y') #y(Y)
rule2 = CPSimpleRule('S0', 'S1', '1')
rule2.AddR(rhs2_1)
rule2.AddR(rhs2_2)
rule2.AddPM(pmt2_1)

# rule 3: S1 x(X) w(0) ->1 S2 x(X)
lhs3_1 = CPSimpleTerm('x', 0, 'X') #x(X)
lhs3_2 = CPSimpleTerm('w') #w(0)
rhs3_1 = CPSimpleTerm('x', 0, 'X') #x(X)
rule3 = CPSimpleRule('S1', 'S2', '1')
rule3.AddL(lhs3_1)
rule3.AddL(lhs3_2)
rule3.AddR(rhs3_1)

# rule 4: S1 x(X) w(Y1) ->1 S1 x(XZ) w(Y) | z(Z)
lhs4_1 = CPSimpleTerm('x', 0, 'X') #x(X)
lhs4_2 = CPSimpleTerm('w', 1, 'Y') #w(Y1)
rhs4_1 = CPSimpleTerm('x', 0, 'XZ') #x(XZ)
rhs4_2 = CPSimpleTerm('w', 0, 'Y') #w(Y)
pmt4_1 = CPSimpleTerm('z', 0, 'Z') #z(Z)
rule4 = CPSimpleRule('S1', 'S1', '1')
rule4.AddL(lhs4_1)
rule4.AddL(lhs4_2)
rule4.AddR(rhs4_1)
rule4.AddR(rhs4_2)
rule4.AddPM(pmt4_1)

#system, suppose we have y(4) and z(7) in the system
y = CPSimpleTerm('y', 8)
z = CPSimpleTerm('z', 7)
sys = CPSystemSimple('S0')
sys.AddRule(rule1)
sys.AddRule(rule2)
sys.AddRule(rule3)
sys.AddRule(rule4)
sys.AddTerm(y)
sys.AddTerm(z)

#Initial state of the cP system
sys.SystemSnapshot()
sys.RunUntilSystemHalt(10) #run at most 10 loops, which is enough here