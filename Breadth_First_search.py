# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 14:12:49 2022

@author: CJ
"""
# https://stackoverflow.com/questions/2482602/a-general-tree-implementation
import queue
import csv
import time
    
class TreeNode(object):
    def __init__(self, name):
        self.Name = name
        self.children = dict()

    def add_child(self, name, cost):
        self.children[name] = cost

class TreeNode_US(object):
    def __init__(self, name, number, state):
        self.Name = name
        self.children = dict()
        self.Number = number
        self.State = state
    def add_child(self, name, cost):
        self.children[name] = cost

def readinTowns():
    cityDict = dict()
    with open("C:/Users/CJ/Documents/Grad_2022-23/ECE577/Project1/sf12010placename.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                StateNumber = int(row[0])*100000 + int(row[2])
                StateNumberStr = str(StateNumber).zfill(7)
                cityDict[StateNumberStr] = TreeNode_US(row[3], StateNumberStr, row[1])
                
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

        
def createRomaniaTree():
    mapDict = dict();
    Arad = TreeNode("Arad")
    Arad.add_child("Zerind", 75)
    Arad.add_child("Timisoara", 118)
    Arad.add_child("Sibiu", 140)
    mapDict["Arad"] = Arad    

    Zerind = TreeNode("Zerind")
    Zerind.add_child("Arad", 75)
    Zerind.add_child("Oradea", 71)
    mapDict["Zerind"] = Zerind
    
    Oradea = TreeNode("Oradea")
    Oradea.add_child("Sibiu", 151)
    Oradea.add_child("Zerind", 71)
    mapDict["Oradea"] = Oradea
    
    Sibiu = TreeNode("Sibiu")
    Sibiu.add_child("Oradea", 151)
    Sibiu.add_child("Fagaras", 99)
    Sibiu.add_child("Arad", 140)
    Sibiu.add_child("Rimnicu_Vilcea", 80)
    mapDict["Sibiu"] = Sibiu    

    Fagaras = TreeNode("Fagaras")
    Fagaras.add_child("Bucharest", 211)
    Fagaras.add_child("Sibiu", 99)
    mapDict["Fagaras"] = Fagaras

    Bucharest = TreeNode("Bucharest")
    Bucharest.add_child("Fagaras", 211)
    Bucharest.add_child("Giurgiu", 90)
    Bucharest.add_child("Pitesti", 101)
    Bucharest.add_child("Urziceni", 85)    
    mapDict["Bucharest"] = Bucharest

    Urziceni = TreeNode("Urziceni")
    Urziceni.add_child("Vaslui", 142)
    Urziceni.add_child("Hirsova", 98)
    Urziceni.add_child("Bucharest", 85)    
    mapDict["Urziceni"] = Urziceni     

    Hirsova = TreeNode("Hirsova")
    Hirsova.add_child("Eforie", 86)
    Hirsova.add_child("Urziceni", 98)   
    mapDict["Hirsova"] = Hirsova 

    Eforie = TreeNode("Eforie")
    Eforie.add_child("Hirsova", 86)  
    mapDict["Eforie"] = Eforie

    Vaslui = TreeNode("Vaslui")
    Vaslui.add_child("Urziceni", 142)
    Vaslui.add_child("Iasi", 92)   
    mapDict["Vaslui"] = Vaslui

    Iasi = TreeNode("Iasi")
    Iasi.add_child("Neamt", 87)
    Iasi.add_child("Vaslui", 92)   
    mapDict["Iasi"] = Iasi   

    Neamt = TreeNode("Neamt")
    Neamt.add_child("Iasi", 87)  
    mapDict["Neamt"] = Neamt

    Giurgiu = TreeNode("Giurgiu")
    Giurgiu.add_child("Bucharest", 90)  
    mapDict["Giurgiu"] = Giurgiu

    Pitesti = TreeNode("Pitesti")
    Pitesti.add_child("Craiova", 138)
    Pitesti.add_child("Rimnicu_Vilcea", 97)  
    Pitesti.add_child("Bucharest", 101)  
    mapDict["Pitesti"] = Pitesti
    
    Rimnicu_Vilcea = TreeNode("Rimnicu_Vilcea")
    Rimnicu_Vilcea.add_child("Craiova", 146)
    Rimnicu_Vilcea.add_child("Pitesti", 97)  
    Rimnicu_Vilcea.add_child("Sibiu", 80)  
    mapDict["Rimnicu_Vilcea"] = Rimnicu_Vilcea
    
    Craiova = TreeNode("Craiova")
    Craiova.add_child("Rimnicu_Vilcea", 146)
    Craiova.add_child("Pitesti", 138)  
    Craiova.add_child("Drobeta", 120)  
    mapDict["Craiova"] = Craiova
 
    Drobeta = TreeNode("Drobeta")
    Drobeta.add_child("Craiova", 120)
    Drobeta.add_child("Mehadia", 75)   
    mapDict["Drobeta"] = Drobeta
    
    Mehadia = TreeNode("Mehadia")
    Mehadia.add_child("Drobeta", 75)
    Mehadia.add_child("Lugoj", 70)   
    mapDict["Mehadia"] = Mehadia

    Lugoj = TreeNode("Lugoj")
    Lugoj.add_child("Mehadia", 70)
    Lugoj.add_child("Timisoara", 111)   
    mapDict["Lugoj"] = Lugoj

    Timisoara = TreeNode("Timisoara")
    Timisoara.add_child("Arad", 70)
    Timisoara.add_child("Lugoj", 111)   
    mapDict["Timisoara"] = Timisoara
    
    return mapDict

def main():
    #mapGraph = createRomaniaTree()
    cityGraph = readinTowns()
    frontier = queue.Queue()
    visited = []; 
    frontier_dict = dict()
    visited_dict = dict()
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
        for city in cityGraph:
            if ((cityGraph[city].Name == goal_city) and (cityGraph[city].State == goal_state)):
                goal = cityGraph[city].Number
        if (goal == 0):
            print("Invalid city name!")
    st = time.time()   
    frontier.put_nowait(cityGraph[start]);      
    current_state = frontier.get()
    from_where = [cityGraph[start].Name + ", " + cityGraph[start].State ]
    current_path = from_where.pop();
    print()
    # Loop until we reach goal state
    while(current_state.Number != goal):
        # Explore on current level
             
        for kids in current_state.children:
            if not(kids in visited_dict.keys()):
                #print("Enqueue: " + kids)
                if not(kids in frontier_dict.keys()):
                    frontier.put_nowait(cityGraph[kids])
                    frontier_dict[kids] = cityGraph[kids].Name
                    from_where.append(current_path + " -> " + cityGraph[kids].Name + ", " + cityGraph[kids].State )    
        
        visited_dict[current_state.Number] = current_state.Name
        if frontier.qsize == 0:
            print("No possible route")
            return
        
        current_state = frontier.get()
        #print("CurrentState: " + current_state.Name)   
        del frontier_dict[current_state.Number]
        current_path = from_where.pop(0)
        #print("Dequeue: " + current_state.Number)
        
        #print("Current path exploring: " + current_path)
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    
    print()    
    print("Final route = " + current_path)
    
                
if __name__ == "__main__":
    main()