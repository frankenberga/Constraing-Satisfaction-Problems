
from CSP import CSP

class MapColoringCSP(CSP):
    def __init__(self, word_variables, word_values, word_constraints, inf_bool):
        self.values = self.convert_num(word_values)
        self.variables = self.convert_variables(word_variables)
        self.init_domains = self.domains(word_variables, word_values)
        self.constraints = self.convert_constraints(word_constraints, word_variables)
        self.inference_bool = inf_bool

    def generateCSP(self, word_values, word_variables):
        CSP.__init__(self, self.values, self.variables, self.constraints, self.init_domains, self.inference_bool)
        final_assignment = CSP.backtracking_search(self)
        print ("final assignment", final_assignment)
        return final_assignment
        #self.output(word_variables, word_values, final_assignment)

    #this turns the word variables and the word values into the initial assignments for all of them
    def domains(self, word_variables, word_values):
        init_domains = []

        #filling the list with empty sets first
        x = 0
        while x < len(word_variables):
            init_domains.append({})
            x += 1
        counter = 0
        #now going back through and filling them in
        while counter < len(word_variables):
            init_domains[counter] = self.values
            counter += 1
        return init_domains

    #a method that converts a string to a numerical representation of that string
    def convert_num(self, word_values):
        count = 0
        value_set = set()
        for x in word_values:
            value_set.add(count)
            count += 1
        return value_set
    
    def convert_variables(self, word_variables):
        count = 0
        variables = []
        while count < len(word_variables):
            variables.append(count)
            count += 1
        return variables

    #this method converts the constraints from the initial problem statement to 
    #numerical values that can be used with general CSP
    def convert_constraints(self, word_constraints, word_variables):
        constraints = dict()
        curr_var = 0
        constrained = self.get_constrained()
        not_constrained = self.get_not_constrained()
        while curr_var < len(self.variables):
            next_var = curr_var + 1
            while next_var < len(self.variables):
                pair = (curr_var, next_var)
                if self.pair_constrained(pair, word_constraints, word_variables):     
                    legal_values = constrained
                else:
                    legal_values = not_constrained
                constraints[pair] = legal_values
                next_var += 1
            curr_var += 1
        return constraints

    #this method returns a list of tuple values for the case where two variables are not constrained
    def get_not_constrained(self):
        not_constrained = list()
        for x in self.values:
            for y in self.values:
                pair = (x, y)
                not_constrained.append(pair)
        return not_constrained

    #this method returns a list of tuple values for the case where two variables are not constrained
    def get_constrained(self):
        constrained = list()
        for x in self.values:
            for y in self.values:
                if x != y:
                    pair = (x, y)
                    constrained.append(pair)
        return constrained

    #returns true if a pair of values is a part of the constraint graph, false if it is not
    def pair_constrained(self, pair, word_constraints, word_variables):
        elem1 = pair[0]
        word_elem1 = word_variables[elem1]
        elem2 = pair[1]
        word_elem2 = word_variables[elem2]
        for rule in word_constraints:
            if word_elem1 in rule:
                if word_elem2 in rule:
                    return True
        return False

    #takes solutions from the CSP and outputs them in readable way
    def output(self, word_variables, word_values):
        print ("values", self.values)
        print ("variables", self.variables)
        print ("constraints", self.constraints)
        word_output = []
        count = 0
        final_assignment = self.generateCSP(word_variables, word_values)
        while count < len(final_assignment):
            value = final_assignment[count]
            word_output.append("state: " + word_variables[count] + ", color: " + word_values[value])
            count += 1
        print (word_output)
    
    def test(self, word_variables, word_values):
        print ("generate CSP")
        self.output(word_variables, word_values)
        


    


