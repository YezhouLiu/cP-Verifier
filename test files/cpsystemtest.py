import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from term import Term
from rule import Rule
from cpsystem import CPSystem
from cpparser import ParseTerms
from cpparser import ParseRule
import sys
from cpverifier import CPVerifier
 
r1 = ParseRule('s1 f(a(b)) f(X) b ->1 s1 c g(X) d')
sys1 = CPSystem('s1')
sys1.AddRule(r1)
sys1.AddSystemMultiset(ParseTerms('f(a(b)) f(a(b)) f(1) b d'))
sys1.DetailOn()
sys1.Snapshot()
sys1.Run()

r2 = ParseRule('s1 f(1) g(1) ->+ s1 ')
#r3 = ParseRule('s1 ->1 s2 ')
sys2 = CPSystem('s1')
sys2.AddRule(r2)
#sys2.AddRule(r3)
sys2.AddSystemMultiset(ParseTerms('f(1) f(1) f(1) f(1) g(1) g(1) g(1)'))
#sys2.DetailOn()
#sys2.Snapshot()
#sys2.Run()

cpv = CPVerifier(sys2)
cpv.Next()