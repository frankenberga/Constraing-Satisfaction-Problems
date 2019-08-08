from MapColoringCSP import MapColoringCSP
from CircuitBoardCSP import CircuitBoardCSP
from CSP import CSP

#this class just tests the two different CSP's (Map coloring and Circuit board)

word_variables = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
word_values = ["red", "green", "blue"]
word_constraints = {("SA", "WA"), ("SA", "NT"), ("SA", "Q"), ("SA", "NSW"), ("SA", "V"), 
    ("WA", "NT"), ("NT", "Q"), ("Q", "NSW"), ("NSW", "V")}

# csp = MapColoringCSP(word_variables, word_values, word_constraints, True)
# MapColoringCSP.test(csp, word_variables, word_values)

size = (10, 3)
circuit_components = {'a': (3,2), 'b': (5, 2), 'c': (2, 3), 'e': (7, 1)}

csp = CircuitBoardCSP(size, circuit_components, True)
CircuitBoardCSP.test(csp, size, circuit_components)