#cP terms

from collections import OrderedDict
from copy import deepcopy
#Multiset = OrderedDict

class Term: #compound term
    def __init__(self, label: str):
        self.label = label #label of a cell/subcell/term
        self.atoms = OrderedDict()
        self.variables = OrderedDict()
        self.subterms = OrderedDict() #subcompoundterms

    #HASH
    #------------------------------------------------------------------------------
    def __eq__(self, term2): 
        if not isinstance(term2, Term): # compare terms only
            return False
        return self.ToString() == term2.ToString()
    def __lt__(self, term2): #less than
        if not isinstance(term2, Term): # compare terms only
            return False
        return self.ToString() < term2.ToString()
    def __hash__(self): #implement eq and hash function, which the system can use Term as a dictionary key
        return hash(self.ToString())

    #SORT CONTENT
    #------------------------------------------------------------------------------
    def SortContent(self):
        self.atoms = OrderedDict(sorted(self.atoms.items()))
        self.variables = OrderedDict(sorted(self.variables.items()))
        self.subterms = OrderedDict(sorted(self.subterms.items()))

    #LABEL
    #------------------------------------------------------------------------------
    def Label(self):
        return self.label
    #currently, no "higher-order" rule (not really higher-order, let's call it this way) in cP~systems, therefore, no need to provide a setter for label

    #NUMBER
    #------------------------------------------------------------------------------
    def AddNumber(self, val: int): #numbers can be treated as atoms
        if '1' in self.atoms and val > 0:
            self.atoms['1'] += val
        elif val > 0:
            self.atoms['1'] = val
            self.SortContent()

    def SubtractNumber(self, val: int):
        if val > 0 and val <= self.atoms['1']:
            self.atoms['1'] -= val
            if self.atoms['1'] == 0:
                self.atoms.pop('1')

    def Number(self):
        if '1' in self.atoms:
            return self.atoms['1']
        return 0

    #ATOM
    #------------------------------------------------------------------------------
    def AddAtom(self, atom: str, count = 1): #atom: 'a'
        if atom in self.atoms:
            self.atoms[atom] += count
        else:
            self.atoms[atom] = count
        self.SortContent()
    
    def AddAtoms(self, atoms: str): #atoms: 'aab', 'vvwww'...
        if len(atoms) > 0:
            for i in range(0, len(atoms)):
                if atoms[i] in self.atoms:
                    self.atoms[atoms[i]] += 1
                else:
                    self.atoms[atoms[i]] = 1
        self.SortContent()

    def Atoms(self):
        return self.atoms

    def SetAtoms(self, ats: OrderedDict):
        self.atoms = ats

    #consume atoms - MultisetMinus

    #VARIABLE
    #------------------------------------------------------------------------------
    def AddVariable(self, var: str, count = 1): #var: 'X'
        if var in self.variables:
            self.variables[var] += count
        else:
            self.variables[var] = count
        self.SortContent()

    def AddVariables(self, vars: str): #vars: 'XXY', 'YYZ'
        if len(vars) > 0:
            for i in range(0, len(vars)):
                if vars[i] in self.variables:
                    self.variables[vars[i]] += 1
                else:
                    self.variables[vars[i]] = 1
        self.SortContent()

    def Variables(self):
        return self.variables

    #consume vars is different, its unifier application.

    #SUBTERM
    #------------------------------------------------------------------------------
    def AddSubterm(self, term, count = 1): #add a subterm / subterms
        if not isinstance(term, Term):
            return
        if term in self.subterms: #dictionary: key:Term value:nat
            self.subterms[term] += count
        else:
            self.subterms[term] = count
        self.SortContent()
    
    def Subterms(self):
        return self.subterms

    #ALL CONTENT
    #------------------------------------------------------------------------------
    def CellContent(self): #it returns a multiset contains everything in a cell
        ms = deepcopy(self.atoms)
        for key in self.variables:
            ms[key] = self.variables[key]
        for key in self.subterms:
            ms[key] = self.subterms[key]
        return ms

    #OTHERS
    #------------------------------------------------------------------------------
    def ToString(self):
        temp_str = self.label + '('
        for var1 in self.variables: #variables
            for _ in range(self.variables[var1]): #multiplicity
                temp_str += var1
        for atom1 in self.atoms: #atoms
            for _ in range(self.atoms[atom1]):
                temp_str += atom1
        for term1 in self.subterms: #subterms
            for _ in range(self.subterms[term1]): 
                temp_str += term1.ToString()
        temp_str += ')'
        return temp_str

    def IsGround(self):
        term_str = self.ToString()
        for i in range(len(term_str)):
            if term_str[i] >= 'A' and term_str[i] <= 'Z':
                return False
        return True

    def Print(self):
        print (self.ToString())

