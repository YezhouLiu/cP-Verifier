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
import heapq
import time

VERSION = 1.0

class CPNode:
    def __init__(self):
        self.terms = {}
        self.products = {}
        self.state = ''
        self.committed_state = ''
        self.is_committed = False
        self.next_rule_index = 0
        self.step = 0
    
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
        
    def ReadContent(self, terms, products, state, committed_state, is_committed, next_rule_index, step):
        self.terms = terms
        self.products = products
        self.state = state
        self.committed_state = committed_state
        self.is_committed = is_committed
        self.next_rule_index = next_rule_index
        self.step = step
        
    def ToString(self):
        str_node = 'Step: ' + str(self.step) + '\n'
        str_node += 'State: ' + self.state + '\n'
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
        self.search_method = 'Priority Search'
        self.state_limit = 100000
        self.state_checked = 0
        self.property = 'deadlock'
        self.counter_example_found = False
        self.counter_example = CPNode()
        self.target = {}
        self.target_state = ''
        self.termination_set = set()
        self.shortest_termination_step = -1
        self.terminating_time_out = 1000000

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
        self.terminations = terminations
        
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
            
    def DetailOn(self):
        self.show_detail = True
        
    def DetailOff(self):
        self.show_detail = False
        
    def SetTargetTerms(self, target: OrderedDict[Term, int]):
        self.target = target
        
    def SetTargetState(self, target: str):
        self.target_state = target
        
    def SetTimeOut(self, maxsteps: int):
        self.terminating_time_out = maxsteps

    def Verify(self, property_code = 0, state_limit = 100000):
        try:
            self.CheckProperties(property_code, state_limit)
        except:
            print('The cP system verification is NOT finished as expected, which is often caused by non-terminating cP rules, please check the rules!')

    def CheckProperties(self, property_code = 0, state_limit = 100000):
        if self.property == 'terminating':
            self.state_limit = self.terminating_time_out
        else:
            self.state_limit = state_limit
        self.property = self.Property(property_code)

        time_start = time.perf_counter()
        self.Next()
        time_end = time.perf_counter()
        print('The cP system verification is finished in ' + str(time_end - time_start) + ' second(s), ' + str(self.state_checked) + ' states were checked.')
        print('The search method is ' + self.search_method + '.')
        
        if self.counter_example_found:
            if self.property == 'terms_in_one_halting':
                print('The target terms are included by a halting configuration!\n' + self.counter_example.ToString())
            elif self.property == 'terms_in_all_halting':
                print('The target terms are NOT included by all halting configurations!\n' + self.counter_example.ToString())
            elif self.property == 'state_in_one_halting':
                print('The target state ' + self.target_state + ' is reached in a halting configuration!\n' + self.counter_example.ToString())
            elif self.property == 'state_in_all_halting':
                print('The target state ' + self.target_state + ' is NOT reached in all halting configurations!\n' + self.counter_example.ToString())
            elif self.property == 'deterministic':
                print('The cP system is nondeterministic!')
            elif self.property == 'deadlockfree':
                print('A deadlock state is found!\n' + self.counter_example.ToString())
            elif self.property == 'confluent':
                print('The cP system is NOT confluent! Different halting configuration can be found!')
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
            
            
        else:
            if self.property == 'terms_in_one_halting':
                print('The target terms are NOT included by any halting configuration!')
            elif self.property == 'terms_in_all_halting':
                print('The target terms are included by all halting configurations!\n')
            elif self.property == 'state_in_one_halting':
                print('The target state ' + self.target_state + ' is NOT reached in any halting configuration!')
            elif self.property == 'state_in_all_halting':
                print('The target state ' + self.target_state + ' is reached in all halting configurations!\n')
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
        
        if self.state_checked >= self.state_limit: #verfication limit reached
            if self.property == 'terminating':
                self.counter_example_found = True
                return True
            else:
                print("Verification limit reached!")
                return False
        
        nodes_left = len(self.node_list)
        if nodes_left <= 0: #verification finished, all nodes checked
            return False
        
        conf1 = CPNode()
        if self.search_method == 'Priority Search':
            conf1 = self.node_list[0]
        elif self.search_method == 'BFS':
            conf1 = self.node_list[0]
        else: #DFS
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
        step = conf1.step
        
        if self.shortest_termination_step != -1 and step > self.shortest_termination_step: #system already terminated
            if self.search_method == 'Priority Search':
                self.node_list.pop(0)
            elif self.search_method == 'BFS':
                self.node_list.pop(0)
            else:
                self.node_list.pop()
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
        if state in self.terminations:
            if self.shortest_termination_step == -1:
                self.shortest_termination_step = step
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
                
        if (not state in self.terminations) and (rules_skipped >= len(self.rules)-1) and (self.property == 'deadlockfree'):  #no outgoing edge, not a expected termination, deadlock
            self.counter_example = conf1
            self.counter_example_found = True
            return True           
        
        if self.search_method == 'Priority Search':
            self.node_list.pop(0)
        elif self.search_method == 'BFS':
            self.node_list.pop(0)
        else: #DFS
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
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step)
            self.PushCPNode(new_node)
            self.Next(new_rules_skipped+1)
        
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
            new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step)
            self.PushCPNode(new_node)
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
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step)
                    self.PushCPNode(new_node)
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
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step)
                    self.PushCPNode(new_node)
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
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step)
                    self.PushCPNode(new_node)
                    self.Next(new_rules_skipped+1)
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
                    new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step)
                    self.PushCPNode(new_node)
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
                    new_rules_skipped = -1 
                new_node = CPNode()
                new_node.ReadContent(terms, products, state, committed_state, is_committed, next_rule_index, step)
                self.PushCPNode(new_node)
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
                            step2 = step
                            if lnmu.MultisetIn(ms_to_check, terms2): #rule applicable
                                self.VConsumeMultiset(terms2, r2.LHS())
                                self.VProduceMultiset(products2, r2.RHS())
                                rule_applied = True      
                            if rule_applied:
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
                                new_node.ReadContent(terms2, products2, state2, committed_state2, is_committed2, next_rule_index, step2)
                                self.PushCPNode(new_node)
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
                            step2 = step
                            ms_to_check = lnmu.MultisetUnion(r3.PMT(), r3.LHS())
                            if lnmu.MultisetIn(ms_to_check, terms2): #rule applicable
                                self.VConsumeMultiset(terms2, r3.LHS())
                                self.VProduceMultiset(products2, r3.RHS())
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
                            new_node.ReadContent(terms2, products2, state2, committed_state2, is_committed2, next_rule_index, step2)
                            self.PushCPNode(new_node)
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
            
    def PushCPNode(self, node1):
        if self.search_method == 'Priority Search':
            heapq.heappush(self.node_list, node1)
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