# COMP472 Assignment 2
# Alexander Newman
# 27021747
# Nov 2020

import glob
import matplotlib.pyplot as plt
from pathlib import Path

def main():
  
  #calculate data from output files
  data = {}
  data["ucs"] = calculateMetrics("ucs")
  data["gbfs-h1"] = calculateMetrics("gbfs-h1")
  data["gbfs-h2"] = calculateMetrics("gbfs-h2")
  data["astar-h1"] = calculateMetrics("astar-h1")
  data["astar-h2"] = calculateMetrics("astar-h2")
  
  #Scaling up analysis
  #data["astar-h2-5x2"] = calculateMetrics("astar-h2-5x2")
  #data["astar-h2-4x3"] = calculateMetrics("astar-h2-4x3")
  
  #generate diagrams from data
  generateDiagrams(data)
  
def calculateMetrics(filePrefix):
  #solution metrics
  numPuzzles = 0
  avgSolutionLength = 0
  numNoSolution = 0
  avgSolutionCost = 0
  totalExecutionTime = 0
  avgExecutionTime = 0
  minExecutionTime = 999999
  maxExecutionTime = 0
  
  solutionFiles = glob.glob("output/*_" + filePrefix + "_solution.txt")
  numPuzzles = len(solutionFiles)
  for solutionFile in solutionFiles:
    with open(solutionFile, "r") as f:
      lines = f.read().splitlines()
      if len(lines) == 1:
        #can safely assume this is "no solution"
        numNoSolution += 1
        totalExecutionTime += 60
      else:
        avgSolutionLength += len(lines) - 2
        avgSolutionCost += int(lines[-1].split()[0])
        execTime = float(lines[-1].split()[1])
        totalExecutionTime += execTime
        
        if execTime < minExecutionTime:
          minExecutionTime = execTime
        if maxExecutionTime < execTime:
          maxExecutionTime = execTime
        
  avgSolutionLength /= (numPuzzles - numNoSolution)
  avgSolutionCost /= (numPuzzles - numNoSolution)
  avgExecutionTime = totalExecutionTime / numPuzzles
  
  #search metrics
  avgSearchLength = 0
  searchFiles = glob.glob("output/*_" + filePrefix + "_search.txt")
  for searchFile in searchFiles:
    with open(searchFile, "r") as f:
      avgSearchLength += len(f.read().splitlines())
      
  avgSearchLength /= (numPuzzles - numNoSolution)
  
  returnDict = {
    "avgSolutionLength" : avgSolutionLength,
    "avgSolutionCost" : avgSolutionCost,
    "numNoSolution" : numNoSolution,
    "totalExecutionTime" : totalExecutionTime,
    "avgExecutionTime" : avgExecutionTime,
    "avgSearchLength" : avgSearchLength,
    "minExecutionTime" : minExecutionTime,
    "maxExecutionTime" : maxExecutionTime
  }
  
  return returnDict
  
def generateDiagrams(data):
  #ensure "diagrams" directory exists
  Path("diagrams").mkdir(parents=True, exist_ok=True)
  
  labels = ["ucs", "gbfs-h1", "gbfs-h2", "astar-h1", "astar-h2"]
  
  #average solution length
  chartData = [data["ucs"]["avgSolutionLength"], \
               data["gbfs-h1"]["avgSolutionLength"], \
               data["gbfs-h2"]["avgSolutionLength"], \
               data["astar-h1"]["avgSolutionLength"], \
               data["astar-h2"]["avgSolutionLength"]]
  plt.bar(labels, chartData)
  plt.title("Average Solution Length")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, '{0:.4f}'.format(value), horizontalalignment='center')
  #plt.show()
  plt.savefig("diagrams/avgSolutionLength.png")
  plt.close()
  
  #average solution cost
  chartData = [data["ucs"]["avgSolutionCost"], \
               data["gbfs-h1"]["avgSolutionCost"], \
               data["gbfs-h2"]["avgSolutionCost"], \
               data["astar-h1"]["avgSolutionCost"], \
               data["astar-h2"]["avgSolutionCost"]]
  plt.bar(labels, chartData)
  plt.title("Average Solution Cost")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, '{0:.4f}'.format(value), horizontalalignment='center')
  #plt.show()
  plt.savefig("diagrams/avgSolutionCost.png")
  plt.close()
  
  #no solutions
  chartData = [data["ucs"]["numNoSolution"], \
               data["gbfs-h1"]["numNoSolution"], \
               data["gbfs-h2"]["numNoSolution"], \
               data["astar-h1"]["numNoSolution"], \
               data["astar-h2"]["numNoSolution"]]
  plt.bar(labels, chartData)
  plt.title("Number of \"no solution\"")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, str(value), horizontalalignment='center')
  #plt.show()
  plt.savefig("diagrams/noSolutions.png")
  plt.close()
  
  #average execution time
  chartData = [data["ucs"]["avgExecutionTime"], \
               data["gbfs-h1"]["avgExecutionTime"], \
               data["gbfs-h2"]["avgExecutionTime"], \
               data["astar-h1"]["avgExecutionTime"], \
               data["astar-h2"]["avgExecutionTime"]]
               
  plt.bar(labels, chartData)
  plt.title("Average Execution Time")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, '{0:.4f}'.format(value), horizontalalignment='center')
  plt.ylabel("seconds")
  #plt.show()
  plt.savefig("diagrams/avgExecutionTime.png")
  plt.close()
  
  #total execution time
  chartData = [data["ucs"]["totalExecutionTime"], \
               data["gbfs-h1"]["totalExecutionTime"], \
               data["gbfs-h2"]["totalExecutionTime"], \
               data["astar-h1"]["totalExecutionTime"], \
               data["astar-h2"]["totalExecutionTime"]]
               
  plt.bar(labels, chartData)
  plt.title("Total Execution Time")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, '{0:.4f}'.format(value), horizontalalignment='center')
  #plt.show()
  plt.ylabel("seconds")
  plt.savefig("diagrams/totalExecutionTime.png")
  plt.close()
  
  #Average search length
  chartData = [data["ucs"]["avgSearchLength"], \
               data["gbfs-h1"]["avgSearchLength"], \
               data["gbfs-h2"]["avgSearchLength"], \
               data["astar-h1"]["avgSearchLength"], \
               data["astar-h2"]["avgSearchLength"]]
               
  plt.bar(labels, chartData)
  plt.title("Average Search Length")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, '{0:.4f}'.format(value), horizontalalignment='center')
  #plt.show()
  plt.savefig("diagrams/avgSearchLength.png")
  plt.close()
  
  #Section 2.5 - scaling up
  '''
  #average execution time
  labels = ["4x2", "5x2", "4x3"]
  chartData = [data["astar-h2"]["avgExecutionTime"], \
               data["astar-h2-5x2"]["avgExecutionTime"], \
               data["astar-h2-4x3"]["avgExecutionTime"]]
               
  plt.bar(labels, chartData)
  plt.title("Average Execution Time\nA* Manhattan Distance")
  plt.ylabel("seconds")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, '{0:.4f}'.format(value), horizontalalignment='center')
  #plt.show()
  plt.savefig("diagrams/scaleUpAvgExec.png")
  plt.close()
  
  #total execution time
  chartData = [data["astar-h2"]["totalExecutionTime"], \
               data["astar-h2-5x2"]["totalExecutionTime"], \
               data["astar-h2-4x3"]["totalExecutionTime"]]
               
  plt.bar(labels, chartData)
  plt.title("Total Execution Time\nA* Manhattan Distance")
  plt.ylabel("seconds")
  for index, value in enumerate(chartData):
    plt.text(index, value + 0.003, '{0:.4f}'.format(value), horizontalalignment='center')
  #plt.show()
  plt.savefig("diagrams/scaleUpTotalExec.png")
  plt.close()
  
  #comparison of min/max execution time
  import numpy as np
  minData = [data["astar-h2"]["minExecutionTime"], \
               data["astar-h2-5x2"]["minExecutionTime"], \
               data["astar-h2-4x3"]["minExecutionTime"]]
               
  maxData = [data["astar-h2"]["maxExecutionTime"], \
               data["astar-h2-5x2"]["maxExecutionTime"], \
               data["astar-h2-4x3"]["maxExecutionTime"]]
               
  x = np.arange(len(labels))
  width = 0.35
  
  fig, ax = plt.subplots()
  rects1 = ax.bar(x - width/2, minData, width, label="Min")
  rects2 = ax.bar(x + width/2, maxData, width, label="Max")
  
  ax.set_ylabel("seconds")
  ax.set_title("Min vs Max Execution Time\nA* Manhattan Distance")
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.legend()
  
  for i in range(len(labels)):
    plt.text(i - width/2, minData[i]+0.003, '{0:.4f}'.format(minData[i]), horizontalalignment='center')
    plt.text(i + width/2, maxData[i]+0.003, '{0:.4f}'.format(maxData[i]), horizontalalignment='center')
  
  fig.tight_layout()
  #plt.show()
  plt.savefig("diagrams/scaleUpMinMax.png")
  plt.close()
  '''
  
if __name__ == '__main__':
  main()