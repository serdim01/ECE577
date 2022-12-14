# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 14:12:49 2022

@author: CJ
"""
import csv
import time
from operator import attrgetter  
    
class city_US(object):
    def __init__(self, name, number, state):
        self.Name = name
        self.children = dict()
        self.Number = number
        self.State = state
    def add_child(self, name, cost):
        self.children[name] = cost

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

def main():
    # cityGraph is our problem space - all 
    cityGraph = readinTowns()
    frontier = []
    frontier_dict = dict()
    visited_dict = dict()
    
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
    frontier = [priorityQueueObject(cityGraph[start].Number, 0)];      
    current_state = frontier[0]
    frontier_dict[current_state.Number] = Tree(current_state.Number, 0)
    
     # Goal Check - Loop until we reach goal
    while(current_state.Number != goal):
        # Explore on current level - kids is the city ID number [string]
        # Iterate through adjacent towns fro current state
        for kids in cityGraph[current_state.Number].children:
            # Check if the adjacent towns is in visited dict or frontier dict
            # Only add if not in visited or frontier 
            # If is in frontier with higher cost - replace
            if not(kids in visited_dict.keys()):
                if (kids in frontier_dict.keys()):
                    pathCostInFrontier = frontier_dict[kids].PathCost
                    pathCostToChild = current_state.PathCost + float(cityGraph[current_state.Number].children[kids])
                    if (pathCostInFrontier > pathCostToChild):
                        for x in frontier:
                            if x.PathCost == pathCostInFrontier:
                                break
                        frontier.remove(x)
                        frontier.append(priorityQueueObject(kids,pathCostToChild ))
                        del frontier_dict[kids]
                        frontier_dict[kids] = frontier_dict[current_state.Number].add_child(kids, pathCostToChild)
                elif not(kids in frontier_dict.keys()):
                    # Add children to current state frontier dict
                    # Children are themselves a tree node
                    pathCostToChild = current_state.PathCost + float(cityGraph[current_state.Number].children[kids])
                    frontier_dict[kids] = frontier_dict[current_state.Number].add_child(kids, pathCostToChild)
                    frontier.append(priorityQueueObject(kids,pathCostToChild ))
                    
        # Add current state to visited - visited is the main tree we are creating            
        visited_dict[current_state.Number] = frontier_dict[current_state.Number] 
        frontier.remove(current_state)
        del frontier_dict[current_state.Number]
        nextState = min(frontier,key=attrgetter('PathCost'))
        
        # If no more items in our queue then we cannot reach goal
        if len(frontier) == 0:
            print("No possible route")
            return
        
        # Dequeue Current state and delete from fronteir dict        
        current_state = nextState  
    
        # Print excecution time
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    print()
    
    # Bookeeping - don't add goal to visited in loop - do now for graph traversal    
    visited_dict[current_state.Number] = frontier_dict[current_state.Number]  
    
    # Use visited tree to find path found
    state = current_state.Number
    path_reverse_order = list()
    while state != start:
        path_reverse_order.append(cityGraph[state].Name + ", " + (cityGraph[state].State))
        state = visited_dict[state].parent.data
 
    # Loop won't add start
    path_reverse_order.append(cityGraph[start].Name + ", " + (cityGraph[start].State))
    # Reverse order as we started at goal
    path_reverse_order.reverse()
    # Print Route
    for cities in path_reverse_order:
        if cities == (goal_city + ", " + goal_state):
            print(cities)
        else:
            print(cities + " -> ", end='')
    print()        
    print("Final distance = " + str(current_state.PathCost))
    
if __name__ == "__main__":
    main()