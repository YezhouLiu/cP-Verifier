#cP verifier

from copy import deepcopy
from cpsystem import CPSystem
from rule import Rule
import random as rd
import lnmu

class CPChecker:
    def __init__(self):
        #self.properties = {} #1: deadlock, #2: nondeterministic, #3: confluent
        #self.results ={} #1: true, 2: false, 3: false
        self.one_property = []
        
        self.trace = [] #conf1 -> conf2 -> conf3
        
    def Check(self):
        pass
    
    def CheckOne(self, sys1: CPSystem, current_rule_index: int, trace):
        #check properties here
        
        #Here we check the system by each rule application rather than each cP step
        if (not self.system.IsCommitted()) and self.ExpandOneRule(sys1.Rules()[current_rule_index], sys1.IsCommitted()):
            pass
        
        pass
    
    def ExpandOneRule(self):
        pass
    
    def GetNextRuleIndex(self, curr):
        if curr < len(self.ruleset) - 1:
            return curr + 1
        else:
            return 0
        
    def ExpandOneRule(self, r1: Rule, is_committed = False): 
        if r1.LState() != self.state:
            return False
        elif is_committed and r1.RState() != self.committed_state:
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
                    return False
            else: #model = '+'
                ms_to_check = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
                ms_to_check_2 = deepcopy(ms_to_check)
                mult = 1
                while lnmu.MultisetIn(ms_to_check_2, self.terms):
                    mult += 1
                    ms_to_check_2 = lnmu.MultisetTimes(ms_to_check, mult)
                if mult == 1:
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