import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import simpleCSPsharp

#inputs
ruleset = ['s1 a a a b ->+ s1 b', 's1 b ->+ s1 a']
system_terms = {'a': 100, 'b': 90}
system_state = 's1'
system_name = 'simplecp2'

CSPfile = simpleCSPsharp.cPtoCSP(ruleset, system_terms, system_state, system_name)
print(CSPfile)

simpleCSPsharp.PAT3MC(ruleset, system_terms, system_state, system_name)


#custom_properties = ['#assert P0() |= F r1', '#assert P0() |= G r2']
#simpleCSPsharp.PAT3MCCustom(ruleset, system_terms, system_state, system_name, custom_properties)