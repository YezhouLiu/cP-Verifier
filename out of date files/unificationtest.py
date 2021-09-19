from cpparser import ParseTerm
from toolbox import UnifyCompound
from toolbox import PrintUnifyCompound
import sys
import time

#pattern = ParseTerm('p(ABBC)')
#term = ParseTerm('p(s(1)s(1)s(1)2d(2))')
#sys.stdout = open('unification.txt', 'w')

#pattern = ParseTerm('t( a(X) b(XY) c(W) d(2Ze(f()g()h())) ) ')
#term = ParseTerm('t( a(4) d(6e(f()g()h())) b(4a()b()c())// c(f()) ) ')

#pattern = ParseTerm('t(aXg(Y))')
#term = ParseTerm('t(af(b())g(c())) ')

pattern = ParseTerm('t(a(XYZ)b(WAB))')
term = ParseTerm('t(a(4)b(2a()b()c())) ')
#term = ParseTerm('t(a(4)b(4)) ') #15
#term = ParseTerm('t(a(2a()b()c())b(2a()b()c())) ') #162

#pattern = ParseTerm('t(a(ABCD)b(WXYZ))')
#term = ParseTerm('t(a(11)b(7)) ')

print('Pattern:', pattern.ToString())
print('Term:', term.ToString())

t1 = int(round(time.time() * 1000))
x = UnifyCompound(pattern,term)
t2 = int(round(time.time() * 1000))
#PrintUnifyCompound(x)
print('Number of unifiers: ', len(x))
print('Unification time: ', t2 - t1, 'milliseconds')