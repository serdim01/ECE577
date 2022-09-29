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
    Berkshire = TreeNode("Berkshire")
    Berkshire.add_child("Hampden", 56)
    Berkshire.add_child("Hampshire", 40)
    Berkshire.add_child("Franklin", 120)
    mapDict["Berkshire"] = Berkshire

    Franklin = TreeNode("Franklin")
    Franklin.add_child("Worcester", 33)
    Franklin.add_child("Berkshire", 120)
    mapDict["Franklin"] = Franklin

    Hampshire = TreeNode("Hampshire")
    Hampshire.add_child("Worcester", 47)
    Hampshire.add_child("Berkshire", 40)
    mapDict["Hampshire"] = Hampshire

    Hampden = TreeNode("Hampden")
    Hampden.add_child("Worcester", 41)
    Hampden.add_child("Berkshire", 56)
    mapDict["Hampden"] = Hampden

    Worcester = TreeNode("Worcester")
    Worcester.add_child("Middlesex", 41)
    Worcester.add_child("Norfolk", 35)
    Worcester.add_child("Hampshire", 47)
    Worcester.add_child("Hampden", 41)
    Worcester.add_child("Franklin", 33)
    mapDict["Worcester"] = Worcester

    Middlesex = TreeNode("Middlesex")
    Middlesex.add_child("Norfolk", 37)
    Middlesex.add_child("Suffolk", 30)
    Middlesex.add_child("Essex", 41)
    Middlesex.add_child("Worcester", 41)
    mapDict["Middlesex"] = Middlesex

    Norfolk = TreeNode("Norfolk")
    Norfolk.add_child("Middlesex", 37)
    Norfolk.add_child("Bristol", 38)
    Norfolk.add_child("Plymouth", 47)
    Norfolk.add_child("Worcester", 35)
    mapDict["Norfolk"] = Norfolk

    Suffolk = TreeNode("Suffolk")
    Suffolk.add_child("Essex", 37)
    Suffolk.add_child("Middlesex", 30)
    mapDict["Suffolk"] = Suffolk

    Essex = TreeNode("Essex")
    Essex.add_child("Suffolk", 37)
    Essex.add_child("Middlesex", 41)
    mapDict["Essex"] = Essex

    Plymouth = TreeNode("Plymouth")
    Plymouth.add_child("Norfolk", 47)
    Plymouth.add_child("Barnstable", 36)
    mapDict["Plymouth"] = Plymouth

    Bristol = TreeNode("Bristol")
    Bristol.add_child("Norfolk", 38)
    mapDict["Bristol"] = Bristol

    Barnstable = TreeNode("Barnstable")
    Barnstable.add_child("Plymouth", 36)
    mapDict["Barnstable"] = Barnstable

    return mapDict

def main():
    mapGraph = createRomaniaTree()
    frontier = queue.Queue()
    visited = [];
    start = "blah"
    while (not (start in mapGraph)):
        print("Enter start city:")
        start = input()
        if not (start in mapGraph):
            print("Invalid city name!")

    goal = "blah"
    while (not (goal in mapGraph)):
        print("Enter destination:")
        goal = input()
        if not (goal in mapGraph):
            print("Invalid city name!")
        if start == goal:
            print("You are already here!")
            return
    frontier.put_nowait(mapGraph[start]);
    current_state = frontier.get()
    from_where = [start]
    current_path = from_where.pop();
    print()
    # Loop until we reach goal state
    while (current_state.Name != goal):
        # Explore on current level
        print("CurrentState: " + current_state.Name)
        for kids in current_state.children:
            if not ((kids) in visited):
                print("Pushing: " + kids)
                frontier.put_nowait(mapGraph[kids])
                from_where.append(current_path + " -> " + kids)

        visited.append(current_state.Name)
        current_state = frontier.get()
        current_path = from_where.pop(0)
        print("Popping: " + current_state.Name)
        print("Current path exploring: " + current_path)
    print()
    print("Final route = " + current_path)


#    # We have reached destination at this point now we traverse up
#    route = []
#    # route back state is string
#    route_back_state = current_state.Name
#    route.append(route_back_state)
#    while (route_back_state != start):
#        for names in visited:
#            if route_back_state in mapGraph[names].children:
#                route_back_state = names
#                route.append(route_back_state)
#                break
#    route.reverse()
#    print()
#    print("Route =", end = " ")
#    for cities in route:
#        if cities == route[-1]:
#            print(cities)
#        else:
#            print(cities + " ->", end=" ")

if __name__ == "__main__":
    main()