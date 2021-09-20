import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from term import Term
from rule import Rule
from cpsystem import CPSystem
from cpparser import ParseTerms
from cpparser import ParseRule
import sys
 
r1 = ParseRule('s1 f(a(b)) f(X) b ->1 s1 c g(X) d')
sys1 = CPSystem('s1')
sys1.AddRule(r1)
sys1.AddSystemMultiset(ParseTerms('f(a(b)) f(a(b)) f(1) b d'))
sys1.DetailOn()
sys1.Snapshot()
sys1.Run()