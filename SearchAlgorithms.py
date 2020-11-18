# COMP472 Assignment 2
# Alexander Newman
# 27021747
# Nov 2020

import copy
import time
from enum import Enum

#Class & Enum definitions
class SearchAlgo(Enum):
  UCS = 1
  GBFS = 2
  ASTAR = 3
  
class Heuristic(Enum):
  Hamming = 1
  Manhattan = 2
  Demo = 3
  
class Node:
  def __init__(self, puzzleState, hVal, gVal, searchAlgo, prevMoved, moveCost, parentNode=None):
    self.puzzleState = puzzleState
    self.hVal = hVal
    self.gVal = gVal
    self.searchAlgo = searchAlgo
    self.prevMoved = prevMoved
    self.moveCost = moveCost
    self.parentNode = parentNode
    
  def fVal(self):
    if self.searchAlgo == SearchAlgo.UCS:
      return self.gVal
    elif self.searchAlgo == SearchAlgo.GBFS:
      return self.hVal
    else: #ASTAR
      return self.hVal + self.gVal;
    
  def __lt__(self, other):
    return self.fVal() < other.fVal()
    
  def __eq__(self, other):
    return self.puzzleState == other.puzzleState
    
  def __str__(self):
    retStr = ""
    for y in self.puzzleState:
      for x in y:
        retStr += str(x) + " "
        
    return retStr[:-1]
    
#Heuristic functions
def hammingDistance(target, current):
  missplaced = 0
  for y in range(len(target)):
    for x in range(len(target[0])):
      if(target[y][x] != current[y][x]):
        missplaced += 1
        
  return missplaced
  
def manhattanDistance(target, current):
  distance = 0
  for y in range(len(target)):
    for x in range(len(target[0])):
      if target[y][x] != current[y][x] and target[y][x] != 0:
        
        #find x y of value in current
        currentX, currentY = 0, 0
        for i in range(len(current)):
          if current[i].count(target[y][x]) == 1:
            currentX = current[i].index(target[y][x])
            currentY = i
            break;
            
        distance += abs(x - currentX) + abs(y - currentY)
  
  return distance
  
def demoHeuristic(current):
  if(current[len(current)-1][len(current[0])-1] == 0):
    return 0
    
  return 1
  
def calculateHeuristic(type, targets, current):
  if(type == None):
    return 0
  elif(type == Heuristic.Demo):
    return demoHeuristic(current)
  else:
    heuristics = []
    for t in targets:
      if(type == Heuristic.Hamming):
        heuristics.append(hammingDistance(t, current))
      elif (type == Heuristic.Manhattan):
        heuristics.append(manhattanDistance(t, current))
    heuristics.sort()
    return heuristics[0]
    
#X-puzzle specific

# Returns a list of children Nodes
#  parentNode - Node to generate children from
#  targets    - List of goal Nodes used for heuristic calculation
#  heuristic  - Heuristic used for searchAlgo
#  searchAlgo - Search algorithm being used
def generateChildren(parentNode, targets, heuristic, searchAlgo):
  children = []
  
  #setup
  xWidth = len(parentNode.puzzleState[0]) - 1
  yWidth = len(parentNode.puzzleState) - 1
  
  targetX, targetY = 0,0 # location of the 0 in our puzzle
  i = 0
  for y in parentNode.puzzleState:
    if y.count(0) == 1:
      targetX = y.index(0)
      targetY = i
      break
    i += 1
    
  regularCost = 1
  wrapCost = 2
  diagCost = 3
    
  #regular moves (up,down,left,right)
  #up
  if(targetY > 0):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY-1][targetX] = newState[targetY-1][targetX], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+regularCost, searchAlgo, newState[targetY][targetX], regularCost, parentNode))
    
  #down
  if(targetY < yWidth):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY+1][targetX] = newState[targetY+1][targetX], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+regularCost, searchAlgo, newState[targetY][targetX], regularCost, parentNode))
    
  #left
  if(targetX > 0):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY][targetX-1] = newState[targetY][targetX-1], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+regularCost, searchAlgo, newState[targetY][targetX], regularCost, parentNode))
    
  #right
  if(targetX < xWidth):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY][targetX+1] = newState[targetY][targetX+1], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+regularCost, searchAlgo, newState[targetY][targetX], regularCost, parentNode))
    
  #row wrap moves
  #left to right
  if(targetX == 0):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY][xWidth] = newState[targetY][xWidth], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+wrapCost, searchAlgo, newState[targetY][targetX], wrapCost, parentNode))
    
  #right to left
  if(targetX == xWidth):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY][0], = newState[targetY][0], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+wrapCost, searchAlgo, newState[targetY][targetX], wrapCost, parentNode))
    
  #column wrap moves (Uncomment for  sect 2.5 scaling up)
  '''
  #top to bottom
  if(targetY == 0):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[yWidth][targetX] = newState[yWidth][targetX], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+wrapCost, searchAlgo, newState[targetY][targetX], wrapCost, parentNode))
    
  #bottom to top
  if(targetY == yWidth):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[0][targetX] = newState[0][targetX], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+wrapCost, searchAlgo, newState[targetY][targetX], wrapCost, parentNode))
  '''
  #diagonal moves
  #top left
  if(targetX == 0 and targetY == 0):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY+1][targetX+1] = newState[targetY+1][targetX+1], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
    
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[yWidth][xWidth] = newState[yWidth][xWidth], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
    
  #bottom left
  if(targetX == 0 and targetY == yWidth):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY-1][targetX+1] = newState[targetY-1][targetX+1], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
    
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[0][xWidth] = newState[0][xWidth], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
    
  #top right
  if(targetX == xWidth and targetY == 0):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY+1][targetX-1] = newState[targetY+1][targetX-1], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
    
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[yWidth][0] = newState[yWidth][0], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
  
  #bottom right
  if(targetX == xWidth and targetY == yWidth):
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[targetY-1][targetX-1] = newState[targetY-1][targetX-1], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
    
    newState = copy.deepcopy(parentNode.puzzleState)
    newState[targetY][targetX], newState[0][0] = newState[0][0], newState[targetY][targetX]
    h = calculateHeuristic(heuristic, targets, newState)
    children.append(Node(newState, h, parentNode.gVal+diagCost, searchAlgo, newState[targetY][targetX], diagCost, parentNode))
    
  return children

# Solves the x-puzzle.
# Returns the goal Node, a string representing the search trace, and the duration
# Goal node is None when no solution is found
#   initialNode   - Puzzle start Node
#   targets       - List of goal Nodes for puzzle
#   heuristicType - Heuristic used for search
#   searchAlgo    - Search algorithm used for puzzle
def solvePuzzle(initialNode, targets, heuristicType, searchAlgo):
  openList = []
  closedList = []
  searchTrace = ""
  
  openList.append(initialNode)
  currentNode = None
  
  startTime = time.time()
  
  #NOTE - remove time restriction when running scaled-up puzzles
  while len(openList) != 0 and (time.time() - startTime) < 60:
    
    currentNode = openList.pop(0)
    closedList.append(currentNode)
    
    
    #append to search trace string
    if searchAlgo == SearchAlgo.UCS:
      searchTrace += "0 " + str(currentNode.gVal) + " 0 " + str(currentNode) + "\n"
    elif searchAlgo == SearchAlgo.GBFS:
      searchTrace += "0 0 " + str(currentNode.hVal) + " " + str(currentNode) + "\n"
    else:
      searchTrace += str(currentNode.fVal()) + " " + str(currentNode.gVal) + " " + str(currentNode.hVal) + " " + str(currentNode) + "\n"
    
    if currentNode.puzzleState in targets:
      #GOOOOAAAALLLLLLLLLLLL 8D
      break
    
    children = generateChildren(currentNode, targets, heuristicType, searchAlgo)
    for child in children:
      #check closed list
      if closedList.count(child) != 0:
        if searchAlgo == SearchAlgo.ASTAR:
          #pop node from closed to open if node found with lower fVal
          if(closedList[closedList.index(child)].fVal() > child.fVal()):
            closedList.remove(child)
            openList.append(child)
          
      #check open list
      elif openList.count(child) != 0:
        if searchAlgo != SearchAlgo.GBFS:
          #update node from open if node found with lower fVal
          if openList[openList.index(child)].fVal() > child.fVal():
            openList.remove(child)
            openList.append(child)
            
      else:
        openList.append(child)
        
    openList.sort()
    
  stopTime = time.time()
    
  if currentNode.puzzleState in targets:
    #goal was found
    return currentNode, searchTrace[:-1], (stopTime - startTime)
  else:
    return None, searchTrace[:-1], (stopTime - startTime)