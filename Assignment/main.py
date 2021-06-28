import random
from Graph import Graph


def generatestring():
    length = random.randint(0, 128)
    string = ""
    for i in range(length):
        charnum = random.randint(0, 1)
        if charnum == 0:
            string = string + 'a'
        else:
            string = string + 'b'
    return string


def classifystring(a, m):
    for i in range(100):
        teststring = generatestring()
        print(str(i + 1) + " " + teststring + " :: " + a.evaluatestring(teststring) + " in automaton " + a.name)
        print(str(i + 1) + " " + teststring + " :: " + m.evaluatestring(teststring) + " in automaton " + m.name)


A = Graph(random.randint(16, 64), "A")
A.printdetails()
M = A.minimize("M")
M.printdetails()

classifystring(A, M)

M.tarjansgetSCC()

