from Minefield import * 
from Solver import *

def compareSolution(solution, GAattempt):
    """Makes pretty output for comparison"""
    #Color codes
    g = "\033[92m"
    r = "\033[91m"
    w = "\033[0m"

    outString = ""
    lastBit = ""
    #Since no compuition/change using zip for double iteration
    for r1, r2 in zip(solution, GAattempt):
        r1Str = ""
        r2Str = ""
        for v1, v2 in zip(r1, r2):
            r1Str += f"{v1} "
            r2Str += f"{v2} "

            #Color version
            if v1 == v2:
                lastBit += f"{g}{v1}{w} "
            else:
                lastBit += f"{r}{v2}{w} "
        #spacing
        outString += r1Str + "\t" + r2Str
        outString = outString[:-1] + "\n"
        lastBit = lastBit[:-1] + "\n"

    outString = outString + "\n" + lastBit
    return outString

def main():
    rows = 4
    cols = 4
    mines = 4

    # mineField = Minefield(rows,cols,mines)

    # print(mineField.stringUAV())
    # print(mineField.stringMines())
    # print("\n\n\n")

    example1 = [[0,1,1,1], [1,2,2,2], [1,2,3,3],[1,1,2,2], [0,0,1,1]]
    minesAt = [[0,0,0,1], [0,0,1,0], [1,0,0,1], [0,0,0,1], [0,0,0,0]]

    res = genetic_algorithm(popSize=11, generations=10000, mutationRate=0.1, toSolve=example1, numMines=mines)

    print(compareSolution(minesAt, res))

if __name__ == '__main__':
    main()