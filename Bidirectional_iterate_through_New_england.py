# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:59:20 2022

@author: CJ
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 14:12:49 2022
@author: CJ
"""
import queue
import csv
import time
    
class city_US(object):
    def __init__(self, name, number, state):
        self.Name = name
        self.children = dict()
        self.Number = number
        self.State = state
    def add_child(self, name, cost):
        self.children[name] = cost

# Not ranking here just using object
class priorityQueueObject(object):
    def __init__(self, name, pathcost):
        self.Number = name
        self.PathCost = pathcost
        
def readinTowns():
    cityDict = dict()
    # Create all entries of Dict with txt file with all city names
    # Dict keys will be a unique number identifier to avoid cities w/ same name in diff states
    with open("C:/Users/CJ/Documents/Grad_2022-23/ECE577/Project1/sf12010placename.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                StateNumber = int(row[0])*100000 + int(row[2])
                StateNumberStr = str(StateNumber).zfill(7)
                cityDict[StateNumberStr] = city_US(row[3], StateNumberStr, row[1])
    # Add adjacent towns within 25 mile radius of each town in dict            
    with open("C:/Users/CJ/Documents/Grad_2022-23/ECE577/Project1/sf12010placedistance25miles.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                StateNumber1 = int(row[0])*100000 + int(row[1])
                StateNumberStr1 = str(StateNumber1).zfill(7)
                StateNumber2 = int(row[3])*100000 + int(row[4])
                StateNumberStr2 = str(StateNumber2).zfill(7)
                cityDict[StateNumberStr1].add_child(StateNumberStr2, row[2])    
    return cityDict

# https://stackoverflow.com/questions/41760856/most-simple-tree-data-structure-in-python-that-can-be-easily-traversed-in-both
# https://stackoverflow.com/questions/41760856/most-simple-tree-data-structure-in-python-that-can-be-easily-traversed-in-both
class Tree(object):
    def __init__(self, data, pathcost, children=None, parent=None):
        self.data = data
        self.PathCost = pathcost
        self.children = children or []
        self.parent = parent

    def add_child(self, data, pathCost):
        new_child = Tree(data, pathCost, parent=self)
        self.children.append(new_child)
        return new_child
    
    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return not self.children

    def __str__(self):
        if self.is_leaf():
            return str(self.data)
        return '{data} [{children}]'.format(data=self.data, children=', '.join(map(str, self.children)))  
        
def intersection_check(intersections, visited_dict1, visited_dict2, cityGraph, start, goal):
    depth_of_ints = []
    for int_points in intersections:
        # Use visited tree to find path found
        state = int_points
        path_reverse_order1 = list()
    
        while state != start:
            path_reverse_order1.append(cityGraph[state].Name + ", " + (cityGraph[state].State))
            state = visited_dict1[state].parent.data
    
        path_reverse_order2 = list()
        state = int_points
        while state != goal:
            path_reverse_order2.append(cityGraph[state].Name + ", " + (cityGraph[state].State))
            state = visited_dict2[state].parent.data
                # Loop won't add start
        path_reverse_order1.append(cityGraph[start].Name + ", " + (cityGraph[start].State))
        path_reverse_order2.append(cityGraph[goal].Name + ", " + (cityGraph[goal].State))
        # Reverse order as we started at goal
        path_reverse_order1.reverse()
        path = path_reverse_order1 + path_reverse_order2[1:]
        depth_of_ints.append(len(path) - 1)
    index_min = min(range(len(depth_of_ints)), key=depth_of_ints.__getitem__) 
    return index_min

def main():
    # cityGraph is our problem space - all
    cityGraph = readinTowns()
    frontier1 = queue.Queue()
    frontier_dict1 = dict()
    visited_dict1 = dict()
    frontier2 = queue.Queue()
    frontier_dict2 = dict()
    visited_dict2 = dict()
    
    file = open("BD_NewEngland_Results.txt", "w")
    writer = csv.writer(file)
    writer.writerow(["ID Number", "City Name", "State", "Depth", "Excecution Time", "Cost", "Nodes Expanded"])
    #Goals
    start = "2545000"
    Goal_cities = []
    for cities in cityGraph:
        if cityGraph[cities].State == "Massachusetts" or cityGraph[cities].State == "Vermont" or cityGraph[cities].State == "Rhode Island" or cityGraph[cities].State == "Connecticut" or cityGraph[cities].State == "Maine" or cityGraph[cities].State == "New Hampshire":
            if cityGraph[cities].Number != start:
                Goal_cities.append(cityGraph[cities].Number)
    
    for goal in Goal_cities:    
        frontier_dict1 = dict()
        visited_dict1 = dict()
        frontier_dict2 = dict()
        visited_dict2 = dict()
        frontier1 = [priorityQueueObject(cityGraph[start].Number, 0)];
        frontier2 = [priorityQueueObject(cityGraph[goal].Number, 0)];
        # Initial update of current state      
        current_state1 = frontier1.pop(-1)
        current_state2 = frontier2.pop(-1)
        
        frontier_dict1[current_state1.Number] = Tree(current_state1.Number, 0)
        frontier_dict2[current_state2.Number] = Tree(current_state2.Number, 0)
        
        intersections = 0;
        intersection_point = list();
        intersection_costs = []
        level = 0
        no_route = 0
        number_of_nodes_on_current_depth1 = 0
        number_of_nodes_on_current_depth2 = 0
        st = time.time()   
        while(1):
        # Explore on current level - kids is the city ID number [string]
        # Iterate through adjacent towns fro current state
            level+=1
            number_of_nodes_on_current_depth1 = (len(frontier1) - number_of_nodes_on_current_depth1)
            number_of_nodes_on_current_depth2 = (len(frontier2) - number_of_nodes_on_current_depth2)
        ## From start branch
            iterations = 1
            while(1):
                iterations+=1
                for kids in cityGraph[current_state1.Number].children:
            # Check if the adjacent towns is in visited dict or frontier dict
            # Only add if not in visited or frontier
                    if not(kids in visited_dict1.keys()):
                        if not(kids in frontier_dict1.keys()):
                    # Enqueue to frontier
                            pathCostToChild = current_state1.PathCost + float(cityGraph[current_state1.Number].children[kids])
                            frontier_dict1[kids] = frontier_dict1[current_state1.Number].add_child(kids, pathCostToChild)
                            frontier1.append(priorityQueueObject(kids,pathCostToChild ))
                        # Add children to current state frontier dict
                        # Children are themselves a tree node
                            if kids in frontier_dict2.keys():
                                intersections+=1;
                                intersection_point.append(kids)
                                intersection_costs.append(pathCostToChild + frontier_dict2[kids].PathCost)
                                visited_dict1[kids] = frontier_dict1[kids]
                                visited_dict2[kids] = frontier_dict2[kids] 
                visited_dict1[current_state1.Number] = frontier_dict1[current_state1.Number] 
                if len(frontier1) == 0:
                    break
                else:
                    del frontier_dict1[current_state1.Number]
                current_state1 = frontier1.pop(0)
                if not(iterations < number_of_nodes_on_current_depth1):
                    break
        ## From goal branch
            iterations = 1
            while(1):
                iterations+=1
                for kids in cityGraph[current_state2.Number].children:
            # Check if the adjacent towns is in visited dict or frontier dict
            # Only add if not in visited or frontier
                    if not(kids in visited_dict2.keys()):
                        if not(kids in frontier_dict2.keys()):
                    # Enqueue to frontier
                            pathCostToChild = current_state2.PathCost + float(cityGraph[current_state2.Number].children[kids])
                            frontier_dict2[kids] = frontier_dict2[current_state2.Number].add_child(kids, pathCostToChild)
                            frontier2.append(priorityQueueObject(kids,pathCostToChild ))
                    # Add children to current state frontier dict
                    # Children are themselves a tree node
                            if kids in frontier_dict1.keys():
                                intersections+=1;
                                intersection_point.append(kids)
                                intersection_costs.append(pathCostToChild + frontier_dict1[kids].PathCost)
                                visited_dict1[kids] = frontier_dict1[kids]
                                visited_dict2[kids] = frontier_dict2[kids]  
            # Add current state to visited - visited is the main tree we are creating
                visited_dict2[current_state2.Number] = frontier_dict2[current_state2.Number] 
                if len(frontier2) == 0:
                    break
                else:
                    del frontier_dict2[current_state2.Number]
                current_state2 = frontier2.pop(0)
                if not(iterations < number_of_nodes_on_current_depth2):
                    break
            if intersections > 0:
                break;
            if len(frontier1) == 0 and len(frontier2) == 0:
                print("No possible route for " + cityGraph[start].Name + " to " + cityGraph[goal].Name)
                intersection_point.append(current_state2.Number)
                no_route = 1;
                break
                                            
        # If no more items in our queue then we cannot reach goal

#        # Dequeue Current state and delete from fronteir dict        
#
#            if len(frontier1) > 0 and len(frontier2) > 0:
#                visited_dict1[current_state1.Number] = frontier_dict1[current_state1.Number] 
#                visited_dict2[current_state2.Number] = frontier_dict2[current_state2.Number]
#                del frontier_dict1[current_state1.Number]
#                del frontier_dict2[current_state2.Number]
#                current_state1 = frontier1.pop(0)
#                current_state2 = frontier2.pop(0)
#            elif len(frontier1) > 0:
#                visited_dict1[current_state1.Number] = frontier_dict1[current_state1.Number]
#                del frontier_dict1[current_state1.Number]     
#                current_state1 = frontier1.pop(0)
#            else:
#                visited_dict2[current_state2.Number] = frontier_dict2[current_state2.Number]
#                del frontier_dict2[current_state2.Number]
#                current_state2 = frontier2.pop(0)


    
    # Bookeeping - don't add goal to visited in loop - do now for graph traversal
        et = time.time()
        if not(no_route):
            if not(intersection_point == start):
    # Use visited tree to find path found
                path_reverse_order1 = list()
                best_intersection_index = intersection_check(intersection_point, visited_dict1, visited_dict2, cityGraph, start, goal)
                best_intersection = intersection_point[best_intersection_index]
                state = best_intersection
                while state != start:
                    path_reverse_order1.append(cityGraph[state].Name + ", " + (cityGraph[state].State))
                    state = visited_dict1[state].parent.data
    
                path_reverse_order2 = list()
                state = best_intersection
                while state != goal:
                    path_reverse_order2.append(cityGraph[state].Name + ", " + (cityGraph[state].State))
                    state = visited_dict2[state].parent.data
        
    # Loop won't add start
                path_reverse_order1.append(cityGraph[start].Name + ", " + (cityGraph[start].State))
                path_reverse_order2.append(cityGraph[goal].Name + ", " + (cityGraph[goal].State))
    # Reverse order as we started at goal
                path_reverse_order1.reverse()
                path = path_reverse_order1 + path_reverse_order2[1:]
            
            else:
                path = [(cityGraph[start].Name + ", " + (cityGraph[start].State)), (cityGraph[goal].Name + ", " + (cityGraph[goal].State))] ;
  
            depth =len(path) - 1
            elapsed_time = et - st
            
            finalPathCost = intersection_costs[best_intersection_index] 
            writer.writerow([cityGraph[goal].Number, cityGraph[goal].Name, cityGraph[goal].State, depth, elapsed_time, finalPathCost, len(visited_dict1) + len(visited_dict2)])
#            for cities in path:
#                if cities == (cityGraph[goal].Name + ", " + cityGraph[goal].State):
#                    print(cities)
#                else:
#                    print(cities + " -> ", end='')
                
                
if __name__ == "__main__":
    main()