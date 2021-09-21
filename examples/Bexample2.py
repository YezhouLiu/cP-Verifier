import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import simpleB

#inputs
ruleset = ['s1 a a a b ->+ s1 b', 's1 b ->+ s1 a']
system_terms = {'a': 100, 'b': 90}
system_state = 's1'
system_name = 'simplecp2'

Bfile = simpleB.cPtoB(ruleset, system_terms, system_state, system_name)
print(Bfile)

simpleB.ProBMCBreathFirst(ruleset, system_terms, system_state, system_name, 5000)
simpleB.ProBMCTimeout(ruleset, system_terms, system_state, system_name, 10000)