# Ege Karabacak #101010870
# COMP 3106 Project Bloxorz with Astar vs UCS

import heapq
# Note that the input below looks like it has been rotated clockwise 90 degrees. It does not affect the overall output.
'''
inputState = (('O', 'O', 'O', 'X', 'X', 'X'),
              ('O', 'S', 'O', 'O', 'X', 'X'),
              ('O', 'O', 'O', 'O', 'X', 'X'),
              ('X', 'O', 'O', 'O', 'X', 'X'),
              ('X', 'O', 'O', 'O', 'X', 'X'),
              ('X', 'O', 'O', 'O', 'O', 'X'),
              ('X', 'X', 'O', 'O', 'O', 'O'),
              ('X', 'X', 'O', 'O', 'G', 'O'),
              ('X', 'X', 'O', 'O', 'O', 'O'),
              ('X', 'X', 'X', 'O', 'O', 'X'))

To run the program with the map from level 3 use this inputState
'''
inputState = (('X', 'O', 'O', 'O', 'O', 'X'), 
               ('X', 'O', 'O', 'S', 'O', 'X'), 
               ('X', 'O', 'O', 'O', 'O', 'X'),
               ('X', 'O', 'O', 'O', 'O', 'X'), 
               ('X', 'X', 'O', 'X', 'X', 'X'), 
               ('X', 'X', 'O', 'X', 'X', 'X'),
               ('O', 'O', 'O', 'X', 'X', 'X'),  
               ('O', 'O', 'O', 'X', 'X', 'X'),  
               ('O', 'O', 'O', 'X', 'X', 'X'),
               ('O', 'X', 'X', 'X', 'X', 'X'),  
               ('O', 'X', 'X', 'X', 'X', 'X'),  
               ('O', 'O', 'O', 'O', 'O', 'X'),
               ('O', 'O', 'O', 'O', 'O', 'O'),  
               ('X', 'X', 'O', 'G', 'O', 'O'),  
               ('X', 'X', 'O', 'O', 'O', 'O'))

# Set the matrix as a tuple of tuples and the empty matrix as a list of lists(left to right and top to bottom)
valid = []  # Record the coordinates of valid actions as a list of lists
goal = []  # Record the coordinates of the goal as a list of lists
inPos = []  # Record the coordinates of the initial position as a list of lists
stepCost = 1    # Step cost is 1 for 'Bloxorz'
m = len(inputState)
n = len(inputState[0])
for column in range(m):       # Record the necessary information to global variables
    for row in range(n):
        if inputState[column][row] != 'X':
            valid.append([column, row])
        if inputState[column][row] == 'G':
            goal.append([column, row])
        elif inputState[column][row] == 'S':
            inPos.append([column, row])
if len(goal) == 1:
    goal.append([])
if len(inPos) == 1:
    inPos.append([])

class Node:
    '''
    the node contains position and generation cost
    '''
    def __init__(self, position1, position2, cost=0):
        self.position1 = position1
        self.position2 = position2
        self.cost = cost

    def __repr__(self):     # required to make Node unambiguous
        return "node at " + str(self.position1) + str(self.position2)

    def __eq__(self, other):    # checks if the nodes are the same
        return (self.position1 == other.get_position1()) and (self.position2 == other.get_position2())

    def __hash__(self):  # for the heap queue
        return hash(self.__repr__())

    def __lt__(self, other):    # determines the greater/less than relationships by utilizing the generation cost
        return self.cost < other.get_cost()

    def __gt__(self, other):
        return self.cost > other.get_cost()

    def __le__(self, other):
        return self.cost <= other.get_cost()

    def __ge__(self, other):
        return self.cost >= other.get_cost()

    def __str__(self):
        return "State position:" + str(self.position1) + str(self.position2) + "\n" + "with cost:" + str(self.cost)

    # Boolean method the check if the given position complies to the constraints
    def is_alive(self):
        return (self.position1 in valid) and ((self.position2 in valid) or (self.position2 == []))

    # Getter methods
    def get_position1(self):
        return self.position1

    def get_position2(self):
        return self.position2

    def get_position(self):
        return [self.position1, self.position2]

    def get_cost(self):
        return self.cost

goalNode = Node(goal[0], goal[1])
initial_node = Node(inPos[0], inPos[1])

def add_edge(node):
    position1 = node.get_position1()
    position2 = node.get_position2()
    successors = []
    cost = node.get_cost() + stepCost
    if position2:  # The state is horizontal
        if position1[0] == position2[0]:  # horizontal with constant x
            temp_node = Node([position1[0] + 1, position1[1]], [position2[0] + 1, position2[1]], cost)
            if temp_node.is_alive():    # can move right
                successors.append(temp_node)
            temp_node = Node([position1[0] - 1, position1[1]], [position2[0] - 1, position2[1]], cost)
            if temp_node.is_alive():    # can move left
                successors.append(temp_node)
            temp_node = Node([position2[0], position2[1] + 1], [], cost)
            if temp_node.is_alive():    # can move up
                successors.append(temp_node)
            temp_node = Node([position1[0], position1[1] - 1], [], cost)
            if temp_node.is_alive():    # can move down
                successors.append(temp_node)
        else:  # horizontal with constant y
            temp_node = Node([position2[0] + 1, position2[1]], [], cost)
            if temp_node.is_alive():
                successors.append(temp_node)
            temp_node = Node([position1[0] - 1, position1[1]], [], cost)
            if temp_node.is_alive():
                successors.append(temp_node)
            temp_node = Node([position1[0], position1[1] + 1], [position2[0], position2[1] + 1], cost)
            if temp_node.is_alive():
                successors.append(temp_node)
            temp_node = Node([position1[0], position1[1] - 1], [position2[0], position2[1] - 1], cost)
            if temp_node.is_alive():
                successors.append(temp_node)
    else:  # The state is vertical
        temp_node = Node([position1[0] + 1, position1[1]], [position1[0] + 2, position1[1]], cost)
        if temp_node.is_alive():
            successors.append(temp_node)
        temp_node = Node([position1[0] - 2, position1[1]], [position1[0] - 1, position1[1]], cost)
        if temp_node.is_alive():
            successors.append(temp_node)
        temp_node = Node([position1[0], position1[1] + 1], [position1[0], position1[1] + 2], cost)
        if temp_node.is_alive():
            successors.append(temp_node)
        temp_node = Node([position1[0], position1[1] - 2], [position1[0], position1[1] - 1], cost)
        if temp_node.is_alive():
            successors.append(temp_node)
    return successors

class Graph:    # Utilize the graph class to store and get the shortest paths required the reach the nodes
    def __init__(self):
        # store the parent child relationships
        self.came_from = {}

    def set_origin(self, child, parent):
        if child in self.came_from.keys():
            if child <= self.came_from[child]:
                self.came_from[child] = parent
        else:
            self.came_from[child] = parent
        return

    def get_origin(self, child):
        # returns the shortest path to the node utilizing the values taken from the ucs function
        origin = []
        temp = child
        while temp != initial_node:
            origin.append(temp)
            temp = self.came_from[temp]
        origin.append(temp)
        return origin
#unifrom cost search function graph is the path and start is our initial node
def ucs(graph, start):
    visited = []
    queue = []
    heapq.heapify(queue)
    heapq.heappush(queue, start)
    memory = 1
    while queue:
        if len(queue) > memory:
            memory = len(queue)
        state = heapq.heappop(queue)

        if state not in visited:
            visited.append(state)

            if state == goalNode:
                path = bloxorz.get_origin(state)
                print("\nGoal reached" + "\n" + "path length: " + str(len(path)))
                print("\nNumber of visited nodes: " + str(len(visited)))
                print("\n" + "Max size of the frontier: " + str(memory))
                print("\nSteps to goal are:")
                for p in path:
                    print(p)

                ''' Uncomment to print the nodes in frontier
                
                print("\nNodes in frontier are:")
                for v in visited:     
                    print(v)
                    '''
                return

            edge = add_edge(state)
            for i in edge:
                if i not in visited:
                    graph.set_origin(i, state)
                    heapq.heappush(queue, i)

bloxorz = Graph()
ucs(bloxorz, initial_node)