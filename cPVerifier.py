#cP verifier

from copy import deepcopy
from cpsystem import CPSystem
from rule import Rule
from term import Term
import random as rd
import lnmu
from cpsystemsupport import ValidSystemTerm
import itertools

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
        
    def ToString(self):
        str_node = 'State: ' + self.state + '\n'
        if self.is_committed:
            str_node += 'Commited to: ' + self.committed_state + '\n'
        str_node += 'Terms:\n'
        for item in self.terms:
            if isinstance(item, Term):
                str_node += item.ToString() + ": " + str(self.terms[item]) + '\n'
            else:
                str_node += item + ": " + str(self.terms[item]) + '\n'
        if len(self.products) > 0:
            str_node += 'Virtual products:\n'
            for item in self.products:
                if isinstance(item, Term):
                    str_node += item.ToString() + ": " + str(self.products[item]) + '\n'
                else:
                    str_node += item + ": " + str(self.products[item]) + '\n'
        return str_node
    
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
        if rules_skipped >= len(self.rules): #node terminated, all rules are skipped (not applicable)
            self.node_list.pop()
            new_rules_skipped = 0
            new_limit -= 1
        nodes_left = len(self.node_list)
        if nodes_left <= 0: #verification finished, all nodes checked
            return False
        
        conf1 = self.node_list[nodes_left-1] #depth-first: deal with the last node
        print('Expanding node ' + str(10001-limit)  + ':\n' + conf1.ToString())

        terms = conf1.terms
        products = conf1.products
        state = conf1.state
        committed_state = conf1.committed_state
        is_committed = conf1.is_committed
        current_rule_index = conf1.next_rule_index
        r1 = self.rules[current_rule_index]
        next_rule_index = self.GetNextRuleIndex(current_rule_index)
        
        self.node_list.pop()
        
        #1
        if (r1.LState() != state) or (is_committed and r1.RState() != committed_state): #rule is not applicable, go to next rule
            if next_rule_index == 0:
                is_committed = False
                state = committed_state
                for item1 in products:
                    if item1 in terms:
                        terms[item1] += products[item1]
                    else:
                        terms[item1] = products[item1]
                products = {}    
            new_node = CPNode()
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
            self.node_list.append(new_node)
            self.Next(new_rules_skipped+1, new_limit)
        
        #2
        elif len(r1.LHS()) == 0 and len(r1.PMT()) == 0: #no lhs and promoter, success, no diff between 1 and +
            self.VProduceMultiset(products, r1.RHS())
            if not is_committed:
                is_committed = True
                committed_state = r1.RState()
            if next_rule_index == 0:
                is_committed = False
                state = committed_state
                for item1 in products:
                    if item1 in terms:
                        terms[item1] += products[item1]
                    else:
                        terms[item1] = products[item1]
                products = {}
            new_node = CPNode()
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
            self.node_list.append(new_node)
            self.Next(0, new_limit)
        
        #3
        elif r1.IsGround(): #no need to unify
            if r1.Model() == '1':
                ms_to_check = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
                if lnmu.MultisetIn(ms_to_check, terms): #rule applicable
                    self.VConsumeMultiset(terms, r1.LHS())
                    self.VProduceMultiset(products, r1.RHS())
                    if not is_committed:
                        is_committed = True
                        committed_state = r1.RState()
                    if next_rule_index == 0:
                        is_committed = False
                        state = committed_state
                        for item1 in products:
                            if item1 in terms:
                                terms[item1] += products[item1]
                            else:
                                terms[item1] = products[item1]
                        products = {}
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(0, new_limit)
                    
                else: #rule not applicable
                    if next_rule_index == 0:
                        is_committed = False
                        state = committed_state
                        for item1 in products:
                            if item1 in terms:
                                terms[item1] += products[item1]
                            else:
                                terms[item1] = products[item1]
                        products = {} 
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
                    if next_rule_index == 0:
                        is_committed = False
                        state = committed_state
                        for item1 in products:
                            if item1 in terms:
                                terms[item1] += products[item1]
                            else:
                                terms[item1] = products[item1]
                        products = {} 
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(new_rules_skipped+1, new_limit)
                else:
                    mult -= 1
                    self.VConsumeMultiset(terms, lnmu.MultisetTimes(r1.LHS(), mult))
                    self.VProduceMultiset(products, lnmu.MultisetTimes(r1.RHS(), mult))
                    if not is_committed:
                        is_committed = True
                        committed_state = r1.RState()
                    if next_rule_index == 0:
                        is_committed = False
                        state = committed_state
                        for item1 in products:
                            if item1 in terms:
                                terms[item1] += products[item1]
                            else:
                                terms[item1] = products[item1]
                        products = {} 
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(0, new_limit)
        
        #4           
        elif (not is_committed) or (is_committed and r1.RState() == committed_state): #a rule with variables
            ms_to_process = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
            G = []
            G.append((ms_to_process, terms, 'in')) #items in a rule's LHS and PMT are included in terms
            SS = [] #the set of unifiers
            S = {}
            lnmu.LNMU(G, S, SS)
            
            if len(SS) == 0: #unification failed
                if next_rule_index == 0:
                    is_committed = False
                    state = committed_state
                    for item1 in products:
                        if item1 in terms:
                            terms[item1] += products[item1]
                        else:
                            terms[item1] = products[item1]
                    products = {} 
                new_node = CPNode()
                new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                self.node_list.append(new_node)
                self.Next(new_rules_skipped+1, new_limit)
                
            else:
                if r1.Model() == '1': #exact-once model, non-deterministically apply it once
                    for unifier in SS:
                        lhs2 = lnmu.ApplyBindingMultiset(r1.LHS(), unifier)
                        rhs2 = lnmu.ApplyBindingMultiset(r1.RHS(), unifier)
                        pmt2 = lnmu.ApplyBindingMultiset(r1.PMT(), unifier)
                        r2 = Rule(r1.LState(), r1.RState(), '1') #a unified, ground rule
                        r2.SetLHS(lhs2)
                        r2.SetRHS(rhs2)
                        r2.SetPMT(pmt2)
                        if r2.IsGround():
                            terms2 = deepcopy(terms)
                            products2 = deepcopy(products)
                            ms_to_check = lnmu.MultisetUnion(r2.PMT(), r2.LHS())
                            rule_applied = False
                            is_committed2 = is_committed
                            committed_state2 = committed_state
                            state2 = state
                            if lnmu.MultisetIn(ms_to_check, terms2): #rule applicable
                                self.VConsumeMultiset(terms2, r2.LHS())
                                self.VProduceMultiset(products2, r2.RHS())
                                rule_applied = True      
                            if rule_applied:
                                if not is_committed2:
                                    is_committed2 = True
                                    committed_state2 = r2.RState()
                                if next_rule_index == 0:
                                    is_committed2 = False
                                    state2 = committed_state2
                                    for item1 in products2:
                                        if item1 in terms2:
                                            terms2[item1] += products2[item1]
                                        else:
                                            terms2[item1] = products2[item1]
                                    products2 = {}
                                new_node = CPNode()
                                new_node.ReadContent(terms2, products2, state2, committed_state2, is_committed2, next_rule_index)
                                self.node_list.append(new_node)
                                self.Next(0, new_limit)
                            else: #fail
                                new_node = CPNode()
                                new_node.ReadContent(terms2, products2, state, committed_state, is_committed, next_rule_index)
                                self.node_list.append(new_node)
                                self.Next(new_rules_skipped+1, new_limit)
                        else: #fail, should not happen
                            new_node = CPNode()
                            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                            self.node_list.append(new_node)
                            self.Next(new_rules_skipped+1, new_limit)
                        
                elif r1.Model() == '+': #max-parallel model
                    p_SS = list(itertools.permutations(SS))
                    success = False
                    for s_SS in p_SS:
                        ruleset = []
                        for unifier in s_SS:
                            lhs2 = lnmu.ApplyBindingMultiset(r1.LHS(), unifier)
                            rhs2 = lnmu.ApplyBindingMultiset(r1.RHS(), unifier)
                            pmt2 = lnmu.ApplyBindingMultiset(r1.PMT(), unifier)
                            r2 = Rule(r1.LState(), r1.RState(), '+') #a unified, ground rule
                            r2.SetLHS(lhs2)
                            r2.SetRHS(rhs2)
                            r2.SetPMT(pmt2)
                            if r2.IsGround():
                                ruleset.append(r2)
                        terms2 = deepcopy(terms)
                        products2 = deepcopy(products)
                        is_committed2 = is_committed
                        committed_state2 = committed_state
                        state2 = state
                        rule_applied = False
                        for r3 in ruleset:
                            ms_to_check = lnmu.MultisetUnion(r3.PMT(), r3.LHS())
                            if lnmu.MultisetIn(ms_to_check, terms2): #rule applicable
                                self.VConsumeMultiset(terms2, r2.LHS())
                                self.VProduceMultiset(products2, r2.RHS())
                                rule_applied = True
                                success = True
                        if rule_applied:
                            if not is_committed2:
                                is_committed2 = True
                                committed_state2 = r2.RState()
                            if next_rule_index == 0:
                                is_committed2 = False
                                state2 = committed_state2
                                for item1 in products2:
                                    if item1 in terms2:
                                        terms2[item1] += products2[item1]
                                    else:
                                        terms2[item1] = products2[item1]
                                products2 = {}
                            new_node = CPNode()
                            new_node.ReadContent(terms2, products2, state2, committed_state2, is_committed2, next_rule_index)
                            self.node_list.append(new_node)
                    if success:
                        self.Next(0, new_limit)
                    else:
                        new_node = CPNode()
                        new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                        self.node_list.append(new_node)
                        self.Next(new_rules_skipped+1, new_limit)          
                else: #currently cP systems only have 2 major models, '1' and '+'
                    print('Incorrect application model!')
                    return False
        return True
            
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