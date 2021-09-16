#computing engine - Yezhou

from copy import deepcopy
from term import Term
from collections import OrderedDict

#UNIFICATION
#------------------------------------------------------------------------------
def UnifyTerms(tv: Term, tg: Term): #tv: variable term, tg: ground term, return value: substitutions + token, which indicates that unification succeeds or fails 
    if not tg.IsGround(): #one-way unification, pattern matching only
        return {}, False
    if tv.IsGround(): #both ground terms, if tv = tg, any substitution unifies it; otherwise, not unifiable
        if tv.ToString() == tg.ToString():
            return {}, True
        else:
           return {}, False 
    if tv.Label() != tg.Label(): #label mismatching, not unifiable
        return {}, False
    G = [] #equations
    G.append((tv.CellContent(), tg.CellContent())) #an equation is a pair (lhs, rhs)
    SS = [] #the set of unifiers
    S = {} #current substitution
    LNMU(G, S, SS)
    return SS

def LNMU(G, S, SS): #G: set G, all working equations; SS: all substitutions, S: current subtitution
    #process current G - one branch
    working_G = []
    for equation in G:
        mv_temp = equation[0] #lhs, mv
        mg_temp = equation[1] #rhs, mg
        mv, mg = GROUND(mv_temp, mg_temp) #apply ground
        if FAIL1(mv, mg) or FAIL2(mv, mg):
            return False
        if can_be_DELETED(mv, mg): #the equation is lambda = lambda
            continue
        elif len(mv) == 0: #fail when lambda = non-empty multiset
            return False
        else:
            working_G.append((mv, mg))
    if len(working_G) == 0: #success, all the equations are solved
        exist1 = False
        for s1 in SS:
            if BindingEqual(s1, S):
                exist1 = True
                break
        if not exist1:
            SS.append(S)
        return True

    (mv, mg) = working_G[0] #deal with the first equation
    if len(mv) == 1: #lhs only contains one kind of variable or variable term, apply VARIABLE
        for item in mv:
            if item >= 'A' and item <= 'Z': #item is a variable
                dict1 = OrderedDict()
                for item2 in mg:
                    if mg[item2] % mv[item] != 0: #fail, XX = f(a)f(a)f(a)
                        return False 
                    else: #XX = aaaa
                        dict1[item2] = mg[item2] / mv[item] #dict1[a] = 4 / 2 = 2, X -> aa
                S1 = deepcopy(S)
                S1[item] = dict1 # X -> dict1
                G_temp = working_G[1:]
                G_new = []
                for equation in G_temp:
                    lhs = equation[0] #mv
                    rhs = equation[1] #mg
                    lhs_new = ApplyBindingMultiset(lhs, S1)
                    G_new.append((lhs_new, rhs))
                LNMU(G_new, S1, SS)
            elif isinstance(item, Term): #item is a variable term
                if len(mg) > 1: #fail, f(X) = f(a)g(b)
                    return False 
                for item2 in mg: #the only term in mg, f(XY) = f(abc)
                    if isinstance(item2, Term) and item.Label() == item2.Label() and mv[item] == mg[item2]: #same label and multiplicity
                        G1 = [(item.CellContent(), item2.CellContent())] + working_G[1:] #get rid of functors, XY = abc
                        return LNMU(G1, S, SS)
                    else: #fail, f(X) = g(ab), or f(X)f(X) = f(abc)f(abc)f(abc)
                        return False
            else: #which should not happen
                return False

    elif ContainsCompoundTerms(mv): #mv contains functors (compound terms), apply FUNCTOR
        mv_temp = deepcopy(mv)
        succ = False
        for item in mv:
            if isinstance(item, Term):
                mv_temp.pop(item)
                for item2 in mg: #f(X)g(Y) = f(a)f(b)g(c)
                    if isinstance(item2, Term) and item.Label() == item2.Label() and mv[item] == mg[item2]:
                        mg_temp = deepcopy(mg)
                        mg_temp.pop(item2)
                        G1 = [(item.CellContent(), item2.CellContent())] + working_G[1:]
                        G1.append((mv_temp, mg_temp))
                        LNMU(G1, S, SS)
                        succ = True #successfully applied FUNCTOR
                break #only deal with one compound term a time
        return succ
    else: #mv contains no functor, no atom, but only variables, XXY = f(a)bbccccc
        for item in mv: #only deal with the first variable, let's call it X here
            if isinstance(item, Term): #which won't happen
                return False
            elif item < 'A' or item > 'Z': #not a variable
                return False
            else: # XXY = f(a)bbccccc, X -> lambda, b, c, bc, cc, bcc
                all_combinations = []
                for item2 in mg:
                    if mg[item2] < mv[item]: #mismatch, ignore it, XXX != f(a)f(a)
                        continue
                    else:
                        q1 = int(mg[item2] / mv[item])
                        item2_mappings = []
                        for copies in range(q1 + 1):
                            temp_dict = OrderedDict()
                            if copies > 0:
                                temp_dict[item2] = copies
                            item2_mappings.append(temp_dict)
                        all_combinations.append(item2_mappings)

                expanded = [] #it will store all possible bindings for X
                ExpandCombinations(all_combinations, {}, expanded)
                for binding1 in expanded:
                    S1 = deepcopy(S)
                    S1[item] = binding1
                    G_new = []
                    for equation in working_G:
                        lhs = equation[0] #mv
                        rhs = equation[1] #mg
                        lhs_new = ApplyBindingMultiset(lhs, S1)
                        G_new.append((lhs_new, rhs))
                        LNMU(G_new, S1, SS)


def ExpandCombinations(all_combinations, CC, EC): #EC: expanded combinations, CC: current/working dict
    if len(all_combinations) == 0:
        EC.append(CC)
    else:
        for comb1 in all_combinations[0]:
            CC2 = MultisetUnion(CC, comb1)
            ExpandCombinations(all_combinations[1:], CC2, EC)

def can_be_DELETED(mv: OrderedDict, mg: OrderedDict):
    if len(mv) == 0 and len(mg) == 0:
        return True
    else:
        return False 

def FAIL1(mv: OrderedDict, mg: OrderedDict): #true: fail, false: succeed
    for t1 in mv:
        if t1 not in mg:
            if isinstance(t1, Term) and t1.IsGround(): #t1 a is ground term
                return True
            elif t1 < 'A' or t1 > 'Z': #t1 is ground/ not a var
                return True
    return False

def FAIL2(mv: OrderedDict, mg: OrderedDict): #true: fail, false: succeed
    if MultisetInclusion(Functors(mg), Functors(mv)):
        return False
    else:
        return True

def Functors(m: OrderedDict):
    labels = OrderedDict()
    for term in m:
        if isinstance(term, Term):
            if term.Label() in labels:
                labels[term.Label()] += 1
            else:
                labels[term.Label()] = 1
    return labels

def GROUND(ms1: OrderedDict, ms2: OrderedDict): #return two multisets, optimize it later as needed
    mi = MultisetIntersection(ms1, ms2)
    return MultisetMinus(ms1, mi), MultisetMinus(ms2, mi)

def ContainsCompoundTerms(mv: OrderedDict):
    for item in mv:
        if isinstance(item, Term):
            return True
    return False

#BINDING APPLICATION
#------------------------------------------------------------------------------

#no occurs check here, one-way unification, X -> f(a g(X)) will not happen
def ApplyBindingTerm(t1: Term, bd1: OrderedDict): #binding: map, from variables to multisets
    t2 = Term(t1.Label())
    t2.SetAtoms(t1.Atoms())
    for v in t1.Variables():
        mult = t1.Variables()[v]
        if v in bd1:
            ms1 = bd1[v]
            for item in ms1:
                mult2 = ms1[item]
                if isinstance(item, Term):
                    t2.AddSubterm(item, mult * mult2)
                elif item >= 'a' and item <= 'z':
                    t2.AddAtom(item, mult * mult2)
                elif item == '1':
                    t2.AddNumber(mult * mult2)
                else: #which should never happen 
                    continue
        else:
            t2.AddVariable(v, mult)
    for t in t1.Subterms():
        mult = t1.Subterms()[t]
        t2.AddSubterm(ApplyBindingTerm(t, bd1), mult)
    return t2

def ApplyBindingMultiset(ms1: OrderedDict, bd1: OrderedDict): #apply bindings to a nested multiset
    new_ms = deepcopy(ms1)
    for item in ms1:
        mult = ms1[item]
        if isinstance(item, Term):
            new_ms.pop(item)
            new_ms[ApplyBindingTerm(item, bd1)] = mult
        elif item >= 'a' and item <= 'z':
            continue
        elif item == '1':
            continue
        elif item >= 'A' and item <= 'Z':
            if item in bd1:
                new_ms.pop(item)
                for item2 in bd1[item]:
                    mult2 = bd1[item][item2]
                    if item2 in new_ms:
                        new_ms[item2] += mult * mult2
                    else:
                        new_ms[item2] = mult * mult2
        else:
            continue
    return new_ms

def PrintBinding(bd1: OrderedDict): #binding: X -> multiset
    for var in bd1:
        ms1 = bd1[var]
        print(var + ':')
        for item in ms1:
            mult = ms1[item]
            if isinstance(item, Term):
                print(item.ToString() + ':' + str(mult), end = ' ')
            else:
                print(item + ':' + str(mult), end = ' ')
            print()
    print()

def BindingEqual(bd1: OrderedDict, bd2: OrderedDict): #bd1 =? bd2
    if len(bd1) != len(bd2):
        return False
    for var in bd1:
        if not var in bd2:
            return False
        elif not MultisetEqual(bd1[var], bd2[var]):
            return False
    return True

#MULTISET OPERATIONS
#------------------------------------------------------------------------------
def MultisetUnion(ms1: OrderedDict, ms2: OrderedDict): #Multiset = OrderedDict, ms1 \cup ms2
    ms = deepcopy(ms1)
    for key in ms2:
        if key in ms:
            ms[key] += ms2[key]
        else:
            ms[key] = ms2[key]
    return ms

def MultisetInclusion(ms1: OrderedDict, ms2: OrderedDict): #return if ms1 includes ms2
    for key in ms2:
        if key in ms1 and ms1[key] >= ms2[key]:
            continue
        else:
            return False
    return True

def MultisetIn(ms1: OrderedDict, ms2: OrderedDict): #some people like this direction :)
    return MultisetInclusion(ms2, ms1)

def MultisetMinus(ms1: OrderedDict, ms2: OrderedDict): #ms1 \ ms2
    ms = deepcopy(ms1)
    if MultisetIn(ms2, ms): #otherwise no computation will be done
        for key in ms2:
            if ms[key] == ms2[key]:
                ms.pop(key)
            else:
                ms[key] -= ms2[key]
    return ms

def MultisetEqual(ms1: OrderedDict, ms2: OrderedDict): #ms1 =? ms2
    if len(ms1) != len(ms2):
        return False
    for key in ms1: #even different copies (different addresses in memory) of the same term will be properly handled by OrderedDict.
        if not key in ms2:
            return False
        elif ms1[key] != ms2[key]:
            return False
    return True

def MultisetIntersection(ms1: OrderedDict, ms2: OrderedDict): #ms1 \cap ms2
    ms = OrderedDict()
    for key in ms2:
        if key in ms1:
            ms[key] = min(ms1[key], ms2[key])
    return ms

def MultisetEmpty(ms: OrderedDict):
    return len(ms) == 0

def MultisetPop(ms1: OrderedDict, key1): #it returns a new deep copy
    ms = deepcopy(ms1)
    ms.pop(key1)
    return ms

def PrintMultiset(ms1: OrderedDict):
    for item in ms1:
        mult = ms1[item]
        if isinstance(item, Term):
            print(item.ToString() + ':' + str(mult), end = ' ')
        else:
            print(item + ':' + str(mult), end = ' ')
    print()