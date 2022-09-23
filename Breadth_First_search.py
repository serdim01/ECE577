# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 14:12:49 2022

@author: CJ
"""
# https://stackoverflow.com/questions/2482602/a-general-tree-implementation
import queue
       
class TreeNode(object):
    def __init__(self, name):
        self.Name = name
        self.children = dict()

    def add_child(self, name, cost):
        self.children[name] = cost


        
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
    mapGraph = createRomaniaTree()
    frontier = queue.Queue()
    visited = [];    
    start = "blah"
    while (not(start in mapGraph)):
        print("Enter start city:" )
        start = input()
        if not(start in mapGraph):
            print("Invalid city name!")
    
    goal = "blah"
    while (not(goal in mapGraph)):
        print("Enter destination:" ) 
        goal = input()        
        if not(goal in mapGraph):
            print("Invalid city name!")
        if start == goal:
            print("You are already here!")
            return
    frontier.put_nowait(mapGraph[start]);      
    current_state = frontier.get()
    print()
    # Loop until we reach goal state
    while(current_state.Name != goal):
        # Explore on current level
        print("CurrentState: " + current_state.Name)        
        for kids in current_state.children:
            if not((kids) in visited):
                print("Pushing: " + kids)
                frontier.put_nowait(mapGraph[kids])
                    
        
        visited.append(current_state.Name)
        current_state = frontier.get()
        print("Popping: " + current_state.Name)
    # We have reached destination at this point now we traverse up 
    route = []
    # route back state is string
    route_back_state = current_state.Name
    route.append(route_back_state)
    while (route_back_state != start):
        for names in visited:
            if route_back_state in mapGraph[names].children:
                route_back_state = names
                route.append(route_back_state)
                break
    route.reverse()
    print()
    print("Route =", end = " ")
    for cities in route:
        if cities == route[-1]:
            print(cities)
        else:
            print(cities + " ->", end=" ")        
                
if __name__ == "__main__":
    main()