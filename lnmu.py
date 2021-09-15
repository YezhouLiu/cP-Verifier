#computing engine - Yezhou

from copy import deepcopy
from term import Term
from collections import OrderedDict

#UNIFICATION
#------------------------------------------------------------------------------
def UnifyTerms(tv: Term, tg: Term): #tv: variable term, tg: ground term, return value: substitutions + token, which indicates that unification succeeds or fails 
    substitutions = {}
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
    SS = {} #the set of unifiers
    S = {} #current substitution
    return LNMU(G, S, SS)

def LNMU(G, S, SS): #G: set G, all working equations; SS: all substitutions, S: current subtitution
    #process current G
    new_G = []
    for equation in G:
        mv_temp = equation[0] #lhs, mv
        mg_temp = equation[1] #rhs, mg
        mv, mg = GROUND(mv_temp, mg_temp) #apply ground
        if FAIL1(mv, mg) or FAIL2(mv, mg):
            return False
        if can_be_DELETED(mv, mg): #the equation is lambda = lambda
            continue
        elif len(mv) == 0: #fail when lambda = something
            return False
        else:
            new_G.append((mv,mg))
    if len(new_G) == 0: #success, all the equations are solved
        SS.add(S)
        return True

    (mv, mg) = new_G[0] #deal with the first equation
    if len(mv) == 1: #lhs only contains one kind of variable, apply VARIABLE
        for t1 in mv: 
            if t1 >= 'A' and t1 <= 'Z': #t1 is a variable
                for t2 in mg:
                    if mg[t2] % mv[t1] != 0: #fail, f(X)f(X) = f(a)f(a)f(a)
                        return False 
                    else:
                        S1 = deepcopy(S)
                        S1[t2] = mg[t2] / mv[t1] # apply it to G1
                        G1 = new_G[1:]

                        #xxx

                        LNMU(new_G[1:], S1, SS) #shallow copy can be used here
            elif isinstance(t1, Term):
                if len(mg) > 1: #fail, f(X) = f(a)g(b)
                    return False 
                for t2 in mg: #the only term in mg, f(XY) = f(abc)
                    if t1.Label() == t2.Label() and mv[t1] == mg[t2]: #same label and multiplicity
                        G1 = new_G[1:] #shallow copy can be used here
                        G1.append((t1.Subterms(), t2.Subterms())) #get rid of functors, XY = abc
                        return LNMU(G1, S, SS)
                    else: #fail, f(X) = g(ab)
                        return False
            else: #which should not happen
                return False
    elif HasCompoundSubterms(mv): #mv contains functors (compound terms), apply FUNCTOR
        for t1 in mv:
            for t2 in mg:
                if isinstance(t1, Term) and isinstance(t2, Term) and t1.Label() == t2.Label() and mv[t1] == mv[t2]: #same multiplicity
                    G1 = deepcopy(new_G[1:])
                    G1.append((t1.Subterms(), t2.Subterms()))
                    G1.append((MultisetPop(mv, t1), MultisetPop(mg, t2)))
                    return LNMU(G1, S, SS)
    else: #mv contains no functor but only variables, apply VARIABLE
        #XXY = f(a)bbccccc, X -> lambda, b, c, bc, cc, bcc
        for t1 in mv: #only deal with one variable at a time
            if t1 >= 'A' and t1 <= 'Z':
                pass
            else: #which should not happen
                return False
        pass

    #apply_binding
    

def FUNCTOR(mv, mg, G): #return all pairs of equations, deterministic
    all_equations = []
    for t1 in mv:
        for t2 in mg:
            if isinstance(t1, Term) and isinstance(t2, Term) and t1.Label() == t2.Label() and mv[t1] == mv[t2]: #same multiplicity
                mv_temp = t1.Subterms()
                mg_temp = t2.Subterms()
                mv1, mg1 = GROUND(mv_temp, mg_temp)
                if FAIL1(mv1, mg1) or FAIL2(mv1, mg1):
                    continue
                else:
                    equation_1 = (mv1, mg1)
                    equation_2 = (MultisetPop(mv, t1), MultisetPop(mg, t2))
                    all_equations.append((equation_1, equation_2))
    return all_equations

def can_be_DELETED(mv, mg):
    if len(mv) == 0 and len(mg) == 0:
        return True
    else:
        return False 

def FAIL1(mv, mg): #true: fail, false: succeed
    for t1 in mv:
        if t1 not in mg:
            if isinstance(t1, Term) and t1.IsGround(): #t1 a is ground term
                return True
            elif t1 < 'A' or t1 > 'Z': #t1 is ground/ not a var
                return True
    return False

def FAIL2(mv, mg): #true: fail, false: succeed
    if MultisetInclusion(Functors(mg), Functors(mv)):
        return False
    else:
        return True

def Functors(m):
    labels = {}
    for term in m:
        if isinstance(term, Term):
            if term.Label() in labels:
                labels[term.Label()] += 1
            else:
                labels[term.Label()] = 1
    return labels

def GROUND(ms1, ms2): #return two multisets, optimize it later as needed
    mi = MultisetIntersection(ms1, ms2)
    return MultisetMinus(ms1, mi), MultisetMinus(ms2, mi)

def HasCompoundSubterms(mv):
    for s in mv.Subterms():
        if isinstance(s, Term):
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