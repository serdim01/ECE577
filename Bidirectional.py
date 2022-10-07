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
    return intersections[index_min]

def exhaust_frontier(frontier1, frontier2, frontier_dict1, frontier_dict2, intersections, cityGraph, visited_dict1, visited_dict2):
    while((len(frontier1) > 0) and (len(frontier2) > 0)):
        current_state1 = frontier1.pop(0)
        current_state2 = frontier2.pop(0)
        ## From start branch
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
                        intersections.append(kids)
                        visited_dict1[kids] = frontier_dict1[kids]
                        visited_dict2[kids] = frontier_dict2[kids] 

        ## From start branch
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
                        intersections.append(kids)
                        visited_dict1[kids] = frontier_dict1[kids]
                        visited_dict2[kids] = frontier_dict2[kids]  
        # Add current state to visited - visited is the main tree we are creating            
        visited_dict1[current_state1.Number] = frontier_dict1[current_state1.Number] 
        visited_dict2[current_state2.Number] = frontier_dict2[current_state2.Number]  
        # Add current state to visited - visited is the main tree we are creating            
        visited_dict1[current_state1.Number] = frontier_dict1[current_state1.Number] 
        visited_dict2[current_state2.Number] = frontier_dict2[current_state2.Number] 
    return intersections
    
def main():
    # cityGraph is our problem space - all 
    cityGraph = readinTowns()
    
    frontier_dict1 = dict()
    visited_dict1 = dict()

    frontier_dict2 = dict()
    visited_dict2 = dict()
    # Get user input for start and goal
    start = 0
    while (start == 0):
        print("Enter start state:" )
        start_state = input()
        print("Enter start city:")
        start_city = input()
        for city in cityGraph:
            if ((cityGraph[city].Name == start_city) and (cityGraph[city].State == start_state)):
                start = cityGraph[city].Number
        if (start == 0):
            print("Invalid city name!")    
    goal = 0
    while (goal == 0):
        print("Enter destination state:" )
        goal_state = input()
        print("Enter destination city:")
        goal_city = input()
        # Initial Goal Check
        for city in cityGraph:
            if ((cityGraph[city].Name == goal_city) and (cityGraph[city].State == goal_state)):
                goal = cityGraph[city].Number
        if (goal == 0):
            print("Invalid city name!")
    st = time.time()
    
    frontier1 = [priorityQueueObject(cityGraph[start].Number, 0)]; 
    frontier2 = [priorityQueueObject(cityGraph[goal].Number, 0)]; 
    # Initial update of current state      
    current_state1 = frontier1.pop(0)
    current_state2 = frontier2.pop(0)
    
    frontier_dict1[current_state1.Number] = Tree(current_state1.Number,0)
    frontier_dict2[current_state2.Number] = Tree(current_state2.Number,0)
        
    frontier_intersection_flag = 0
    intersections = 0;
    intersection_point = [];
    # Goal Check - Loop until we reach goal
    while(1):
        # Explore on current level - kids is the city ID number [string]
        # Iterate through adjacent towns fro current state
        
        ## From start branch
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
                        visited_dict1[kids] = frontier_dict1[kids]
                        visited_dict2[kids] = frontier_dict2[kids] 

        ## From goal branch
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
                        visited_dict1[kids] = frontier_dict1[kids]
                        visited_dict2[kids] = frontier_dict2[kids]  
        # Add current state to visited - visited is the main tree we are creating            
        visited_dict1[current_state1.Number] = frontier_dict1[current_state1.Number] 
        visited_dict2[current_state2.Number] = frontier_dict2[current_state2.Number] 
        
        
        if intersections > 0:
            break;
        # If no more items in our queue then we cannot reach goal
        if len(frontier1) == 0 or len(frontier2) == 0:
            print("No possible route")
            return
        
        # Dequeue Current state and delete from fronteir dict        
        del frontier_dict1[current_state1.Number]
        del frontier_dict2[current_state2.Number]
        current_state1 = frontier1.pop(0)
        current_state2 = frontier2.pop(0)
    
    # Print excecution time
    et = time.time()
    elapsed_time = et - st
    
    print('Execution time:', elapsed_time, 'seconds')
    print()
    print("Number of Nodes Visited: " + str(len(visited_dict1) + len(visited_dict2))) 
    num_nodes = len(visited_dict1) + len(visited_dict2);
    # Use visited tree to find path found
    #exhaust_frontier(frontier1, frontier2, frontier_dict1, frontier_dict2, intersections, cityGraph, visited_dict1, visited_dict2)
    all_intersections = exhaust_frontier(frontier1, frontier2, frontier_dict1, frontier_dict2, intersection_point, cityGraph, visited_dict1, visited_dict2)
    # intersection_check(intersections, visited_dict1, visited_dict2, cityGraph, start, goal)
    best_intersection = intersection_check(all_intersections, visited_dict1, visited_dict2, cityGraph, start, goal)
    state = best_intersection
    path_reverse_order1 = list()
    
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
    depth =len(path) - 1
    print("Depth = " + str(depth))
           
    # Print Route
    for cities in path:
        if cities == (goal_city + ", " + goal_state):
            print(cities)
        else:
            print(cities + " -> ", end='')
                
if __name__ == "__main__":
    main()