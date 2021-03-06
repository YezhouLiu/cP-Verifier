#cP verifier

from copy import deepcopy
from cpsystem import CPSystem
from rule import Rule
from term import Term
import random as rd
import lnmu
from cpsystemsupport import ValidSystemTerm
from typing import List, OrderedDict
import heapq
import time

VERSION = 1.1

class CPNode:
    def __init__(self):
        self.terms = {}
        self.products = {}
        self.state = ''
        self.committed_state = ''
        self.is_committed = False
        self.next_rule_index = 0
        self.step = 0
        self.ancestors = [] #use string to make it smaller
        self.terminated = False
    
    #HASH
    #------------------------------------------------------------------------------
    def __eq__(self, node2): 
        if not isinstance(node2, CPNode): # compare cp nodes only
            return False
        return self.ToString() == node2.ToString()
    
    def __lt__(self, node2): #less than
        if not isinstance(node2, CPNode):
            return False
        if self.step != node2.step:
            return self.step < node2.step
        else:
            return self.ToString() < node2.ToString()
        
    def __hash__(self):
        return hash(self.ToString())
        
    def ReadCP(self, sys1: CPSystem):
        self.terms = sys1.SystemTerms()
        self.state = sys1.State()
        self.committed_state = sys1.State()
        
    def ReadContent(self, terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated):
        self.terms = terms
        self.products = products
        self.state = state
        self.committed_state = committed_state
        self.is_committed = is_committed
        self.next_rule_index = next_rule_index
        self.step = step
        self.ancestors = ancestors
        self.terminated = terminated
        
    def ToString(self):
        str_node = 'Step: ' + str(self.step) + '\n'
        str_node += 'State: ' + self.state + '\n'
        if self.is_committed:
            str_node += 'Commited to: ' + self.committed_state + '\n'
        str_node += 'Terms:\n'
        
        ordered_terms = OrderedDict(sorted(self.terms.items(), key = lambda t: t[0]))
        for item in ordered_terms:
            if isinstance(item, Term):
                str_node += item.ToString() + ": " + str(ordered_terms[item]) + '\n'
            else:
                str_node += item + ": " + str(ordered_terms[item]) + '\n'
                
        if len(self.products) > 0:
            str_node += 'Virtual products:\n'
            ordered_products = OrderedDict(sorted(self.products.items(), key = lambda t: t[0]))
            for item in ordered_products:
                if isinstance(item, Term):
                    str_node += item.ToString() + ": " + str(ordered_products[item]) + '\n'
                else:
                    str_node += item + ": " + str(ordered_products[item]) + '\n'
        str_node += 'Next rule: ' + str(self.next_rule_index) + '\n'
        return str_node
        #ancestors is not considered in __hash__
        
    def AncestorsToString(self):
        str_ans = ''
        for ancestor in self.ancestors:
            str_ans += ancestor + '\n'
        return str_ans
                
class CPVerifier:
    def __init__(self, sys1: CPSystem):
        node = CPNode()
        node.ReadCP(sys1)
        self.node_list = [node]
        self.detail_level = 0
        self.rules = sys1.Rules()
        self.expected_terminations = []
        self.search_method = 'Priority Search'
        self.state_limit = 10000
        self.states_checked = 0
        self.property = 'deadlock'
        self.counter_example_found = False
        self.counter_example = CPNode()
        self.target = {}
        self.target_state = ''
        self.termination_set = set() #only used for Church-Rosser property check
        self.step_limit = 100
        #self.target_until_1 = {} #some terms are in the system
        #self.target_until_2 = {} #until others are in the system
        #self.target_next_1 = {} #some terms are in the system
        #self.target_next_2 = {} #until others are in the system in the next step

#Property code
#0: If the cP system is deadlockfree
#1: If the cP system is deterministic
#2: If the cP system is confluent
#3: If certain goal terms are included in a halting configuration
#4: If certain goal terms are included in all halting configurations
#5: If a goal state is reachable in a halting configuration
#6: If a goal state is reachable in all halting configurations
#7: If certain terms are always in the cP system
#8: If certain terms are in the cP system at least in one configuration
#9: If the cP system is terminating
    def Property(self, code):
        if code == 0:
            return 'deadlockfree'
        elif code == 1:
            return 'deterministic'
        elif code == 2:
            return 'confluent'
        elif code == 3:
            return 'terms_in_one_halting'
        elif code == 4:
            return 'terms_in_all_halting'
        elif code == 5:
            return 'state_in_one_halting'
        elif code == 6:
            return 'state_in_all_halting'
        elif code == 7:
            return 'terms_in_all'
        elif code == 8:
            return 'terms_in_one'
        elif code == 9:
            return 'terminating'
        elif code == 10:
            return 'state_in_all'
        elif code == 11:
            return 'state_in_one'
        
        else:
            return 'deadlockfree'
        
    def SetTerminations(self, terminations: List[str]):
        self.expected_terminations = terminations
        
    def GetNextRuleIndex(self, current_rule_index: int):
        if current_rule_index < len(self.rules) - 1:
            return current_rule_index + 1
        else:
            return 0
        
    #cP systems are usually working in a priority search way! 
    #Don't choose BFS or DSF unless you know what are you verifying exactly! 
    #BFS and DFS may work for certain properties, while they may also drive the verifier to check practically unreachable states!
    def SetSearchMethod(self, sm: str):
        if sm == 'Priority Search' or 'DFS' or 'BFS':
            self.search_method = sm
            
    def SetDetailLevel(self, lvl):
        if lvl == 0 or lvl == 2 or lvl == 3:
            self.detail_level = lvl
        
    def SetTargetTerms(self, target: OrderedDict[Term, int]):
        self.target = target
        
    def SetTargetState(self, target: str):
        self.target_state = target

    def Verify(self, property_code = 0, state_limit = 10000, step_limit = 100):
        try:
            self.CheckProperties(property_code, state_limit, step_limit)
        except BaseException as err:
            print("Unexpected {err=}", type(err))
    
    def CheckProperties(self, property_code = 0, state_limit = 10000, step_limit = 100):
        self.state_limit = state_limit
        self.step_limit = step_limit
        self.property = self.Property(property_code)

        time_start = time.perf_counter()
        self.Next()
        time_end = time.perf_counter()
        print('The verification is finished in ' + str(round(time_end - time_start, 4)) + ' second(s), ' + str(self.states_checked) + 
              ' cP system nodes were checked.' )
        print('The search method is ' + self.search_method + '.')
        
        if self.counter_example_found and self.detail_level == 0:
            if self.property == 'terms_in_one_halting':
                print('The target terms are included by a halting configuration!\n' + self.counter_example.ToString())
            elif self.property == 'terms_in_all_halting':
                print('The target terms are NOT included by all halting configurations!\n' + self.counter_example.ToString())
            elif self.property == 'state_in_one_halting':
                print('The target state ' + self.target_state + ' is reached in a halting configuration!\n' + self.counter_example.ToString())
            elif self.property == 'state_in_all_halting':
                print('The target state ' + self.target_state + ' is NOT eventually reached!\n' + self.counter_example.ToString())
            elif self.property == 'deterministic':
                print('The cP system is nondeterministic!')
            elif self.property == 'deadlockfree':
                print('A deadlock state is found!\n' + self.counter_example.ToString())
            elif self.property == 'confluent':
                print('The cP system is NOT confluent! Different halting configurations can be found!')
                self.PrintTerminationSet()
            elif self.property == 'terms_in_all':
                print('The target terms are NOT included in all configurations!\n' + self.counter_example.ToString())
            elif self.property == 'terms_in_one':
                print('The target terms are included in a configuration!\n' + self.counter_example.ToString())
            elif self.property == 'terminating':
                print('Time out! The cP system is assumed to be nonterminating!\n')
            elif self.property == 'state_in_all':
                print('The target state is NOT held by all configurations!\n' + self.counter_example.ToString())
            elif self.property == 'state_in_one':
                print('The target state is reachable!\n' + self.counter_example.ToString())
                
        elif self.counter_example_found:
            if self.property == 'terms_in_one_halting':
                print('The target terms are included by a halting configuration!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'terms_in_all_halting':
                print('The target terms are NOT included by all halting configurations!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'state_in_one_halting':
                print('The target state ' + self.target_state + ' is reached in a halting configuration!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'state_in_all_halting':
                print('The target state ' + self.target_state + ' is NOT eventually reached!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'deterministic':
                print('The cP system is nondeterministic!')
            elif self.property == 'deadlockfree':
                print('A deadlock state is found!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'confluent':
                print('The cP system is NOT confluent! Different halting configuration can be found!')
                self.PrintTerminationSet()
                i = 1
                for item in self.termination_set:
                    print('Trace' + str(i) + ':\n' + item.AncestorsToString())
                    i += 1
            elif self.property == 'terms_in_all':
                print('The target terms are NOT included in all configurations!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'terms_in_one':
                print('The target terms are included in a configuration!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'terminating':
                print('Time out! The cP system is assumed to be nonterminating!\n')
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'state_in_all':
                print('The target state is NOT held by all configurations!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())
            elif self.property == 'state_in_one':
                print('The target state is reachable!\n' + self.counter_example.ToString())
                print('*******************************************\nTrace:\n' + self.counter_example.AncestorsToString())      
        else:
            if self.property == 'terms_in_one_halting':
                print('The target terms are NOT included by any halting configuration!')
            elif self.property == 'terms_in_all_halting':
                print('The target terms are included by all halting configurations!\n')
            elif self.property == 'state_in_one_halting':
                print('The target state ' + self.target_state + ' is NOT reached in any halting configuration!')
            elif self.property == 'state_in_all_halting':
                print('The target state ' + self.target_state + ' is eventually reached!\n')
            elif self.property == 'deterministic':
                print('The cP system is deterministic!')
            elif self.property == 'deadlockfree':
                print('The cP system is deadlock free!')
            elif self.property == 'confluent':
                print('The cP system is confluent!')
            elif self.property == 'terms_in_all':
                print('The target terms are included in all configurations!\n')
            elif self.property == 'terms_in_one':
                print('The target terms are NOT included in any configuration!\n')
            elif self.property == 'terminating':
                print('The cP system is terminating!\n')
            elif self.property == 'state_in_all':
                print('The target state is held by all configurations!\n')
            elif self.property == 'state_in_one':
                print('The target state is NOT reachable!\n')
            
        
    def Next(self, rules_skipped = 0):
        if self.counter_example_found:
            return True
        
        if self.states_checked >= self.state_limit: #verfication limit reached
            if self.property == 'terminating':
                self.counter_example_found = True
                return True
            else:
                print("The statespace limit is reached!")
                return False
        
        nodes_left = len(self.node_list)
        if nodes_left <= 0: #verification finished, all nodes checked
            return False
        
        conf1 = CPNode()
        if self.search_method == 'Priority Search':
            conf1 = self.node_list[0] #a shallow copy
        elif self.search_method == 'BFS':
            conf1 = self.node_list[0] #a shallow copy
        else: #DFS
            conf1 = self.node_list[-1] #a shallow copy
        self.states_checked += 1
        
        state = conf1.state
        terms = conf1.terms
        products = conf1.products
        committed_state = conf1.committed_state
        is_committed = conf1.is_committed
        current_rule_index = conf1.next_rule_index
        r1 = self.rules[current_rule_index]
        next_rule_index = self.GetNextRuleIndex(current_rule_index)
        ancestors = conf1.ancestors
        ancestors.append(conf1.ToString())
        step = conf1.step
        terminated = conf1.terminated
        
        # If I do this somewhere else to allow some inline modifications to the objects, it may be error-prune, however, it can improve the performance.
        if self.search_method == 'Priority Search':
            heapq.heappop(self.node_list)
        elif self.search_method == 'BFS':
            self.node_list.pop(0)
        else: #DFS
            self.node_list.pop()
            
        if step > self.step_limit:
            self.Next()
            return False
        
        #checking properties here for normal configurations
        if self.property == 'terms_in_all':
            if not lnmu.MultisetInclusion(terms, self.target):
                self.counter_example = conf1
                self.counter_example_found = True
                return True
        elif self.property == 'terms_in_one':
            if lnmu.MultisetInclusion(terms, self.target):
                self.counter_example = conf1
                self.counter_example_found = True
                return True
        elif self.property == 'state_in_all':
            if state != self.target_state:
                self.counter_example = conf1
                self.counter_example_found = True
                return True
        elif self.property == 'state_in_one':
            if state == self.target_state:
                self.counter_example = conf1
                self.counter_example_found = True
                return True  
            
        #checking properties here for halting configurations
        if state in self.expected_terminations or terminated:
            self.termination_set.add(conf1)
            if self.property == 'terms_in_one_halting':
                if lnmu.MultisetInclusion(terms, self.target):
                    self.counter_example = conf1
                    self.counter_example_found = True
                    return True
            elif self.property == 'terms_in_all_halting':
                if not lnmu.MultisetInclusion(terms, self.target):
                    self.counter_example = conf1
                    self.counter_example_found = True
                    return True
            elif self.property == 'state_in_one_halting':
                if state == self.target_state:
                    self.counter_example = conf1
                    self.counter_example_found = True
                    return True
            elif self.property == 'state_in_all_halting':
                if state != self.target_state:
                    self.counter_example = conf1
                    self.counter_example_found = True
                    return True
            elif self.property == 'confluent': #: confluence check
                if len(self.termination_set) > 1:
                    self.counter_example_found = True
                    return True
            elif (self.property == 'deadlockfree') and (not state in self.expected_terminations):
                self.counter_example = conf1
                self.counter_example_found = True
                return True 
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
                if rules_skipped >= len(self.rules) - 1:
                    terminated = True
                
            old_node = CPNode()
            old_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated)
            self.PushOldCPNode(old_node)
            self.states_checked += 1
            if next_rule_index == 0:
                self.Next()
            else:
                self.Next(rules_skipped + 1)
        
        #2
        elif len(r1.LHS()) == 0 and len(r1.PMT()) == 0: #no lhs and promoter, success, no diff between 1 and +
            self.VProduceMultiset(products, r1.RHS())
            if not is_committed:
                is_committed = True
                committed_state = r1.RState()
                step += 1 #a rule commitment = a step
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
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated)
            self.PushNewCPNode(new_node)
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
                        step += 1
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
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated)
                    self.PushNewCPNode(new_node)  
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
                        if rules_skipped >= len(self.rules) - 1:
                            terminated = True
                    old_node = CPNode()
                    old_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated)
                    self.PushOldCPNode(old_node)
                    if next_rule_index == 0:
                        self.Next()
                    else:
                        self.Next(rules_skipped + 1)
                    
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
                        if rules_skipped >= len(self.rules) - 1:
                            terminated = True
                    old_node = CPNode()
                    old_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated)
                    self.PushOldCPNode(old_node)
                    if next_rule_index == 0:
                        self.Next()
                    else:
                        self.Next(rules_skipped + 1)
                else:
                    mult -= 1
                    self.VConsumeMultiset(terms, lnmu.MultisetTimes(r1.LHS(), mult))
                    self.VProduceMultiset(products, lnmu.MultisetTimes(r1.RHS(), mult))
                    if not is_committed:
                        is_committed = True
                        committed_state = r1.RState()
                        step += 1
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
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated)
                    self.PushNewCPNode(new_node)
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
                if self.property == 'deterministic':
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
                    if rules_skipped >= len(self.rules) - 1:
                        terminated = True
                old_node = CPNode()
                old_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step, ancestors, terminated)
                self.PushOldCPNode(old_node)
                if next_rule_index == 0:
                    self.Next()
                else:
                    self.Next(rules_skipped + 1)
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
                            is_committed2 = is_committed
                            committed_state2 = committed_state
                            state2 = state
                            step2 = step
                            if lnmu.MultisetIn(ms_to_check, terms2): #rule applicable
                                self.VConsumeMultiset(terms2, r2.LHS())
                                self.VProduceMultiset(products2, r2.RHS())
                                if not is_committed2:
                                    is_committed2 = True
                                    committed_state2 = r2.RState()
                                    step2 += 1
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
                                new_node.ReadContent(terms2, products2, state2, committed_state2, is_committed2, next_rule_index, step2, ancestors, terminated)
                                self.PushNewCPNode(new_node)
                        
                elif r1.Model() == '+': #max-parallel model
                    gruleset = []
                    for unifier in SS:
                        lhs2 = lnmu.ApplyBindingMultiset(r1.LHS(), unifier)
                        rhs2 = lnmu.ApplyBindingMultiset(r1.RHS(), unifier)
                        pmt2 = lnmu.ApplyBindingMultiset(r1.PMT(), unifier)
                        r2 = Rule(r1.LState(), r1.RState(), '+') #a unified, ground rule
                        r2.SetLHS(lhs2)
                        r2.SetRHS(rhs2)
                        r2.SetPMT(pmt2)
                        if r2.IsGround():
                            gruleset.append(r2)
                    total = pow(2, len(SS)) - 1
                    self.states_checked += total
                    applied_unifiers = []
                    for x in range(total,-1,-1): #using binary to enumerate c(n,1), c(n,2)... c(n,n) max-compatible unifiers
                        needed = True
                        for x1 in applied_unifiers:
                            if self.IsSubset(x, x1):
                                needed = False
                                break
                        if not needed:
                            continue  
                        
                        terms2 = deepcopy(terms)
                        products2 = deepcopy(products)
                        is_committed2 = is_committed
                        committed_state2 = committed_state
                        state2 = state
                        step2 = step
                               
                        y = x
                        unifier_ids = []       
                        position = len(SS) - 1
                        while position >= 0:
                            if y % 2 == 1:
                                unifier_ids.append(position)
                            position -= 1
                            y = int(y / 2)
                            
                        all_applied = True
                        for i in unifier_ids:
                            ms_to_check = lnmu.MultisetUnion(gruleset[i].PMT(), gruleset[i].LHS())
                            if lnmu.MultisetIn(ms_to_check, terms2): #rule applicable
                                self.VConsumeMultiset(terms2, gruleset[i].LHS())
                                self.VProduceMultiset(products2, gruleset[i].RHS())
                            else:
                                all_applied = False
                                break
                                       
                        if all_applied: 
                            applied_unifiers.append(x)
                            if not is_committed2:
                                is_committed2 = True
                                committed_state2 = r1.RState()
                                step2 += 1
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
                            new_node.ReadContent(terms2, products2, state2, committed_state2, is_committed2, next_rule_index, step2, ancestors, terminated)
                            self.PushNewCPNode(new_node)
                          
                else: #currently cP systems only support 2 application models, '1' and '+'
                    print('Incorrect application model!')
                    return False
                
                self.Next() 
                
        return True
    
    def IsSubset(self, child, parent):
        if parent < child:
            return False
        elif parent == child:
            return True
        if parent % 2 == 0 and child % 2 == 1:
            return False
        else:
            return self.IsSubset(int(child / 2), int(parent / 2))
            
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
            
    def PushNewCPNode(self, node1):
        if self.search_method == 'Priority Search':
            heapq.heappush(self.node_list, node1)
        else:
            self.node_list.append(node1)
            
    def PushOldCPNode(self, node1):
        if self.search_method == 'Priority Search':
            heapq.heappush(self.node_list, node1)
        elif self.search_method == 'BFS':
            self.node_list.insert(0, node1)
        else:
            self.node_list.append(node1)
            
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