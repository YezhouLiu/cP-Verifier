from collections import OrderedDict

d1 = OrderedDict()

l1 = [['A','B','C','D','E'], ['A','B','E','F','G'], ['B','A','E','F'], ['A','B','C','F'], ['A','B','C','H']]

def buildtree (list1, dict1):
    if len(list1) > 0:
        if not list1[0] in dict1:
            dict1[list1[0]] = OrderedDict()
        buildtree (list1[1:], dict1[list1[0]])

for l2 in l1:
    buildtree (l2, d1)
print (d1)

space1 = '  '

def printpretty (layer, d1): #display
    for key in d1:
        if len(d1) < 4:
            print(space1 * layer, key)
        else:
            print(space1 * layer, key, '*')
        printpretty (layer+1, d1[key])

printpretty (1, d1)

ll1 = ['A','B','C','E']
buildtree (ll1, d1)
printpretty (1, d1)

