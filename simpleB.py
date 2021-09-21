from cpparser import ParseRule
import lnmu
import sys
import subprocess

#only for ground, atom cp rules
def cPtoB(str_ruleset, system_terms, system_state, system_name):
    atoms = set()
    ruleset = []
    for str_rule in str_ruleset:
        rule = ParseRule(str_rule)
        ruleset.append(rule)
        for a1 in rule.LHS():
            atoms.add(a1)
        for a2 in rule.RHS():
            atoms.add(a2)
        for a3 in rule.PMT():
            atoms.add(a3)
    B_file = 'MACHINE ' + system_name
    B_file += '\nVARIABLES state'
    for ch in atoms:
        B_file += ',' + ch
    B_file += '\nINVARIANT state >= 0'
    for ch in atoms:
        B_file += ' & ' + ch + ' >= 0'
    B_file += '\nINITIALISATION state := ' + system_state[1:]
    for ch in atoms:
        if ch in system_terms:
            B_file += '; ' + ch + ' := ' + str(system_terms[ch])
        else:
            B_file += '; ' + ch + ' := 0'
    B_file += '\nOPERATIONS\n'
    i = 1
    for rule in ruleset:
        B_file += 'r' + str(i) + ' = PRE state = ' + rule.LState()[1:]
        LP = lnmu.MultisetUnion(rule.LHS(), rule.PMT())
        for atom in LP:
            B_file += ' & ' + atom + ' >= ' + str(LP[atom])
        B_file += ' THEN '
        for atom in rule.LHS():
            B_file += atom + ' := ' + atom + ' - ' + str(rule.LHS()[atom]) + '; '
        for atom in rule.RHS():
            B_file += atom + ' := ' + atom + ' + ' + str(rule.RHS()[atom]) + '; '
        B_file += 'state := ' + rule.RState()[1:] + ' END;\n'
        i += 1
    B_file = B_file[:-2]
    B_file += '\nEND'
    return B_file
    
    
def CreateBFile(str_ruleset, system_terms, system_state, system_name):
    sys.stdout = open(system_name + '.mch', 'w')
    print(cPtoB(str_ruleset, system_terms, system_state, system_name))
    sys.stdout = sys.__stdout__
    
def ProBHelp():
    result = subprocess.run(['probcli', '--help'], stdout=subprocess.PIPE)
    PrintProBRes(str(result))
    
def ProBMC(str_ruleset, system_terms, system_state, system_name):
    CreateBFile(str_ruleset, system_terms, system_state, system_name)
    file_path = system_name + '.mch'
    result = subprocess.run(['probcli', file_path], stdout=subprocess.PIPE)
    PrintProBRes(str(result))
    
def ProBMCCustom(str_ruleset, system_terms, system_state, system_name, str_commands):
    CreateBFile(str_ruleset, system_terms, system_state, system_name)
    file_path = system_name + '.mch'
    commands = str_commands.split()
    prob_commands = ['probcli', file_path]
    for cmd in commands:
        prob_commands.append(cmd)
    result = subprocess.run(prob_commands, stdout=subprocess.PIPE)
    PrintProBRes(str(result))

def ProBMCBreathFirst(str_ruleset, system_terms, system_state, system_name):
    ProBMCCustom(str_ruleset, system_terms, system_state, system_name, '-bf -mc 1000')
    
def ProBMCTimeout(str_ruleset, system_terms, system_state, system_name, time_limit):
    mode = '-timeout ' + str(time_limit)
    ProBMCCustom(str_ruleset, system_terms, system_state, system_name, mode)
        


def PrintProBRes(result):
    result_len = len(str(result))
    i = 0
    while i < result_len:
        if i < result_len - 5 and str(result)[i: i+4] == '\\r\\n':
            print()
            i += 4
        else:
            print(str(result)[i], end = '')
            i += 1
            
