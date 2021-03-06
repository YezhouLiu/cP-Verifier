import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import simpleCSPsharp
#inputs
ruleset = ['s1 a a ->1 s1 b', 's1 b b ->1 s1 c d d']
system_terms = {'a': 10}
system_state = 's1'
system_name = 'simplecp'

CSPfile = simpleCSPsharp.cPtoCSP(ruleset, system_terms, system_state, system_name)
print(CSPfile)

simpleCSPsharp.PAT3MC(ruleset, system_terms, system_state, system_name)


#custom_properties = ['#assert P0() |= F r1', '#assert P0() |= G r2']
#simpleCSPsharp.PAT3MCCustom(ruleset, system_terms, system_state, system_name, custom_properties)