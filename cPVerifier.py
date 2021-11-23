#cP verifier

from copy import deepcopy
from cpsystem import CPSystem
from rule import Rule
from term import Term
import random as rd
import lnmu
from cpsystemsupport import ValidSystemTerm

class CPNode:
    def __init__(self):
        self.terms = {}
        self.products = {}
        self.state = ''
        self.committed_state = ''
        self.is_committed = False
        self.next_rule_index = 0
        
    def ReadCP(self, sys1: CPSystem):
        self.terms = sys1.SystemTerms()
        self.state = sys1.State()
        self.committed_state = sys1.State()
        
    def ReadContent(self, terms, products, state, committed_state, is_committed, next_rule_index):
        self.terms = terms
        self.products = products
        self.state = state
        self.committed_state = committed_state
        self.is_committed = is_committed
        self.next_rule_index = next_rule_index

class CPVerifier:
    def __init__(self, sys1: CPSystem):
        node = CPNode()
        node.ReadCP(sys1)
        self.node_list = [node]
        self.show_detail = False
        self.rules = sys1.Rules()
        
    def GetNextRuleIndex(self, current_rule_index):
        if current_rule_index < len(self.rules) - 1:
            return current_rule_index + 1
        else:
            return 0
        
    def Next(self, rules_skipped = 0, limit = 10000):
        if limit == 0: #verfication limit reached
            print("Verification limit reached!")
            return False
        new_limit = limit - 1
        new_rules_skipped = rules_skipped
        if rules_skipped == len(self.rules): #node terminated, all rules are skipped (not applicable)
            self.node_list.pop()
            new_rules_skipped = 0
            new_limit -= 1
        nodes_left = len(self.node_list)
        if nodes_left <= 0: #verification finished, all nodes checked
            return False
        
        conf1 = self.node_list[nodes_left-1] #depth-first: deal with the last node

        terms = conf1.terms
        products = conf1.products
        state = conf1.state
        committed_state = conf1.committed_state
        is_committed = conf1.is_committed
        current_rule_index = conf1.next_rule_index
        r1 = self.rules[current_rule_index]
        next_rule_index = self.GetNextRuleIndex(current_rule_index)
        
        self.node_list.pop()
        
        if (r1.LState() != self.state) or (is_committed and r1.RState() != self.committed_state): #rule is not applicable, go to next rule
            if self.show_detail:
                print('State unmatched, the rule ' + r1.ToString() + ' is not applicable!')
            new_node = CPNode()
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
            self.node_list.append(new_node)
            self.Next(new_rules_skipped+1, new_limit)
        
        elif len(r1.LHS()) == 0 and len(r1.PMT()) == 0: #no lhs and promoter, success, no diff between 1 and +
            self.VProduceMultiset(products, r1.RHS())
            new_node = CPNode()
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
            self.node_list.append(new_node)
            self.Next(0, new_limit)
        
        elif r1.IsGround(): #no need to unify
            if r1.Model() == '1':
                ms_to_check = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
                if lnmu.MultisetIn(ms_to_check, terms): #rule applicable
                    self.VConsumeMultiset(terms, r1.LHS())
                    self.VProduceMultiset(products, r1.RHS())
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(0, new_limit)
                else: #rule not applicable
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(new_rules_skipped+1, new_limit)
            else: #model = '+'
                ms_to_check = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
                ms_to_check_2 = deepcopy(ms_to_check)
                mult = 1
                while lnmu.MultisetIn(ms_to_check_2, terms):
                    mult += 1
                    ms_to_check_2 = lnmu.MultisetTimes(ms_to_check, mult)
                if mult == 1: #insufficient terms, rule not applicable
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(new_rules_skipped+1, new_limit)
                else:
                    mult -= 1
                    self.VConsumeMultiset(terms, lnmu.MultisetTimes(r1.LHS(), mult))
                    self.VProduceMultiset(products, lnmu.MultisetTimes(r1.RHS(), mult))
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(0, new_limit)
                    
        elif (not is_committed) or (is_committed and r1.RState() == committed_state): #a rule with variables
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
        
        return True
        
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

    def VerifyGRules(self, ruleset): #stateless
        succ = False
        for r1 in ruleset:
            if self.ApplyARule(r1):
                succ = True
        return succ

    def VerifyARuleset(self, ruleset):
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

    def VStepOver (self): #move to the next step, activate terms in product membrane
        self.state = self.committed_state
        for item1 in self.products:
            if item1 in self.terms:
                self.terms[item1] += self.products[item1]
            else:
                self.terms[item1] = self.products[item1]
        self.products = {}

    def Verify(self, steps = 100):
        i = 0
        while (self.ApplyARuleset(self.rules) and i < steps):
            i += 1
        if i == steps:
            print("The step limit is reached, which is " + str(steps) + '.')
            
    def VConsumeTerm(self, terms, t1, count = 1): #terms passed by reference
        if count < 1:
            return False
        if not t1 in terms:
            return False
        elif terms[t1] >= count: 
            terms[t1] -= count
            if terms[t1] == 0:
                terms.pop(t1)
            return True
        else:
            return False

    def VConsumeMultiset(self, terms, m1): #terms passed by reference
        for t1 in m1:
            mult = m1[t1]
            self.VConsumeTerm(terms, t1, mult)
            
    def VProduceTerm(self, products, t1, count = 1):
        if count < 1:
            return False
        if ValidSystemTerm(t1):
            if t1 in products:
                products[t1] += count
            else: 
                products[t1] = count
            return True
        else:
            return False

    def VProduceMultiset(self, products, m1):
        for t1 in m1:
            mult = m1[t1]
            self.VProduceTerm(products, t1, mult)