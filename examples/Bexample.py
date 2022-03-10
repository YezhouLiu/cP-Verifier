import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import simpleB

#inputs
ruleset = ['s1 a a ->1 s1 b', 's1 b b ->1 s1 c d d']
system_terms = {'a': 10}
system_state = 's1'
system_name = 'simplecp'

Bfile = simpleB.cPtoB(ruleset, system_terms, system_state, system_name)
#print(Bfile)

#simpleB.ProBHelp()

simpleB.ProBMC(ruleset, system_terms, system_state, system_name)
#simpleB.ProBMCCustom(ruleset, system_terms, system_state, system_name, '-bf -mc -nodead 1000')

#simpleB.ProBMCBreathFirst(ruleset, system_terms, system_state, system_name)
#simpleB.ProBMCTimeout(ruleset, system_terms, system_state, system_name, 10000)