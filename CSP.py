import time

class CSP(): 

    def __init__(self, values, variables, constraints, init_domains, inf_bool):
        self.values = values
        self.variables = variables
        self.constraints = constraints
        self.init_domains = init_domains
        self.inference_dict = self.generate_inference_dict()
        self.inference_bool = inf_bool
        print ("inference dict", self.inference_dict)
        print ("domains", self.init_domains)
        print ("CSP initialized")
   
    #this method generates an inference dictionary where the key is each variable and the value
    #is the other variables they influence/connect with -- it is used for MAC-3
    def generate_inference_dict(self):
        inferences = dict()
        for variable in self.variables:
            variable_arcs = []
            for constraint in self.constraints.keys():
                if variable == constraint[0]:
                    variable_arcs.append(constraint[1])
            inferences[variable] = variable_arcs
        return inferences

    #this actually does the backtracking search, returning solution or failure 
    def backtracking_search(self):
        start_time = time.time()
        assignment = dict()
        return self.backtrack(assignment, start_time)

    #backtrack 
    def backtrack(self, assignment, start_time):
        #if the csp is complete then return it
        if len(assignment) == len(self.variables):
            print ("complete")
            print ("time it took: ", time.time() - start_time)
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_values(variable, assignment): 
            if self.consistent(variable, value, assignment):
                assignment[variable] = value
                complete_domains = self.init_domains
                #so that we can turn inference on and off
                if self.inference_bool:
                    inference = self.mac_3(variable, value, assignment) #update them
                    if inference:
                        result = self.backtrack(assignment, start_time)
                        if result is not None:
                            return result
                else:
                    result = self.backtrack(assignment, start_time)
                    if result is not None:
                        return result
                self.init_domains = complete_domains #reassign the domains if this search path didnt work
                del assignment[variable]
        return None

    #returns false if an inconsistency is found, if not it returns true
    def mac_3(self, variable, value, assignment):
        arc_queue = self.generate_arc(variable, assignment)
        while len(arc_queue) > 0:
            next_var = arc_queue.pop(0)
            if self.revise(value, variable, next_var):
                if (len(self.init_domains[variable]) == 0):
                    return False
                for next_elem in self.neighbors(variable):
                    next_tuple = (next_elem, variable)
        return True

    #this method generates an arc, basically by getting the values from the inference dictionary
    #but removing them if they are already in the assignment
    def generate_arc(self, variable, assignment):
        arc_queue = self.inference_dict.get(variable)
        for x in arc_queue:
            if x in assignment.keys():
                arc_queue.remove(x)
        return arc_queue

    #this method updates the rest of the graph 
    def revise(self, value, variable1, variable2):
        revised = False
        some_value_exists = False
        var_tuple = (variable1, variable2)
        value2_list = self.init_domains[variable2]
        for value2 in value2_list.copy():
            value_tuple = (value, value2)
            if value_tuple in self.constraints.get(var_tuple):
                some_value_exists = True
        if some_value_exists == False:
            self.init_domains[variable2].remove(value2)
            revised = True
        return revised

    #this method gets the neighbors
    def neighbors(self, variable):
        neighbors_list = list()
        for constraint in self.constraints.keys():
            if variable == constraint[0]:
                neighbors_list.append(constraint[1])
            elif variable == constraint[1]:
                neighbors_list.append(constraint[0])
        return neighbors_list

    #this method adds inferences to the assignment
    def add_inferences(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                inferences = self.init_domains[variable]
                assignment[variable] = inferences
        return assignment

    #this method selects variables that are not yet assigned
    def select_unassigned_variable(self, assignment):
        naive = True #this boolean toggles which variable selecting method you are doing
        if (naive):
            return self.select_variable_naive(assignment)
        else:
            return self.minimum_remaining_values(assignment)
    
    #this method selects variables that are not yet assigned in the order they are in the variables list
    def select_variable_naive(self, assignment):
        x = 0
        while x < len(self.variables):
            var = self.variables[x]
            if var in assignment.keys():
                x += 1
            else:
                x += 1
                return var #for now just obtaining the next key in the dictionary 
    
    #this method checks the variable that has the fewest remaining variables left
    def minimum_remaining_values(self, assignment):
        next_variable = None
        fewest_var = 10000
        for variable in self.variables:
            if variable not in assignment.keys():
                num_val_remaining = len(self.init_domains[variable])
                if num_val_remaining < fewest_var:
                    fewest_var = num_val_remaining
                    next_variable = variable
        return next_variable

    #this method orders the values that are returned
    def order_values(self, variable, assignment):
        naive = True
        if (naive):
            values = self.init_domains[variable]
            return values #for now just returning them in the list they came in
        else:
            return self.least_constraining_values(variable, assignment)

    #this method orders the values to be searched by putting the least constraining values first
    def least_constraining_values(self, variable, assignment):
        lcv = []
        final_lcv = []
        for value in self.init_domains[variable]:
            var_changed = self.forward_checking(value, variable)
            next_tuple = (var_changed, value)
            lcv.append(next_tuple)
        lcv.sort()
        for x in lcv:
            final_lcv.append(x[1])
        return final_lcv

    #this method does forward checking for the least constrianing values heuristic
    def forward_checking(self, value, variable1):
        var_changed = 0
        some_value_changed = False
        for variable2 in self.inference_dict.get(variable1):
            var_tuple = (variable1, variable2)
            value2_list = self.init_domains[variable2]
            for value2 in value2_list.copy():
                value_tuple = (value, value2)
                if value_tuple not in self.constraints.get(var_tuple):
                    var_changed += 1
        return var_changed

    #this method checks to make sure the value selected is consistent with the assignment already 
    def consistent(self, variable, value, assignment):
        bool_consistent = True
        if len(assignment) == 0:
            return bool_consistent
        else:
            for item in assignment.keys(): #problem HERE HERE HERE 
                tuple1 = (variable, item)
                tuple2 = (item, variable)
                if tuple1 in self.constraints.keys():
                    item_value = assignment[item]
                    tuple_value = (value, item_value)
                    if tuple_value not in list(self.constraints.get(tuple1)):
                        bool_consistent = False
                        return bool_consistent         
                elif tuple2 in self.constraints.keys():
                    item_value = assignment[item]
                    tuple_value = (item_value, value)
                    if tuple_value not in list(self.constraints.get(tuple2)):
                        bool_consistent = False
                        return bool_consistent         
            return bool_consistent
                


        
