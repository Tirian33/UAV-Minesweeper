from Minefield import * 
from Solver import *
from math import floor as fl

def compareSolution(solution, GAattempt):
    """Makes pretty output for comparison"""
    #Color codes
    g = "\033[92m"
    r = "\033[91m"
    w = "\033[0m"
    fp = 0
    fn = 0
    cells = 0

    outString = ""
    lastBit = ""
    #Since no compuition/change using zip for double iteration
    for r1, r2 in zip(solution, GAattempt):
        r1Str = ""
        r2Str = ""
        for v1, v2 in zip(r1, r2):
            cells +=1

            r1Str += f"{v1}{w} " if v1 == 0 else f"{r}{v1}{w} "
            r2Str += f"{v2}{w} " if v2 == 0 else f"{r}{v2}{w} "

            #Color version
            if v1 == v2:
                lastBit += f"{g}{v1}{w} "
            else:
                lastBit += f"{r}{v2}{w} "
                if v2 == 0:
                    fn +=1
                else:
                    fp += 1
        #spacing
        outString += r1Str + "\t" + r2Str
        outString = outString[:-1] + "\n"
        lastBit = lastBit[:-1] + "\n"

    print(outString + "\n" + lastBit)
    print(f"That yields:\nAccuracy: {(cells - fp -fn)} / {cells} {(cells - fp -fn)/cells :.4f}\nFP: {fp}\tFN: {fn}")
    return fp + fn == 0

def main():
    rows = 10
    cols = 15
    mines = fl(rows * cols * .20)

    mineField = Minefield(rows,cols,mines)

    print(mineField.stringUAV())
    print(mineField.stringMines())
    print("\n\n\n")

    # example1 = [[0,1,1,1], [1,2,2,2], [1,2,3,3],[1,1,2,2], [0,0,1,1]]
    # minesAt = [[0,0,0,1], [0,0,1,0], [1,0,0,1], [0,0,0,1], [0,0,0,0]]

    res = genetic_algorithm(popSize=100, generations=10**4, mutationRate=0.075, toSolve=mineField.getUAVInfo(), numMines=mines)

    _ = compareSolution(mineField.getActualField(), res)

if __name__ == '__main__':
    main()