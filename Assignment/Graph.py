from State import State
import random
import copy


class Graph:

    def __init__(self, numofstates=None, name=None):
        self.states = []
        self.finalstates = []
        self.depth = 0
        if name is None:
            self.name = ""
        else:
            self.name = name
        if numofstates is not None:
            for i in range(numofstates):
                tempstate = State(stateid=i)
                tempstate.accepting = bool(random.getrandbits(1))  # randomly generating whether the state is accepting or rejecting
                tempstate.transitions.update({'a': random.randint(0, numofstates - 1)})
                tempstate.transitions.update({'b': random.randint(0, numofstates - 1)})
                while tempstate.transitions['b'] == tempstate.transitions['a']:  # ensuring the 2 transitions from every state are to different states
                    tempstate.transitions.update({'b': random.randint(0, numofstates - 1)})
                self.states.append(tempstate)
                if tempstate.accepting:
                    self.finalstates.append(tempstate)
            self.startid = random.randint(0, numofstates - 1)  # randomly selecting starting state
            self.states[self.startid].start = True
            self.visitedstates = self.calculatedepth()
            self.reachablestates = []
            for state in self.states:
                if self.visitedstates[state.stateid]:
                    self.reachablestates.append(state)

        # the following variables are used for finding the strongly connected components in the graph using tarjan's algorithm
        self.index = 0
        self.stack = []
        self.largestSCC = 0
        self.smallestSCC = 0
        self.sccs = []


    def minimize(self, name=None):
        newgraph = copy.deepcopy(self)
        if name is not None:
            newgraph.name = name
        stateset = set(newgraph.reachablestates)  # creating set of states from list of states
        for state in newgraph.finalstates:
            if state not in stateset:  # checking with set as opposed to list since checking for existence in a set is O(1) complexity as opposed to O(n) complexity in a list https://www.datacamp.com/community/tutorials/sets-in-python
                newgraph.finalstates.remove(state)  # removing unreachable final states from the list of final states
        partition = [set(newgraph.finalstates), stateset.difference(set(newgraph.finalstates))]
        waitlist = [set(newgraph.finalstates)]  # initializing new sets in both lists so as to not have changes to one set affect the other
        while waitlist:
            A = waitlist.pop(0)
            for char in ['a', 'b']:
                X = set()
                for state in newgraph.reachablestates:
                    tempstate = newgraph.states[state.transitions[char]]
                    if tempstate in A and tempstate not in X:
                        X.update({state})
                for Y in partition:
                    if X.intersection(Y) and Y.difference(X):  # for each set Y in the current partition where X n Y is not empty
                        partition.append(X.intersection(Y))
                        partition.append(Y.difference(X))
                        partition.remove(Y)
                        if Y in waitlist:
                            waitlist.append(X.intersection(Y))
                            waitlist.append(Y.difference(X))
                            waitlist.remove(Y)
                        else:
                            if len(X.intersection(Y)) <= len(Y.difference(X)):
                                waitlist.append(X.intersection(Y))
                            else:
                                waitlist.append(Y.difference(X))
        newstates = []
        newfinalstates = []
        for i in range(len(partition)):
            firststate = next(iter(partition[i]))
            newstate = State(accepting=firststate.accepting, stateid=i)
            for key, value in firststate.transitions.items():
                for x in range(len(partition)):
                    if newgraph.states[value] in partition[x]:
                        newstate.transitions[key] = x
            if newgraph.states[newgraph.startid] in partition[i]:
                newstate.start = True
                newgraph.startid = i
            newstates.append(newstate)
            if newstate.accepting:
                newfinalstates.append(newstate)
        newgraph.states = newstates
        newgraph.finalstates = newfinalstates
        newgraph.reachablestates = newstates
        newgraph.visitedstates = newgraph.calculatedepth()
        return newgraph

    def printdetails(self):
        for state in self.states:
            state.printdetails()
        if self.name == "":
            print("Total nodes in Graph: " + str(len(self.states)))
            print("Depth of Graph from the starting node: " + str(self.depth))
        else:
            print("Total nodes in Graph " + self.name + ": " + str(len(self.states)))
            print("Depth of Graph " + self.name + ": " + str(self.depth))

    def calculatedepth(self):  # Breadth First Search, ref: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/, https://stackoverflow.com/questions/43458102/how-to-get-the-max-depth-of-a-graph-with-bfs
        visitednodes = [False] * (len(self.states))
        searchqueue = []
        self.depth = 0

        searchqueue.append(self.startid)
        searchqueue.append(-1)  # using -1 as marker between levels of the tree formed by the search to know when to increment depth
        visitednodes[self.startid] = True

        while searchqueue:  # Empty list = false, continues looping until search queue is empty
            currentstate = searchqueue.pop(0)
            if currentstate == -1:
                searchqueue.append(-1)
                if searchqueue[0] == -1:
                    break
                else:
                    self.depth += 1
            else:
                for key, value in self.states[currentstate].transitions.items():
                    if not visitednodes[value]:
                        searchqueue.append(value)
                        visitednodes[value] = True

        return visitednodes  # returns the list of states reachable from the start state to determine unreachable states for minimization

    def evaluatestring(self, string):
        currentstate = self.states[self.startid]
        for char in string:
            if char is not '':
                currentstate = self.states[currentstate.transitions[char]]
        if currentstate.accepting:
            return "Accepting"
        else:
            return "Rejecting"


    def printacceptingstates(self):
        for state in self.states:
            if state.accepting:
                print("Accepting")
            else:
                print("Rejecting")

    def strongconnect(self, state):
        state.order = self.index
        state.link = self.index
        self.index += 1
        self.stack.append(state)
        state.onstack = True

        for key, value in state.transitions.items():
            state2 = self.states[value]
            if state2.order == -1:
                self.strongconnect(state2)
                state.link = min(state.link, state2.link)
            elif state2.onstack:
                state.link = min(state.link, state2.order)

        if state.link == state.order:
            scc = []
            while True:
                s = self.stack.pop()
                s.onstack = False
                scc.append(s)
                if s == state:
                    self.sccs.append(scc)
                    if self.largestSCC == 0 & self.smallestSCC == 0:
                        self.largestSCC = len(scc)
                        self.smallestSCC = len(scc)
                    elif self.largestSCC < len(scc):
                        self.largestSCC = len(scc)
                    elif self.smallestSCC > len(scc):
                        self.smallestSCC = len(scc)
                    break



    def tarjansgetSCC(self):  # using tarjan's algorithm to get set of SCC
        for state in self.states:
            if state.order == -1:
                self.strongconnect(state)
        print("Number of strongly connected components in graph", self.name + ":", len(self.sccs))
        print("Size of largest SCC in graph", self.name + ":", self.largestSCC)
        print("Size of smallest SCC in graph", self.name + ":", self.smallestSCC)

