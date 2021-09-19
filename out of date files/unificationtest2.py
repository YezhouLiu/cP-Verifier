from cpparser import ParseTerm
from toolbox import UnifyCompound
from toolbox import PrintUnifyCompound
import sys
import time

pattern = ParseTerm('f(a(XY)b(AB))')
term = ParseTerm('f(a(2)b(c()d())) ')


print('Pattern:', pattern.ToString())
print('Term:', term.ToString())

t1 = int(round(time.time() * 1000))
x = UnifyCompound(pattern,term)
t2 = int(round(time.time() * 1000))
PrintUnifyCompound(x)
print('Number of unifiers: ', len(x))
print('Unification time: ', t2 - t1, 'milliseconds')
