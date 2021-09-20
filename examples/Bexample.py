import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simpleB import cPtoB, ProBMC, ProBHelp

#inputs
ruleset = ['s1 a a ->1 s1 b', 's1 b b ->1 s1 c d d']
system_terms = {'a': 10}
system_state = 's1'
system_name = 'simplecp'

Bfile = cPtoB(ruleset, system_terms, system_state, system_name)
print(Bfile)

ProBHelp()

ProBMC(ruleset, system_terms, system_state, system_name)