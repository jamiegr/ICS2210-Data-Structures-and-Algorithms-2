class State:

    def __init__(self, accepting=None, transitions=None, stateid=None):
        self.start = False
        self.onstack = False  # used for tarjan's algorithm
        self.order = -1  # used for tarjan's algorithm
        self.link = -1  # used for tarjan's algorithm
        if accepting is None:
            self.accepting = False
        else:
            self.accepting = accepting
        if transitions is None:
            self.transitions = {
                'a': 0,
                'b': 0
            }
        else:
            self.transitions = transitions
        if stateid is None:
            self.stateid = 0
        else:
            self.stateid = stateid

    def printdetails(self):
        print("State ID:", self.stateid)
        print("Is final state:", self.accepting)
        print("Is start state:", self.start)
        print("A ->", self.transitions['a'], ", B ->", self.transitions['b'])
