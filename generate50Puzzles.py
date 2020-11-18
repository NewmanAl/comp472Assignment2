# COMP472 Assignment 2
# Alexander Newman
# 27021747
# Nov 2020

from numpy.random import permutation

outputFileName = "testPuzzles.txt"
#outputFileName = "testPuzzles5x2.txt"
#outputFileName = "testPuzzles4x3.txt"

def main():
  i = 0
  outputStr = ""
  
  while i < 50:
    puzzle = permutation(8)
    #puzzle = permutation(10)
    #puzzle = permutation(12)
    outputStr += str(puzzle)[1:-1] + "\n"
    
    i+=1
    
  with open(outputFileName, "w") as f:
    f.write(outputStr[:-1])
    
if __name__ == '__main__':
  main()