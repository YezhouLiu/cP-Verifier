from cpsystem import CPSystem
from typing import OrderedDict
from term import Term
from rule import Rule
from cpsystem import CPSystem
import json

def ParsecPVJSON(file_path):
    f = open(file_path, 'r')
    cPV_json = json.loads(f.read())
    ruleset = cPV_json['ruleset']
    system_terms = cPV_json['terms']
    system_state = cPV_json['state']
    system_name = cPV_json['name']
    return ParseSystem(ruleset, system_terms, system_state, system_name)
    

def ParseSystem(str_ruleset, system_terms, system_state, system_name):
    sys1 = CPSystem(system_state, system_name)
    for rule in str_ruleset:
        sys1.AddRule(ParseRule(rule))
    for term in system_terms:
        if ParseTerm(term) != '':
            sys1.AddSystemTerm(ParseTerm(term), system_terms[term])
    return sys1

# Term parser
def ParseTerm(str_term):
    if len(str_term) <= 1: #no need to parse '' or simple terms: atom, variable or number
        return str_term
    elif str_term.isnumeric():
        return str_term
    elif len(str_term) < 3: #a(, bc, ()... invalid term
        return ''
    elif str_term[1] != '(' or str_term[len(str_term)-1] != ')':#invalid compound term
        return ''
    #compound terms
    t1 = Term(str_term[0])
    str_cell_content = str_term[2:len(str_term)-1]
    cell_content = []
    i = 0
    temp_str = ''
    bracket_count = 0
    while i < len(str_cell_content):
        ch = str_cell_content[i]
        if ch.isnumeric(): #number
            temp_str += ch
            if i < len(str_cell_content) - 1 and str_cell_content[i+1].isnumeric():
                pass
            else:
                cell_content.append(temp_str) #[123]
                temp_str = ''
        elif ch >= 'A' and ch <= 'Z': #variable
            cell_content.append(ch)
        elif ch >= 'a' and ch <= 'z': #atom or label
            if i < len(str_cell_content) - 2 and str_cell_content[i+1] == '(': #label
                j = i + 2
                bracket_count = 1
                while(bracket_count > 0 and j < len(str_cell_content)):
                    if str_cell_content[j] == '(':
                        bracket_count += 1
                    elif str_cell_content[j] == ')':
                        bracket_count -= 1
                    j += 1
                cell_content.append(str_cell_content[i:j]) #a compound term
                i = j
                continue
            else: #atom
                cell_content.append(ch)
        else: #other characters, ' ', @, $... which will be ignored
            pass
        i += 1  
    for s1 in cell_content:
        pt1 = ParseTerm(s1)
        if isinstance(pt1, Term):
            t1.AddSubterm(pt1)
        elif pt1.isnumeric():
            t1.AddNumber(int(pt1))
        elif pt1 >= 'A' and pt1 <= 'Z':
            t1.AddVariable(pt1)
        elif pt1 >= 'a' and pt1 <= 'z':
            t1.AddAtom(pt1)
        else: #blank space, wrong characters... 
            continue
    return t1

def ParseTerms(str_terms): #parse a string of terms splitted by blank spaces, returns a dictionary
    terms = str_terms.split(' ')
    term_dict = OrderedDict()
    for t1 in terms:
        t2 = ParseTerm(t1)
        if t2 != '':
            if t2 in term_dict:
                term_dict[t2] += 1
            else:
                term_dict[t2] = 1
    return term_dict
    

def ParseRule(str_rule): # lstate lterm1 lterm2... ->1/+ rstate rterm1 rterm2... | pmt1, pmt2...
    #terms need to be splitted by spaces
    rule = str_rule.split(' ')
    element_type = 'left_state'
    lstate = ''
    rstate = ''
    l_terms = []
    r_terms = []
    pmt_terms = []
    app_model = ''
    for item in rule:
        item = item.strip()
        if item[:2] == '->':
            app_model = item[-1:]
            element_type = 'right_state'
            continue
        if item == '|':
            element_type = 'promoter'
            continue 
        if element_type == 'left_state':
            lstate = item
            element_type = 'left_term'
            continue
        if element_type == 'right_state':
            rstate = item
            element_type = 'right_term'
            continue
        if element_type == 'left_term':
            l_terms.append(item)
            continue
        if element_type == 'right_term':
            r_terms.append(item)
            continue
        if element_type == 'promoter':
            pmt_terms.append(item)
            continue 
    rule = Rule(lstate, rstate, app_model)
    for x in l_terms:
        if ParseTerm(x) != '':
            rule.AddL(ParseTerm(x))
    for y in r_terms:
        if ParseTerm(y) != '':
            rule.AddR(ParseTerm(y))
    for z in pmt_terms:
        if ParseTerm(z) != '':
            rule.AddPMT(ParseTerm(z))
    return rule