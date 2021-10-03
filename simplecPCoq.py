from cpparser import ParseRule
import sys

#only for ground, atomic cp rules, without promoters
def cPtocPCoq(str_ruleset, system_terms, system_state, system_name):
    atoms = set()
    ruleset = []
    for str_rule in str_ruleset:
        rule = ParseRule(str_rule)
        ruleset.append(rule)
        for a1 in rule.LHS():
            atoms.add(a1)
        for a2 in rule.RHS():
            atoms.add(a2)
    cPCoq_file = '(*' + system_name + '*)\n'
    cPCoq_file += 'From CP Require Export operations.\n'
    cPCoq_file += 'From Coq Require Import Lists.List.\n'
    cPCoq_file += 'Import ListNotations.\n\n'
    cPCoq_file += 'Definition cPsys1 := cP_sys (s ' + system_state[1:] + ') ['
    has_sys_term = False
    for t1 in system_terms:
        multi = system_terms[t1]
        for i in range(multi):
            if has_sys_term:
                cPCoq_file += '; Atom ' + t1
            else:
                has_sys_term = True
                cPCoq_file += 'Atom ' + t1
    cPCoq_file += '].\n\n'
            
    i = 1
    for rule in ruleset:
        cPCoq_file += 'Definition r' + str(i) + ' (sys:cPsystem_conf) : cPsystem_conf :=\n'
        cPCoq_file += 'match sys with\n'
        cPCoq_file += '| cP_sys (s 1) terms =>\n'
        lhs_terms = '['
        has_lhs_term = False
        for t2 in rule.LHS():
            multi2 = rule.LHS()[t2]
            for i in range(multi2):
                if has_lhs_term:
                    lhs_terms += '; Atom ' + t2
                else:
                    has_lhs_term = True
                    lhs_terms += 'Atom ' + t2
        lhs_terms += ']'
        new_sys_terms = 'sys'
        for t3 in rule.LHS():
            multi3 = rule.LHS()[t3]
            for i in range(multi3):
                new_sys_terms = '(ConsumeATerm (Atom ' + t3 + ') ' + new_sys_terms + ')'
        for t4 in rule.RHS():
            multi4 = rule.RHS()[t4]
            for i in range(multi4):
                new_sys_terms = '(ProduceATerm (Atom ' + t4 + ') ' + new_sys_terms + ')'       
        cPCoq_file += 'if AtomBagIn ' + lhs_terms + ' terms then ChangeState (s ' + rule.RState()[1:] + ') ' + new_sys_terms + '\n'
        cPCoq_file += 'else sys\n'
        cPCoq_file += '| _ => sys\n'
        cPCoq_file += 'end.\n'
    return cPCoq_file

def CreatecPCoqFile(str_ruleset, system_terms, system_state, system_name):
    sys.stdout = open(system_name + '.v', 'w')
    print(cPtocPCoq(str_ruleset, system_terms, system_state, system_name))
    sys.stdout = sys.__stdout__