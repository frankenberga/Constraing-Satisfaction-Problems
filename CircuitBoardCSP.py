from CSP import CSP

class CircuitBoardCSP(CSP):
    def __init__(self, size, circuit_components, inf_bool):
        self.values = self.generate_values(size)
        self.variables = self.generate_variables(circuit_components)
        self.init_domains = self.domains(circuit_components, size)
        self.constraints = self.create_constraints(circuit_components, size)
        self.inference_bool = inf_bool
        #print (self.constraints)

    def generateCSP(self, size, circuit_components):
        CSP.__init__(self, self.values, self.variables, self.constraints, self.init_domains, self.inference_bool)
        final_assignment = CSP.backtracking_search(self)
        return final_assignment

    #this method generates the complete list of possible values
    def generate_variables(self, circuit_components):
        variables = []
        count = 0
        while count < len(circuit_components.keys()):
            variables.append(count)
            count += 1
        return variables

   #this method generates the complete list of possible locations 
    def generate_values(self, size):
        values = []
        x = 0
        while x <= size[0]:
            y = 0
            while y <= size[1]:
                loc_tuple = (x, y)
                values.append(loc_tuple)
                y += 1
            x += 1
        return values

    #this method creates the constraint dictinary
    def create_constraints(self, circuit_components, size):
        constraints = dict()
        curr_var = 0
        while curr_var < len(self.variables):
            next_var = curr_var + 1
            while next_var < len(self.variables):
                pair = (curr_var, next_var)
                legal_values = self.get_legal_values(size, curr_var, next_var, circuit_components)
                constraints[pair] = legal_values
                next_var += 1
            curr_var += 1
        return constraints

    def get_legal_values(self, size, curr_var, next_var, circuit_components):
        legal_values = set()
        for loc1 in self.values:
            for loc2 in self.values:
                key1 = list(circuit_components.keys())[curr_var]
                key2 = list(circuit_components.keys())[next_var]
                #determinig the low and high x and y values for each variable
                key1_x_low = loc1[0]
                key1_x_high = circuit_components.get(key1)[0] + loc1[0]
                key2_x_low = loc2[0]
                key2_x_high = circuit_components.get(key2)[0] + loc2[0]
                key1_y_low = loc1[1]
                key1_y_high = circuit_components.get(key1)[1] + loc1[1]
                key2_y_low = loc2[1]
                key2_y_high = circuit_components.get(key2)[1] + loc2[1]
                #make sure it doesn't go past the max x or y value
                if (key1_x_high <= size[0] and key1_y_high <= size[1] and key2_x_high < size[0] and key2_y_high <= size[1]):
                    #make sure the two components aren't overlapping
                    if (key2_x_low >= key1_x_high or key1_x_low >= key2_x_high or key2_y_low >= key1_y_high or key1_y_low >= key2_y_high):
                        new_tuple = (loc1, loc2)
                        legal_values.add(new_tuple)
        return legal_values

    #this method turns the final assignment into a list that can then be printed in a "nice enough" way
    def final_list(self, size, circuit_components, final_assignment):
        final_list = []
        y = 0
        while y < size[1]:
            row_string = ""
            x = 0
            while x < size[0]:
                appended = False
                for key in final_assignment.keys():
                    loc = final_assignment[key]
                    #if the row is greater than the low x value and less than the high x value
                    curr_key = list(circuit_components.keys())[key]
                    curr_value = circuit_components[curr_key]
                    if x >= loc[0] and x < (curr_value[0] + loc[0]):
                        if y >= loc[1] and y < (curr_value[1] + loc[1]):
                            row_string += curr_key
                            appended = True
                if (appended == False): #this adds a period if no character was added in the location
                    row_string += "."
                x += 1
            final_list.append(row_string)
            row_list = []
            y += 1   
        return final_list
             
    #takes solutions from the CSP and outputs them in readable way
    def output(self, size, circuit_components):
        print ("values:" , self.values)
        print ("variables:", self.variables)
        print ("constraints:", self.constraints)
        final_assignment = self.generateCSP(size, circuit_components)
        print ("final assignment:", final_assignment)
        final_list = self.final_list(size, circuit_components, final_assignment)
        print (final_list)
        print ("final circuit board layout:")
        count = len(final_list)
        while count > 0:
            print (final_list[count-1])
            count -= 1

    #this method creates the initial assignment--more for me understanding the problem layout 
    def domains(self, circuit_components, size):
        init_domains = []

        #filling the list with empty sets first
        x = 0
        while x < len(self.variables):
            init_domains.append({})
            x += 1
        #now filling them in correctly
        count = 0
        for key in circuit_components.keys():
            value_set = set()
            for value in self.values:
                if (circuit_components.get(key)[0] + value[0]) <= size[0] and (circuit_components.get(key)[1] + value[1]) <= size[1]:
                    value_set.add(value)
            init_domains[count] = value_set
            count += 1
        return init_domains

    def test(self, size, circuit_components):
        print ("generate CSP")
        self.output(size, circuit_components)
        #print (final_assignment)

    
