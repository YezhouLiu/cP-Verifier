#cP Systems

from copy import deepcopy
from rule import Rule
from term import Term
import random as rd
import time
from cpsystemsupport import ValidSystemTerm
import lnmu

#MODULE cP
class CPSystem:
    def __init__(self, state = 's0'):
        self.rules = [] #rules follow a weak-priority order
        self.state = state #'s0' 's1' 's2' ...
        self.terms = {} #system terms, must be ground, atom or term, no need to sort them
        self.products = {} #a virtual product membrane
        self.committed_state = state
        self.is_committed = False
        self.show_detail = False

#STATE
#------------------------------------------------------------------------------
    def State(self):
        return self.state

    def SetState(self, state):
        self.state = state
        
    def CommittedState(self):
        return self.committed_state
    
    def SetCommittedState(self, state):
        self.committed_state = state
        
    def IsCommitted(self):
        return self.is_committed
    
    def SetIsCommitted(self, b1):
        self.is_committed = b1

#SHOW DETAIL
#------------------------------------------------------------------------------
    def DetailOn(self):
        self.show_detail = True

    def DetailOff(self):
        self.show_detail = False

#SYSTEM TERM
#------------------------------------------------------------------------------
    def SystemTerms(self):
        return self.terms

    def AddSystemTerm(self, t1, count = 1):
        if ValidSystemTerm(t1):
            if t1 in self.terms:
                self.terms[t1] += count
            else: 
                self.terms[t1] = count
        elif self.show_detail:
            print('Invalid system term, please check!')

    def AddSystemMultiset(self, m1):
        for t1 in m1:
            mult = m1[t1]
            self.AddSystemTerm(t1, mult)        

    def ConsumeTerm(self, t1, count = 1):
        if count < 1:
            return False
        if not t1 in self.terms:
            if self.show_detail:
                if isinstance(t1, Term):
                    print('There is no ' + t1.ToString() + ' in the cP system!')
                elif t1 >= 'a' and t1 <= 'z':
                    print('There is no ' + t1 + ' in the cP system!')
                else:
                    print('Invalid system term, which cannot be consumed!')
            return False
        elif self.terms[t1] >= count: 
            self.terms[t1] -= count
            if self.terms[t1] == 0:
                self.terms.pop(t1)
            if self.show_detail:
                if isinstance(t1, Term):
                    if count == 1:
                        print('1 copy of ' + t1.ToString() + ' is consumed! ')
                    else:
                        print(str(count) + ' copies of ' + t1.ToString() + ' are consumed!')
                else:
                    if count == 1:
                        print('1 copy of ' + t1 + ' is consumed! ')
                    else:
                        print(str(count) + ' copies of ' + t1 + ' are consumed!')
            return True
        else:
            if self.show_detail:
                print('Insufficient terms in the system!')
            return False

    def ConsumeMultiset(self, m1):
        for t1 in m1:
            mult = m1[t1]
            self.ConsumeTerm(t1, mult)

#PRODUCT MEMBRANE
#------------------------------------------------------------------------------
    def ProduceTerm(self, t1, count = 1):
        if count < 1:
            return False
        if ValidSystemTerm(t1):
            if t1 in self.products:
                self.products[t1] += count
            else: 
                self.products[t1] = count
            if self.show_detail:
                if isinstance(t1, Term):
                    if count == 1:
                        print('1 copy of ' + t1.ToString() + ' is produced! ')
                    else:
                        print(str(count) + ' copies of ' + t1.ToString() + ' are produced!')
                else:
                    if count == 1:
                        print('1 copy of ' + t1 + ' is produced! ')
                    else:
                        print(str(count) + ' copies of ' + t1 + ' are produced!')
            return True
        elif self.show_detail:
            print('Invalid product, please check!')
        return False

    def ProduceMultiset(self, m1):
        for t1 in m1:
            mult = m1[t1]
            self.ProduceTerm(t1, mult)

    def CleanProductMembrane(self):
        self.products = {}

#RULE
#------------------------------------------------------------------------------
    def AddRule(self, r1):
        if r1.IsValid():
            self.rules.append(r1)
            if self.show_detail:
                print('The rule: ' + r1.ToString() + ' is added to the cP system!')
            return True
        elif self.show_detail:
            print('Invalid rule!')
        return False
    
    def AddRuleset(self, list_of_rules):
        for r1 in list_of_rules:
            self.AddRule(r1)
            
    def Rules(self):
        return self.rules

#RULE APPLICATION
#------------------------------------------------------------------------------
    def ApplyARule(self, r1: Rule, is_committed = False): 
        if self.show_detail:
            if not r1.IsGround():
                print('Trying the rule: ' + r1.ToString())
            else:
                print('Ground (unified) rule: ' + r1.ToString())
        if r1.LState() != self.state:
            if self.show_detail:
                print('State unmatched, the rule is not applicable!')
            return False
        elif is_committed and r1.RState() != self.committed_state:
            if self.show_detail:
                print('State unmatched, the rule is not applicable!')
            return False
        elif len(r1.LHS()) == 0 and len(r1.PMT()) == 0: #no lhs and promoter, success, directly generate products
            self.ProduceMultiset(r1.RHS())
            return True
        elif r1.IsGround(): #no need to unify
            if r1.Model() == '1':
                ms_to_check = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
                if lnmu.MultisetIn(ms_to_check, self.terms):
                    self.ConsumeMultiset(r1.LHS())
                    self.ProduceMultiset(r1.RHS())
                    return True
                else:
                    if self.show_detail:
                        print('Insufficient terms, the rule is not applicable!')
                    return False
            else: #model = '+'
                ms_to_check = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
                ms_to_check_2 = deepcopy(ms_to_check)
                mult = 1
                while lnmu.MultisetIn(ms_to_check_2, self.terms):
                    mult += 1
                    ms_to_check_2 = lnmu.MultisetTimes(ms_to_check, mult)
                if mult == 1:
                    if self.show_detail:
                        print('Insufficient terms, the rule is not applicable!')
                    return False
                else:
                    mult -= 1
                    self.ConsumeMultiset(lnmu.MultisetTimes(r1.LHS(), mult))
                    self.ProduceMultiset(lnmu.MultisetTimes(r1.RHS(), mult))
                    return True
        elif (not is_committed) or (is_committed and r1.RState() == self.committed_state): #a rule with variables
            ms_to_process = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
            G = []
            G.append((ms_to_process, self.terms, 'in')) #items in a rule's LHS and PMT are included in the system
            SS = [] #the set of unifiers
            S = {}
            lnmu.LNMU(G, S, SS)
            if len(SS) == 0:
                if self.show_detail:
                    print('Insufficient terms, the rule is not applicable!')
                return False
            else:
                if r1.Model() == '1': #exact-once model, non-deterministically apply it once
                    num_g_rules = len(SS)
                    rd_rule = rd.randint(0, num_g_rules - 1)
                    unifier = SS[rd_rule]
                    lhs2 = lnmu.ApplyBindingMultiset(r1.LHS(), unifier)
                    rhs2 = lnmu.ApplyBindingMultiset(r1.RHS(), unifier)
                    pmt2 = lnmu.ApplyBindingMultiset(r1.PMT(), unifier)
                    r2 = Rule(r1.LState(), r1.RState(), '1') #a unified, ground rule
                    r2.SetLHS(lhs2)
                    r2.SetRHS(rhs2)
                    r2.SetPMT(pmt2)
                    if r2.IsGround():
                        return self.ApplyARule(r2)
                    else:
                        return False
                elif r1.Model() == '+': #max-parallel model
                    rd.shuffle(SS) #no need to keep original SS
                    ruleset = []
                    for unifier in SS:
                        lhs2 = lnmu.ApplyBindingMultiset(r1.LHS(), unifier)
                        rhs2 = lnmu.ApplyBindingMultiset(r1.RHS(), unifier)
                        pmt2 = lnmu.ApplyBindingMultiset(r1.PMT(), unifier)
                        r2 = Rule(r1.LState(), r1.RState(), '+') #a unified, ground rule
                        r2.SetLHS(lhs2)
                        r2.SetRHS(rhs2)
                        r2.SetPMT(pmt2)
                        if r2.IsGround():
                            ruleset.append(r2)
                    return self.ApplyGRules(ruleset)
                else: #currently cP systems only have 2 major models, '1' and '+'
                    return False

    def ApplyGRules(self, ruleset): #stateless
        succ = False
        for r1 in ruleset:
            if self.ApplyARule(r1):
                succ = True
        return succ

    def ApplyARuleset(self, ruleset):
        self.committed_state = self.state
        self.is_committed = False
        for r1 in ruleset:
            if (not self.is_committed) and self.ApplyARule(r1):
                self.is_committed = True
                self.committed_state = r1.RState()
            elif self.is_committed:
                self.ApplyARule(r1, True)
        self.StepOver()
        self.Snapshot()
        if self.is_committed:
            return True
        else: #no rule was applied
            return False

    def StepOver (self): #move to the next step, activate terms in product membrane
        self.state = self.committed_state
        for item1 in self.products:
            if item1 in self.terms:
                self.terms[item1] += self.products[item1]
            else:
                self.terms[item1] = self.products[item1]
        self.products = {}

    def Run(self, steps = 20):
        i = 0
        while (self.ApplyARuleset(self.rules) and i < steps):
            i += 1

#SYSTEM DISPLAY
#------------------------------------------------------------------------------
    def Snapshot(self): 
        print('\n\n--------------------------------------------------------')
        print('System state: ', self.state)
        print('Terms in the system:')
        for item in self.terms:
            if isinstance(item, Term):
                print(item.ToString() + ': ' + str(self.terms[item]))
            else:
                print(item+ ': ' + str(self.terms[item]))
        print('--------------------------------------------------------\n\n')

    def ToString(self):
        str_system = ''
        for rule in self.rules:
            str_system += rule.ToString() + '\n'
        str_system += 'State: ' + self.state + '\n'
        str_system += 'Commited to: ' + self.committed_state + '\n'
        str_system += 'Terms:\n'
        for item in self.terms:
            if isinstance(item, Term):
                str_system += item.ToString() + ": " + str(self.terms[item]) + '\n'
            else:
                str_system += item + ": " + str(self.terms[item]) + '\n'
        if len(self.products) > 0:
            str_system += 'Virtual products:\n'
            for item in self.products:
                if isinstance(item, Term):
                    str_system += item.ToString() + ": " + str(self.products[item]) + '\n'
                else:
                    str_system += item + ": " + str(self.products[item]) + '\n'
        return str_system