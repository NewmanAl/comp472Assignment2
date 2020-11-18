https://github.com/NewmanAl/comp472Assignment2

main.py is the main entry point for this assignment. It can be executed as follows
```
python main.py <inputFile>
```
The contents of the provided input file is expected to be formatted similarly to the provided samples.txt of the assignment

main.py will run through each puzzle contained within the provided input file, and will generate the desired output in the directory 'output/', relative to the location that the program was executed from. If the 'output/' directory does not initially exist, then it is created during execution.

SearchAlgorithms.py contains the meat of this assignment, and is utilised by main.py. This file contains the functions and classes used to perform the search algorithms and solve the x-puzzle.

generate50Puzzles.py is a utility script used to generate the input files used for this assignment. As the name implies, it generates a text file that contains 50 puzzles. The generated file is named "testPuzzles.txt". It is simply executed as
```
python generate50Puzzles.py
```

analyseOutput.py is another utility script which is used to generate the diagrams used as part of this assignment's presentation. The script assumes that execution of main.py has already occured, and that the resulting output already exists under the directory 'output/'. The diagrams created in this script are saved in the directory 'diagrams/', relative to the location that the script was executed from. If the 'diagrams/' directory does not initially exist, then it is created during execution.
The script is simply executed as
```
python analyseOutput.py
```