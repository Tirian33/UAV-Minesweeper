from Minefield import * 
from Solver import *


#main
rows = 9
cols = 9
mines = 9

mineField = Minefield(rows,cols,mines)

print(mineField.stringUAV())
print(mineField.stringMines())
# print("\n\n\n")

print(genetic_algorithm(popSize=11, generations=1000, mutationRate=0.15, toSolve=mineField.getUAVInfo(), numMines=9))