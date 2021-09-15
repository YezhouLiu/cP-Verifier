#cP Systems - Yezhou Liu
#simple term

from collections import OrderedDict

class CPSimpleTerm:
    def __init__(self, name, value = 0, vars = ''): #default cons makes an a(lambda)
        self.name = name #name: a
        self.vars = OrderedDict()#a dict: X:2, Y:1, Z:1 -- a(XXYZ)
        self.value = value
        self.type = 'SIMP'
        self.AddVars(vars)

    def __eq__(self, term2): 
        if not isinstance(term2, CPSimpleTerm): #only compare terms
            return False
        return self.ToString() == term2.ToString()
    
    def __lt__(self, term2): #less than
        return self.ToString() < term2.ToString()
                    
    def __hash__(self): #implement eq and hash function, which the system can use CPTerm as a dictionary key
        return hash(self.ToString())

    def AddValue(self, value):
        if value >= 0:
            self.value += value
            return True
        else:
            print('Error e1!')
            return False

    def SetValue(self, value):
        self.value = value #maybe do a type check to make sure value is typeInt?
        return True

    def AddVar(self, var):
        if var in self.vars:
            self.vars[var] += 1
        else:
            self.vars[var] = 1
        self.vars = OrderedDict(sorted(self.vars.items()))
        return True

    def AddVars(self, vars):
        if len(vars) > 0:
            for i in range(0, len(vars)):
                self.AddVar(vars[i])
        return True

    def RemoveValue(self, value):
        if value > 0 and self.value >= value:
            self.value -= value
            return True
        else:
            print('Error e2!')
            return False

    def ConsumeVar(self, var, count = 1):
        if not var in self.vars:
            print('Error e3!')
            return False
        if self.vars[var] > count:
            self.vars[var] -= count
        elif self.vars[var] == count:
            self.vars.pop(var)
        else:
            print('Error e4!')
        return True

    def ConsumeValue(self, value):
        if self.value >= value:
            self.value -= value
            return True
        else:
            print('Error e5!')
            return False

    def IsGround(self): #True - grounded, False - has variables
        return len(self.vars) == 0

    def ToString(self):
        temp_str = self.name + '('
        if len(self.vars) > 0:
            for var in self.vars:
                for _ in range(0, self.vars[var]):
                    temp_str += var
        if self.value > 0:
            temp_str += str(self.value)
        temp_str += ')'
        return temp_str

