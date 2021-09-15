from collections import OrderedDict
from engine import MultisetUnion
from engine import MultisetInclusion
from engine import MultisetIn
from engine import MultisetMinus
from engine import MultisetIntersection
from engine import GROUND
from term import Term

b3 = Term('b','eff')

d1 = OrderedDict()
d1['AA'] = 11
d1['BB'] = 22
d1[3] = 33
d1[b3] = 44
d1['CC'] = 33
d1['DD'] = 44

d2 = OrderedDict()
d2['EE'] = 11
d2['FF'] = 22
d2['CC'] = 33
d2['DD'] = 44

d3 = OrderedDict()
d3['EE'] = 9
d3['FF'] = 21
d3['CC'] = 30

d4 = OrderedDict()

d5 = MultisetUnion(d1,d2)

print(d1,d2,d3,d4,d5)
print(MultisetIntersection(d1,d2))
print(MultisetInclusion(d2,d3))
print(MultisetIntersection(d5,d2))
print(GROUND(d3,d4))
print('-----')
print(GROUND(d1,d2))
print(MultisetMinus(d5,d1))
print(MultisetIn(d4,d4))
print(MultisetIn(d3,d4))
print(MultisetIn(d1,d5))