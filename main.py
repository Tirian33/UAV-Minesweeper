from Minefield import Minefield #Minefield abstraction
from Individual import Individual #Population member
import sys #Commandline args
import signal #For ctrl + C handling
import random #randomness

def abortRun(signal, stackFrame):
    #Ctrl + C handling
    print("\n\nCtrl+C recived. Terminating...")
    sys.exit(0)

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

def genetic_algorithm(popSize = 10, generations = 100, mutationRate = 0.1, toSolve = [[1]], numMines = 1):
    #setup the Individual class properties
    Individual.boardToSolve = toSolve
    Individual.startingMines = numMines
    mutRate = mutationRate
    mutRampCD = 0
    
    #Create initial population
    pop = [Individual() for _ in range(popSize)]
    lastImprovement = [0, 0]

    #Begin the generations
    for gen in range(generations):
        #Sort by fitness value
        pop.sort(key=lambda indiv: indiv.fitness, reverse=True)
        
        #Are we done?
        if pop[0].fitness == len(toSolve) * len(toSolve[0]):
            print(f"\nExiting early! Generation {gen} was a perfect solution!")
            return pop[0].chromTo2D()
        
        if pop[0].fitness > lastImprovement[0]:
            lastImprovement[0] = pop[0].fitness
            lastImprovement[1] = 0
            mutRampCD = 0
            mutRate = mutationRate
        else:
            lastImprovement[1] += 1

            #Ramp up mutation rate if we don't get progress; 4% of generations
            if lastImprovement[1] >= 0.04 * generations:
                if mutRampCD == 0:
                    mutRate = mutRate * 1.5
                    if mutRate > 1:
                        mutRate = 1
                    #Wait for 1% of generations before intensifying
                    mutRampCD = 0.01 * generations
                else:
                    mutRampCD -= 1
            


        #Exit - local maxima
        if lastImprovement[1] > generations * 0.25:
            print(f"\nExiting early! No improvement after 1/4 of maximum generations. Local Maxima?")
            return pop[0].chromTo2D()
        
        fancyPrint(f"Processing... Generation {gen} | Since last improvement {lastImprovement[1]} | Score {lastImprovement[0]} | MR {mutRate * 100 :.2f}%")
        #Let the best 50% mate
        parents = pop[: popSize//2]

        #The parents go into next generation to reduce slideback
        nextGeneration = parents[:]

        #Mate each of the parents with a random entity (can mate with self)
        for i in range(len(parents)):
            p1 = parents[i]
            p2 = random.choice(parents)
            child = p1.mate(p2)
            nextGeneration.append(child)
        
        #Mutations
        for indiv in nextGeneration:
            if random.random() < mutRate:
                a = indiv.mutate()
                if not a:
                    return indiv.chromTo2D()
        
        pop = nextGeneration
    
    print(f"No exact solution found after {generations} generations.")
    pop.sort(key=lambda indiv: indiv.fitness, reverse=True)
    return pop[0].chromTo2D()

def fancyPrint(fString) -> None:
    sys.stdout.write("\r" + fString)
    sys.stdout.flush()

def main():
    rows = 1
    cols = 1
    mines = 1
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == "easy":
            rows, cols, mines = (9,9,10)
        elif sys.argv[1].lower() == "med":
            rows, cols, mines = (16,16,40)
        elif sys.argv[1].lower() == "hard":
            rows, cols, mines = (16,30,99)
        else:
            print("Usage: py script.py <rows> <cols> <mines> OR py script.py <Easy/Med/Hard>")
    elif len(sys.argv) >= 4:
        try:
            rows, cols, mines = (int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
        except ValueError:
            print("Usage Error: Expected Integers")
    else:
        print("Usage: py script.py <rows> <cols> <mines> OR py script.py <Easy/Med/Hard>")
        sys.exit(1)

    #CTRL + C handler
    signal.signal(signal.SIGINT, abortRun)

    mineField = Minefield(rows,cols,mines)

    print(mineField.stringUAV())
    print(mineField.stringMines())
    print("\n\n\n")

    res = genetic_algorithm(popSize=100, generations=10**4, mutationRate=0.075, toSolve=mineField.getUAVInfo(), numMines=mines)

    _ = compareSolution(mineField.getActualField(), res)

if __name__ == '__main__':
    main()