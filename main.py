# COMP472 Assignment 2
# Alexander Newman
# 27021747
# Nov 2020

from SearchAlgorithms import Node
from SearchAlgorithms import SearchAlgo
from SearchAlgorithms import Heuristic
from SearchAlgorithms import solvePuzzle

from pathlib import Path

import sys

#targets
targets = [[[1,2,3,4],[5,6,7,0]],[[1,3,5,7],[2,4,6,0]]]


#targets for testing scaling up
#5x2
#targets = [[[1,2,3,4,5],[6,7,8,9,0]], [[1,3,5,7,9],[2,4,6,8,0]]]
#4x3
#targets = [[[1,2,3,4],[5,6,7,8],[9,10,11,0]],[[1,4,7,10],[2,5,8,11],[3,6,9,0]]]

def main():
  #check command line arguments
  if(len(sys.argv) != 2):
    print("Usage: main.py <inputFile>")
    return
  
  
  inputPuzzles = readPuzzleFile(sys.argv[1])
  
  #Uniform cost search
  print("UCS")
  print("====================")
  runPuzzles(inputPuzzles, SearchAlgo.UCS, None, "ucs")
  
  #Greedy best first search
  print("GBFS, Hamming")
  print("====================")
  runPuzzles(inputPuzzles, SearchAlgo.GBFS, Heuristic.Hamming, "gbfs-h1")
  print("GBFS, Manhattan")
  print("====================")
  runPuzzles(inputPuzzles, SearchAlgo.GBFS, Heuristic.Manhattan, "gbfs-h2")
  
  #A* search
  print("ASTAR, Hamming")
  print("====================")
  runPuzzles(inputPuzzles, SearchAlgo.ASTAR, Heuristic.Hamming, "astar-h1")
  print("ASTAR, Manhattan")
  print("====================")
  runPuzzles(inputPuzzles, SearchAlgo.ASTAR, Heuristic.Manhattan, "astar-h2")
  
  #Scaling up tests
  '''
  inputPuzzles = readPuzzleFile5x2(sys.argv[1])
  print("ASTAR, Manhattan 5x2")
  print("====================")
  runPuzzles(inputPuzzles, SearchAlgo.ASTAR, Heuristic.Manhattan, "astar-h2-5x2")
  
  inputPuzzles = readPuzzleFile4x3(sys.argv[1])
  print("ASTAR, Manhattan 4x3")
  print("====================")
  runPuzzles(inputPuzzles, SearchAlgo.ASTAR, Heuristic.Manhattan, "astar-h2-4x3")
  '''

def readPuzzleFile(fileName):
  puzzles = []
  
  with open(fileName) as f:
    for line in f:
      puzzle = line.split()
      for i in range(0, len(puzzle)):
        puzzle[i] = int(puzzle[i])
      puzzles.append([puzzle[:4], puzzle[4:]])
      
  return puzzles

def readPuzzleFile5x2(fileName):
  puzzles = []
  
  with open(fileName) as f:
    for line in f:
      puzzle = line.split()
      for i in range(0, len(puzzle)):
        puzzle[i] = int(puzzle[i])
      puzzles.append([puzzle[:5], puzzle[5:]])
      
  return puzzles
  
def readPuzzleFile4x3(fileName):
  puzzles = []
  
  with open(fileName) as f:
    for line in f:
      puzzle = line.split()
      for i in range(0, len(puzzle)):
        puzzle[i] = int(puzzle[i])
      puzzles.append([puzzle[:4], puzzle[4:8], puzzle[8:]])
      
  return puzzles

def runPuzzles(puzzles, searchAlgo, heuristic, outputFilePrefix):
  i = 0
  
  for puzzle in puzzles:
    print("Solving puzzle " + str(i) + " " + str(puzzle), end="")
    sys.stdout.flush() #required to display previous print...weird!
    startNode = Node(puzzle, 0, 0, searchAlgo, 0, 0)
    goalNode, searchTrace, duration = solvePuzzle(startNode, targets, heuristic, searchAlgo)
    if goalNode is None:
      print(" | no solution")
    else:
      print(" | " + str(duration))
    writePuzzleOutput(goalNode, searchTrace, duration, str(i) + "_" + outputFilePrefix)
    i+= 1

def writePuzzleOutput(goalNode, trace, duration, puzzleName):
  #ensure "output" directory exists
  Path("output").mkdir(parents=True, exist_ok=True)
  
  solutionFile = "output/" + puzzleName + "_solution.txt"
  searchFile = "output/" + puzzleName + "_search.txt"
  
  #build & write solution string
  solutionStr = ""
  if goalNode is None:
    solutionStr = "no solution"
  else:
    #reverse order of nodes
    solutionPath = []
    solutionPath.insert(0, goalNode)
    parentNode = goalNode.parentNode
    while parentNode is not None:
      solutionPath.insert(0, parentNode)
      parentNode = parentNode.parentNode
      
    for node in solutionPath:
      solutionStr += str(node.prevMoved) + " " + str(node.moveCost) + " " + str(node) + "\n"
      
    solutionStr += str(goalNode.gVal) + " " + str(duration)
  
  with open(solutionFile, "w") as f:
    f.write(solutionStr)
    
  #write search
  with open(searchFile, "w") as f:
    f.write(trace)
    
if __name__ == '__main__':
  main()