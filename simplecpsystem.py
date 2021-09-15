#cP Systems - Yezhou Liu
#simple cP systems

from copy import deepcopy
from simpleterm import CPSimpleTerm
from toolbox import UnifySimple
from toolbox import ReplaceSimple
from toolbox import ReplaceSimpleDict
import random as rd

class CPSystemSimple:
    def __init__(self, state = ''):
        self.rules = [] #use list/array: rules' have weak priority order
        self.terms = {} #a map... a(1)a(1)a(1)a(2)a(3) -- a(1):3, a(2):1, a(3):1
        self.state = state
        self.products = {} #product membrane
        self.next_state = ''
        self.step = 0

    def StepOver(self): #move to the next step, activate terms in product membrane
        self.state = self.next_state
        for x in self.products:
            if x in self.terms:
                self.terms[x] += self.products[x]
            else:
                self.terms[x] = self.products[x]
        self.products = {}
        self.step += 1

    def SetState(self, state):
        self.state = state
        return True

    def AddTerm(self, term):
        if term in self.terms:
            self.terms[term] += 1
        else: 
            self.terms[term] = 1
        return True

    def AddProduct(self, term):
        if term in self.products:
            self.products[term] += 1
        else: 
            self.products[term] = 1
        return True

    def AddProducts(self, term_dict):
        for term in term_dict:
            if term not in self.terms:
                self.terms[term] = term_dict[term]
            else:
                self.terms[term] += term_dict[term]
        return True

    def ConsumeTerm(self, term):
        if term not in self.terms:
            return False
        elif self.terms[term] > 1: 
            self.terms[term] -= 1
        else:
            self.terms.pop(term)
        print('1 copy of term ', term.ToString(), 'is consumed! ')
        return  True

    def ConsumeTerms(self, term_dict):
        #pre-check
        for term in term_dict:
            if term not in self.terms:
                return False
            elif term_dict[term] > self.terms[term]:
                return False
        #consume
        for term in term_dict:
            diff = self.terms[term] - term_dict[term]
            if diff > 0: 
                self.terms[term] = diff
            else:
                self.terms.pop(term)
            print(term_dict[term], 'copy(copies) of term', term.ToString(), 'is(are) consumed! ')
        return  True    
 
    def AddRule(self, rule):
        if rule.IsValid():
            self.rules.append(rule)
            return True
        else:
            print('Error! Invalid rule!')
            return False

    def RunUntilSystemHalt(self, steps_upper_bound = 0):
        rules_can_apply = True
        breaker = 0
        check_breaker = False
        if steps_upper_bound > 0:
            breaker = steps_upper_bound
            check_breaker = True
        while (True):
            rules_can_apply = False
            for i in range(0, len(self.rules)):
                success = self.ApplyOneRule(self.rules[i])
                if success:
                    rules_can_apply = True
                    print('Successfully applied rule: ', self.rules[i].ToString())
                    ls = self.rules[i].state_l
                    rs = self.rules[i].state_r
                    for j in range(i+1, len(self.rules)): #applying all rules commiting to the same cP~state
                        if self.rules[j].state_l == ls and  self.rules[j].state_r == rs:
                            self.ApplyOneRule(self.rules[j])
                    break
            if not rules_can_apply:
                break
            #step over
            self.StepOver()
            self.SystemSnapshot()
            if check_breaker:
                breaker -= 1
                if breaker == 0:
                    break
        print('System halts!')

    def RunStep(self):
        for i in range(0, len(self.rules)):
            success = self.ApplyOneRule(self.rules[i])
            if success:
                print('Successfully applied rule: ', self.rules[i].ToString())
                ls = self.rules[i].state_l
                rs = self.rules[i].state_r
                for j in range(i+1, len(self.rules)): #applying all rules commiting to the same cP~state
                    if self.rules[j].state_l == ls and  self.rules[j].state_r == rs:
                        self.ApplyOneRule(self.rules[j])
                break
            #step over
        self.StepOver()
        self.SystemSnapshot()

    def PromotersExist(self, pmt):
        if len(pmt) == 0:
            return True
        for x in pmt:
            if x not in self.terms:
                return False
            elif self.terms[x] < pmt[x]:
                return False
        return True

    def ApplyOneRule(self, rule): #a version without considering promoters
        print('Trying to apply the rule: ', rule.ToString())
        if rule.state_l != self.state: #state check failed
            print('cP state unmatched, the rule cannot be applied!')
            return False
        elif len(rule.lhs) == 0 and len(rule.pmt) == 0: #no lhs and promoter, success, directly generate products
            self.AddProducts(rule.rhs)
            return True
        elif rule.IsGround(): #no need to unify
            if self.PromotersExist(rule.pmt) and self.ConsumeTerms(rule.lhs):
                self.AddProduct(rule.rhs)
                return True
            else:
                print('Insufficient terms in the system, the rule cannot be applied.')
                return False
        else:
            variables_unifications = []
            one_dict = {}
            taken = {} #to track how many system terms the rule needs to consume
            self.UnifyRule(rule.lhs, rule.pmt, self.terms, taken, one_dict, variables_unifications)
            if len(variables_unifications) == 0: #the rule does not match system terms, cannot be applied
                print('Insufficient terms in the system, the rule cannot be applied.')
                return False
            #else
            print('Valid bindings: ', variables_unifications)
            self.next_state = rule.state_r
            uni_size = len(variables_unifications)
            rd_uni = rd.randint(0, uni_size-1)
            if rule.model == '1': #exact-once model
                selected_uni = variables_unifications[rd_uni]
                temp_lhs_copy = deepcopy(rule.lhs)
                temp_rhs_copy = deepcopy(rule.rhs)
                lhs_copy = ReplaceSimpleDict(temp_lhs_copy, selected_uni)
                rhs_copy = ReplaceSimpleDict(temp_rhs_copy, selected_uni)
                temp_pmt_copy = deepcopy(rule.pmt)
                pmt_copy = ReplaceSimpleDict(temp_pmt_copy, selected_uni)
                if self.PromotersExist(pmt_copy) and self.ConsumeTerms(lhs_copy):
                    self.AddProducts(rhs_copy)
            elif rule.model == '+': #max-parallel model
                for uni in variables_unifications:
                    temp_lhs_copy = deepcopy(rule.lhs)
                    temp_rhs_copy = deepcopy(rule.rhs)
                    lhs_copy = ReplaceSimpleDict(temp_lhs_copy, uni)
                    rhs_copy = ReplaceSimpleDict(temp_rhs_copy, uni)
                    temp_pmt_copy = deepcopy(rule.pmt)
                    pmt_copy = ReplaceSimpleDict(temp_pmt_copy, uni)
                    if self.PromotersExist(pmt_copy) and self.ConsumeTerms(lhs_copy):
                        self.AddProducts(rhs_copy)
            return True

    def UnifyRule(self, lhs, pmt, sys_terms, _taken, _one_unification, all_unifications): 
        #rule: a(X)a(Y) ->1 a(XY), system terms:{a(1):1, a(2):1} all_unifications: [{X:1, Y:2}, {X:2, Y:1}]
        if len(lhs) == 0 and len(pmt) == 0:
            return False 
        taken = deepcopy(_taken)
        if len(lhs) > 0:
            pattern = list(lhs)[0] #handle lhs
        else:
            pattern = list(pmt)[0] #handle pmt
        if pattern.IsGround():
            if pattern in taken:
                taken[pattern] += 1
            else:
                taken[pattern] = 1
            if not pattern in sys_terms or taken[pattern] > sys_terms[pattern]: #the rule needs to consume or promoted by a(1) x 3, the system only has a(1) x 2, the rule does not work
                return False
            else: #exit of the recursive function 1
                one_unification = deepcopy(_one_unification)
                all_unifications.append(one_unification)
                return True
        else:
            for term in sys_terms:
                for _ in range(sys_terms[term]):
                    taken = deepcopy(_taken) #clear taken here
                    if term in taken and sys_terms[term] - taken[term] < 1: #system has two a(1), they are all taken, thus we cannot unify it to another pattern
                        continue
                    uni = UnifySimple(pattern, term)
                    if len(uni) == 0: #failed to unify pattern with term
                        continue #go to check if the pattern can match next term
                    else: #success, take this term
                        if term in taken:
                            taken[term] += 1
                        else:
                            taken[term] = 1
                        for uni1 in uni: #for every possible unification
                            one_unification = deepcopy(_one_unification)
                            for x in uni1: #save the unification in one_unification
                                one_unification[x] = uni1[x]
                            if len(lhs) + len(pmt) == 1:#the only pattern is already matched, one_unification now contains a set of unification for all variables
                                all_unifications.append(one_unification) #exit of the recursive function 2
                            elif(len(lhs) > 0): #lhs > 0, move to unify next lhs pattern or promoter pattern
                                temp_lhs = deepcopy(lhs)
                                temp_pmt = deepcopy(pmt)
                                temp_lhs.pop(pattern)
                                new_lhs = ReplaceSimpleDict(temp_lhs, uni1)#apply the current unification {X:1, Y:2} to other patterns, then continue to deal with remain patterns
                                new_pmt = ReplaceSimpleDict(temp_pmt, uni1)
                                self.UnifyRule(new_lhs, new_pmt, sys_terms, taken, one_unification, all_unifications)
                            elif(len(pmt) > 1): #pmt > 1, move to unify next promoter pattern
                                temp_pmt = deepcopy(pmt)
                                temp_pmt.pop(pattern)
                                new_pmt = ReplaceSimpleDict(temp_pmt, uni1)
                                self.UnifyRule(lhs, new_pmt, sys_terms, taken, one_unification, all_unifications)
            return False #no system term can match this pattern

    def SystemSnapshot(self):
        print('\n\n\n------------------------------------------------------------------------------------------')
        print('System state: ', self.state)
        print('Terms in the system:')
        for x in self.terms:
            print(x.ToString(), self.terms[x])
        print('------------------------------------------------------------------------------------------\n\n\n')
