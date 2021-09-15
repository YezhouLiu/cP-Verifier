from compoundterm import CPTerm
from compoundrule import CPRule

# Term parser
def ParseTerm(str_term):
    #print(str_term)
    if str_term == '' or str_term.isnumeric() or str_term[0].isupper():
        return -1
    name = str_term[0]
    subterm = str_term[2:-1]
    t = CPTerm(name)
    jump = -1
    for i in range(len(subterm)):
        if i < jump:
             continue
        c = subterm[i]
        if c.isnumeric():
            x = '' + c
            ck = True
            while i < len(subterm)-1:
                i += 1
                if subterm[i].isnumeric():
                    x += subterm[i]
                else:
                    jump = i
                    ck = False
                    break
            t.SetValue(int(x))
            if ck:
                break
        elif c.isupper():
            t.AddVar(c)
        elif c.islower():
            x = '' + c
            if i < len(subterm)-1 and subterm[i+1] == '(':
                bcount = 1
                x += '('
                for j in range(i+2,len(subterm)):
                    sj = subterm[j]
                    x += sj
                    if sj == '(':
                        bcount += 1
                    elif sj == ')':
                        bcount -= 1
                    if bcount == 0:
                        jump = j + 1
                        break
                t.AddSubterm(ParseTerm(x))
    return t

def ParseRule(str_rule): # lstate lterm1 lterm2... ->1/+ rstate rterm1 rterm2... | pmt1, pmt2...
    contents = str_rule.split(' ')
    element_type = 'left_state'
    lstate = ''
    rstate = ''
    l_terms = []
    r_terms = []
    pmt_terms = []
    app_model = ''
    for content in contents:
        if content[:2] == '->':
            app_model = content[-1:]
            element_type = 'right_state'
            continue
        if content == '|':
            element_type = 'promoter'
            continue
        
        if element_type == 'left_state':
            lstate = content
            element_type = 'left_term'
            continue
        if element_type == 'right_state':
            rstate = content
            element_type = 'right_term'
            continue

        if element_type == 'left_term':
            l_terms.append(content)
            continue
        if element_type == 'right_term':
            r_terms.append(content)
            continue
        if element_type == 'promoter':
            pmt_terms.append(content)
            continue 
    rule = CPRule(lstate, rstate, app_model)
    for x in l_terms:
        rule.AddL(ParseTerm(x))
    for y in r_terms:
        rule.AddR(ParseTerm(y))
    for z in pmt_terms:
        rule.AddPM(ParseTerm(z))
    return rule