#cP rules

from term import Term

class Rule:
    def __init__(self, left_state, right_state, model): #a rule's lstate, rstate and application model must be given
        self.l_state = left_state
        self.r_state = right_state
        self.lhs = {} #lhs terms
        self.rhs = {} #rhs terms
        self.pmt = {} #promoter terms
        self.model = model # '1' exact-once, '+' max-parallel
        
#HASH
    #------------------------------------------------------------------------------
    def __eq__(self, rule2): 
        if not isinstance(rule2, Rule): # compare rules only
            return False
        return self.ToString() == rule2.ToString()
    def __lt__(self, rule2): #less than
        if not isinstance(rule2, Rule):
            return False
        return self.ToString() < rule2.ToString()
    def __hash__(self):
        return hash(self.ToString())

#GETTERS
#------------------------------------------------------------------------------
    def LState(self):
        return self.l_state

    def RState(self):
        return self.r_state

    def LHS(self):
        return self.lhs

    def RHS(self):
        return self.rhs

    def PMT(self):
        return self.pmt

    def Model(self):
        return self.model

#SETTERS
#------------------------------------------------------------------------------
    def SetLState(self, ls):
        self.l_state = ls

    def SetRState(self, rs):
        self.r_state = rs

    def SetLHS(self, lhs):
        self.lhs = lhs

    def SetRHS(self, rhs):
        self.rhs = rhs

    def SetPMT(self, pmt):
        self.pmt = pmt

    def SetModel(self, model):
        self.model = model

#OPERATION
#------------------------------------------------------------------------------
    def AddL(self, t1, count = 1): #add an L term
        if t1 in self.lhs:
            self.lhs[t1] += count
        else:
            self.lhs[t1] = count

    def AddR(self, t1, count = 1): #add a R term
        if t1 in self.rhs:
            self.rhs[t1] += count
        else:
            self.rhs[t1] = count

    def AddPMT(self, t1, count = 1): #add a promoter
        if t1 in self.pmt:
            self.pmt[t1] += count
        else:
            self.pmt[t1] = count

#CHECKING
#------------------------------------------------------------------------------
    def IsGround(self): #rule consists of grounded terms only
        term_str = self.ToString()
        for i in range(len(term_str)):
            if term_str[i] >= 'A' and term_str[i] <= 'Z':
                return False
        return True

    def IsValid(self): #variables that appear in a rule's rhs, must appear in its lhs or promoters
        variables = set()
        lp_str = ''
        for t1 in self.lhs:
            if isinstance(t1, Term):
                lp_str += t1.ToString()
            else:
                lp_str += t1
        for t2 in self.pmt:
            if isinstance(t2, Term):
                lp_str += t2.ToString()
            else:
                lp_str += t2
        for i in range(len(lp_str)):
            if lp_str[i] >= 'A' and lp_str[i] <= 'Z':
                variables.add(lp_str[i])
        r_str = ''
        for t3 in self.rhs:
            if isinstance(t3, Term):
                lp_str += t3.ToString()
            else:
                lp_str += t3
        for i in range(len(r_str)):
            if r_str[i] >= 'A' and r_str[i] <= 'Z':
                if not r_str[i] in variables:
                    return False
        return True

#DISPLAY
#------------------------------------------------------------------------------
    def ToString(self):
        temp_str = self.l_state + ' '
        for x in self.lhs:
            x_mult = self.lhs[x]
            if isinstance(x, Term):
                temp_str += (x.ToString() + ' ') * x_mult
            elif x == '1':
                temp_str += str(x_mult) + ' '
            else:
                temp_str += (x + ' ') * x_mult
        temp_str += '->' + self.model + ' '
        temp_str += self.r_state + ' '
        for y in self.rhs:
            y_mult = self.rhs[y]
            if isinstance(y, Term):
                  temp_str += (y.ToString() + ' ') * y_mult
            elif y == '1':
                temp_str += str(y_mult) + ' '
            else:
                temp_str += (y + ' ') * y_mult
        if len(self.pmt) > 0:
            temp_str += '| '
            for z in self.pmt:
                z_mult = self.pmt[z]
                if isinstance(z, Term):
                  temp_str += (z.ToString() + ' ') * z_mult
                elif z == '1':
                    temp_str += str(z_mult) + ' '
                else:
                    temp_str += (z + ' ') * z_mult
        return temp_str

    def Print(self):
        print(self.ToString())