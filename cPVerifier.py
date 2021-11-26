#cP verifier

from copy import deepcopy
from cpsystem import CPSystem
from rule import Rule
from term import Term
import random as rd
import lnmu
from cpsystemsupport import ValidSystemTerm
import itertools
from typing import List, OrderedDict

class CPNode:
    def __init__(self):
        self.terms = {}
        self.products = {}
        self.state = ''
        self.committed_state = ''
        self.is_committed = False
        self.next_rule_index = 0
    
    #HASH
    #------------------------------------------------------------------------------
    def __eq__(self, node2): 
        if not isinstance(node2, CPNode): # compare cp nodes only
            return False
        return self.ToString() == node2.ToString()
    def __lt__(self, node2): #less than
        if not isinstance(node2, CPNode):
            return False
        return self.ToString() < node2.ToString()
    def __hash__(self):
        return hash(self.ToString())
        
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
        str_node += 'Next rule: ' + str(self.next_rule_index) + '\n'
        return str_node
    
class CPVerifier:
    def __init__(self, sys1: CPSystem):
        node = CPNode()
        node.ReadCP(sys1)
        self.node_list = [node]
        self.show_detail = False
        self.rules = sys1.Rules()
        self.terminations = []
        self.search_method = 'DFS'
        self.state_limit = 100000
        self.state_checked = 0
        self.property_code = 0
        self.counter_example_found = False
        self.counter_example = CPNode()
        self.goal = {}
        self.goal_state = ''
        self.reachable_state = ''
        self.termination_set = set()
#Property code
#0: If certain goal terms are included in ALL halting configurations
#1: If a goal state is reachable
#2: If the cP system is deterministic
#3: If the cP system is deadlockfree
#4: If the cP system is confluent
        
    def SetTerminations(self, terminations: List[str]):
        self.terminations = terminations
        
    def GetNextRuleIndex(self, current_rule_index: int):
        if current_rule_index < len(self.rules) - 1:
            return current_rule_index + 1
        else:
            return 0
        
    def SetSearchMethod(self, sm: str):
        if sm == 'DFS' or 'BFS':
            self.search_method = sm
            
    def DetailOn(self):
        self.show_detail = True
        
    def DetailOff(self):
        self.show_detail = False
        
    def SetGoalTerms(self, goal: OrderedDict[Term, int]):
        self.goal = goal
        
    def SetGoalState(self, goal: str):
        self.goal_state = goal
        
    def SetReachableState(self, state: str):
        self.reachable_state = state

    def Verify(self, property_code = 0, state_limit = 100000):
        self.state_limit = state_limit
        self.property_code = property_code
        self.Next()
        print('The cP system verification is finished, totally ' + str(self.state_checked) + ' states were checked.\n')
        if self.counter_example_found:
            if self.property_code == 0:
                print('The following counter example is found: \n' + self.counter_example.ToString())
            elif self.property_code == 1:
                print('The goal state ' + self.goal_state + ' is reached!\n' + self.counter_example.ToString())
            elif self.property_code == 2:
                print('The cP system is nondeterministic!')
            elif self.property_code == 3:
                print('A deadlock state is found!\n' + self.counter_example.ToString())
            elif self.property_code == 4:
                print('The cP system is not confluent! Different halting configuration can be found!')
                self.PrintTerminationSet()
            
        else:
            if self.property_code == 0:
                print('The goal terms cannot be found in the cP system, the property is not held!')
            elif self.property_code == 1:
                print('The goal state ' + self.goal_state + ' is not reachable!')
            elif self.property_code == 2:
                print('The cP system is deterministic!')
            elif self.property_code == 3:
                print('The cP system is deadlock free!')
            elif self.property_code == 4:
                print('The cP system is confluent!')
        
    def Next(self, rules_skipped = 0):
        if self.counter_example_found:
            return True
        
        if self.state_checked >= self.state_limit: #verfication limit reached
            print("Verification limit reached!")
            return False
        
        nodes_left = len(self.node_list)
        if nodes_left <= 0: #verification finished, all nodes checked
            return False
        
        conf1 = CPNode()
        if self.search_method == 'BFS':
            conf1 = self.node_list[0]
        else: #temporarily choose DFS
            conf1 = self.node_list[nodes_left-1]
        self.state_checked += 1
        if self.show_detail:
            print('********************\nState #' + str(self.state_checked)  + ':\n' + conf1.ToString() + '\n********************\n')
        
        new_rules_skipped = rules_skipped
        state = conf1.state
        terms = conf1.terms
        products = conf1.products
        committed_state = conf1.committed_state
        is_committed = conf1.is_committed
        current_rule_index = conf1.next_rule_index
        r1 = self.rules[current_rule_index]
        next_rule_index = self.GetNextRuleIndex(current_rule_index)
        
        if state in self.terminations:
            self.termination_set.add(conf1)
            if self.property_code == 0: #0: goal terms check
                if not lnmu.MultisetInclusion(terms, self.goal):
                    self.counter_example = conf1
                    self.counter_example_found = True
                    return True
            elif self.property_code == 1: #1: goal-state reached
                if state == self.goal_state:
                    self.counter_example = conf1
                    self.counter_example_found = True
                    return True
            elif self.property_code == 4: #: confluence check
                if len(self.termination_set) > 1:
                    self.counter_example_found = True
                    return True
                
        if (not state in self.terminations) and (rules_skipped >= len(self.rules)-1) and (self.property_code == 3):  #no ourgoing edge, not a expected termination
            self.counter_example = conf1
            self.counter_example_found = True
            return True           
        
        if self.search_method == 'BFS':
            self.node_list.pop(0)
        else:
            self.node_list.pop()
        
        if state in self.terminations or rules_skipped >= len(self.rules): #node terminated, termination reached or all rules are skipped (not applicable)
            self.Next()
            return False
            
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
                new_rules_skipped = -1  
            new_node = CPNode()
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
            self.node_list.append(new_node)
            self.Next(new_rules_skipped+1)
        
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
            self.Next()
        
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
                    self.Next()
                    
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
                        new_rules_skipped = -1 
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(new_rules_skipped+1)
                    
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
                        new_rules_skipped = -1 
                    new_node = CPNode()
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                    self.node_list.append(new_node)
                    self.Next(new_rules_skipped+1)
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
                    self.Next()
        
        #4           
        elif (not is_committed) or (is_committed and r1.RState() == committed_state): #a rule with variables
            ms_to_process = lnmu.MultisetUnion(r1.PMT(), r1.LHS())
            G = []
            G.append((ms_to_process, terms, 'in')) #items in a rule's LHS and PMT are included in terms
            SS = [] #the set of unifiers
            S = {}
            lnmu.LNMU(G, S, SS)
            if len(SS) > 1:
                self.nonedeterministic = True
                if self.property_code == 2:
                    self.counter_example_found = True
                    return True
            
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
                    new_rules_skipped = -1 
                new_node = CPNode()
                new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index)
                self.node_list.append(new_node)
                self.Next(new_rules_skipped+1)
                
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
                                self.Next()
                            else: #fail
                                return False
                        
                elif r1.Model() == '+': #max-parallel model
                    p_SS = list(itertools.permutations(SS))
                    #self.PrintP_SS(p_SS)
                    for s_SS in p_SS:
                        ruleset = set() #a set used to get rid of duplicated unified rules
                        for unifier in s_SS:
                            lhs2 = lnmu.ApplyBindingMultiset(r1.LHS(), unifier)
                            rhs2 = lnmu.ApplyBindingMultiset(r1.RHS(), unifier)
                            pmt2 = lnmu.ApplyBindingMultiset(r1.PMT(), unifier)
                            r2 = Rule(r1.LState(), r1.RState(), '+') #a unified, ground rule
                            r2.SetLHS(lhs2)
                            r2.SetRHS(rhs2)
                            r2.SetPMT(pmt2)
                            if r2.IsGround():
                                ruleset.add(r2)
                        for r3 in ruleset:
                            terms2 = deepcopy(terms)
                            products2 = deepcopy(products)
                            is_committed2 = is_committed
                            committed_state2 = committed_state
                            state2 = state
                            ms_to_check = lnmu.MultisetUnion(r3.PMT(), r3.LHS())
                            if lnmu.MultisetIn(ms_to_check, terms2): #rule applicable
                                self.VConsumeMultiset(terms2, r3.LHS())
                                self.VProduceMultiset(products2, r3.RHS())
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
                        self.Next()        
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
            
    def ToString(self):
        str_cpv = 'Nodes:\n'
        for node in self.node_list:
            str_cpv += '***************************\n'
            str_cpv += node.ToString() + '\n'
        str_cpv += '***************************\nRules:\n'
        str_cpv += '***************************\n'
        for rule in self.rules:
            str_cpv += rule.ToString() + '\n'
        str_cpv += '***************************\n'
        return str_cpv
    
    def PrintNodeList(self):
        str_cpv = 'Nodes:\n'
        for node in self.node_list:
            str_cpv += '***************************\n'
            str_cpv += node.ToString() + '\n'
        str_cpv += '***************************\n'
        print(str_cpv)
        
    def PrintTerminationSet(self):
        str_cpv = 'Halting configurations:\n'
        for node in self.termination_set:
            str_cpv += '***************************\n'
            str_cpv += node.ToString() + '\n'
        str_cpv += '***************************\n'
        print(str_cpv)
    
    def Print(self):
        print(self.ToString())
        
    def PrintP_SS(self, p_SS):
        for y in p_SS:
            for x in y:
                for key in x:
                    print('***************************')
                    print(key + ':')
                    for item in x[key]:
                        if isinstance(item, Term):
                            print(item.ToString() + ': '  + str(x[key][item]))
                        else:
                            print(item + ': ' + str(x[key][item]))
                    print('***************************')