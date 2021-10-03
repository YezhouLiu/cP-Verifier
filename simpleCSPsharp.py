from cpparser import ParseRule
import os
import sys
import subprocess

#only for ground, atomic cp rules, without promoters
def cPtoCSP(str_ruleset, system_terms, system_state, system_name):
    atoms = set()
    ruleset = []
    for str_rule in str_ruleset:
        rule = ParseRule(str_rule)
        ruleset.append(rule)
        for a1 in rule.LHS():
            atoms.add(a1)
        for a2 in rule.RHS():
            atoms.add(a2)
    CSP_file = '//' + system_name + '\n'
    for ch in atoms:
        CSP_file += 'var ' + ch + ';\n'
    CSP_file += 'var state = ' + system_state[1:] + ';\n\n'
    CSP_file += 'S0() = cp_init{\n'
    for ch in atoms:
        if ch in system_terms:
            CSP_file += ch + ' = ' + str(system_terms[ch]) + ';\n'
        else:
            CSP_file += ch + ' = 0;\n'
    CSP_file += '}-> S1();\n'
    
    i = 1
    for rule in ruleset:
        pn = str(i)
        CSP_file += 'S' + pn + '() = r' + pn + '{\n'
        CSP_file += 'if (state == ' + rule.LState()[1:]
        for atom in rule.LHS():
            CSP_file += ' && ' + atom + ' > 0'
        CSP_file += '){\n'
        for atom in rule.LHS():
            CSP_file += atom + ' = ' + atom + ' - ' + str(rule.LHS()[atom]) + ';\n'
        for atom in rule.RHS():
            CSP_file += atom + ' = ' + atom + ' + ' + str(rule.RHS()[atom]) + ';\n'
        CSP_file += 'state = ' + rule.RState()[1:] + ';\n'
        if i < len(ruleset) - 1:
            CSP_file += '}\n}-> S' + str(i + 1) + '();\n'
        else:
            CSP_file += '}\n}-> S1();\n'
        i += 1        
    return CSP_file
    
def CreateCSPFile(str_ruleset, system_terms, system_state, system_name):
    sys.stdout = open(system_name + '.csp', 'w')
    print(cPtoCSP(str_ruleset, system_terms, system_state, system_name))
    sys.stdout = sys.__stdout__
    
def PAT3MC(str_ruleset, system_terms, system_state, system_name):
    CSP_file = cPtoCSP(str_ruleset, system_terms, system_state, system_name)
    CSP_file += '#assert S0() nonterminating;\n'
    CSP_file += '#assert S0() deadlockfree;\n'
    CSP_file += '#assert S0() divergencefree;\n'
    CSP_file += '#assert S0() deterministic;\n'
    sys.stdout = open(system_name + '.csp', 'w')
    print(CSP_file)
    sys.stdout = sys.__stdout__
    cwd = os.getcwd()
    file_path = cwd + '\\' + system_name + '.csp'
    output_path = cwd + '\\pat3_result.txt'
    result = subprocess.run(['PAT3.Console.exe', '-csp', '-v', file_path, output_path], stdout=subprocess.PIPE)
    PrintPAT3Res(str(result))
    
def PAT3MCCustom(str_ruleset, system_terms, system_state, system_name, list_of_properties):
    CSP_file = cPtoCSP(str_ruleset, system_terms, system_state, system_name)
    for prop in list_of_properties:
        CSP_file += prop + ';\n'
    sys.stdout = open(system_name + '.csp', 'w')
    print(CSP_file)
    sys.stdout = sys.__stdout__
    cwd = os.getcwd()
    file_path = cwd + '\\' + system_name + '.csp'
    output_path = cwd + '\\pat3_result.txt'
    result = subprocess.run(['PAT3.Console.exe', '-csp', '-v', file_path, output_path], stdout=subprocess.PIPE)
    PrintPAT3Res(str(result))
            
def PrintPAT3Res(result):
    result_len = len(str(result))
    i = 0
    while i < result_len:
        if i < result_len - 5 and str(result)[i: i+4] == '\\r\\n':
            print()
            i += 4
        else:
            print(str(result)[i], end = '')
            i += 1