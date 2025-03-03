import random

def genetic_algorithm(popSize = 10, generations = 100, mutationRate = 0.1, toSolve = [[1]], numMines = 1):
    #setup the Individual class properties
    Individual.boardToSolve = toSolve
    Individual.startingMines = numMines
    
    #Create initial population
    pop = [Individual() for _ in range(popSize)]
    lastImprovement = [0, 0]

    #Begin the generations
    for gen in range(generations):
        #Sort by fitness value
        pop.sort(key=lambda indiv: indiv.fitness, reverse=True)
        
        #Are we done?
        if pop[0].fitness == len(toSolve) * len(toSolve[0]):
            print(f"Exiting early! Generation {gen} was a perfect solution!")
            return pop[0].chromTo2D()
        
        if pop[0].fitness > lastImprovement[0]:
            print(f"New score of {pop[0].fitness}. It took {lastImprovement[1]} generations.")
            lastImprovement[0] = pop[0].fitness
            lastImprovement[1] = 0
        else:
            lastImprovement[1] += 1


        #Exit - local maxima
        if lastImprovement[1] > generations * 0.25:
            print(f"Exiting early! No improvement after 1/4 of maximum generations. Local Maxima?")
            return pop[0].chromTo2D()
        
        #print(f"Generation {gen} best value is {pop[0].fitness}.")
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
            if random.random() < mutationRate:
                indiv.mutate()
        
        pop = nextGeneration
    
    print(f"No exact solution found after {generations} generations.")
    pop.sort(key=lambda indiv: indiv.fitness, reverse=True)
    return pop[0].chromTo2D()




class Individual:
    """Represents a member of the population"""

    effectedCells = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0,0), (0,1), (1, -1), (1, 0), (1, 1)]
    boardToSolve = [[1]]
    startingMines = 1

    def __init__(self, genValues=True):

        if genValues:
            self.chromosome = self.createIndividual()
            self.fitness = self.calcFitness()
        else:
            self.chromosome = None
            self.fitness = None
    
    def createIndividual(self) -> set[tuple[int,int]]:
        """Creates a guess at what the minefield might be"""
        mockField = [(r, c) for r in range(len(self.boardToSolve)) for c in range(len(self.boardToSolve[0]))]
        selected = random.sample(mockField, self.startingMines)
        return set(selected)
    
    def calcFitness(self) -> int:
        testField = [[0 for _ in range(len(self.boardToSolve[0]))] for _ in range(len(self.boardToSolve))]
        problems = [[0 for _ in range(len(self.boardToSolve[0]))] for _ in range(len(self.boardToSolve))]
        score = 0
        mines = list(self.chromosome)

        #Place the mines on testField
        for x, y in mines:
            for dx, dy in self.effectedCells:
                updateX = x + dx
                updateY = y + dy
                if 0 <= updateX < len(self.boardToSolve) and 0 <= updateY < len(self.boardToSolve[0]):
                    testField[updateX][updateY] += 1
        
        for r in range(len(testField)):
            for c in range(len(testField[0])):
                if testField[r][c] == self.boardToSolve[r][c]:
                    score += 1
                else:
                    problems[r][c] = 1
                    #print(f"problem at ({r}, {c})")
        
        #print(f"Score: {score}  Guess: \n{self.readable(testField)} Problem Matrix: \n{self.readable(problems)}")
        return score
    
    def mate(self, other: "Individual") -> "Individual":
        """Mate two parents to make a child instance. Can increase / decrease minecount"""
        #Convert list of tuples into a set for better use later
        p1, p2 = set(self.chromosome), set(other.chromosome)

        #Identify shared genes (probably good)
        bothParents = list(p1 & p2)
        #random.shuffle(bothParents)

        #Identify independent genes & shuffles them (probably not correct)
        singleParent = list((p1 | p2) - set(bothParents))
        random.shuffle(singleParent)

        #Child gets shared genes
        childChromosomes = bothParents[:]

        #Child gets an already randomized gene until all mines are done
        while len(childChromosomes) < len(self.chromosome):
            childChromosomes.append(singleParent.pop())

        #Make a new child, load it which chromosomes, see if its better
        child = Individual(False)
        child.chromosome = childChromosomes
        child.fitness = child.calcFitness()
        return child
        
    def mutate(self) -> bool:
        """Change a random mine"""
        #Make a list and determine which value is getting changed
        mines = list(self.chromosome)
        index = random.randint(0, len(mines) - 1)

        #Calculate all possible positions
        possibleMines = [
            (r, c) for r in range(len(self.boardToSolve)) for c in range(len(self.boardToSolve[0]))
        ]

        #Pick a random location from the set of all possible locations
        while True:
            new_pos = random.choice(possibleMines)
            if new_pos not in self.chromosome:
                break

        #Make the replacement and update values
        mines[index] = new_pos
        self.chromosome = set(mines)
        self.fitness = self.calcFitness()
        
    def chromTo2D(self) -> list[list[int]]:
        field = [[0 for _ in range(len(self.boardToSolve[0]))] for _ in range(len(self.boardToSolve))]
        mines = list(self.chromosome)

        for x,y in mines:
            field[x][y] = 1
        
        return field


    def readable(self, param) -> str:
        outString = ""
        for r in range(len(param)):
            for c in range(len(param[0])):
                outString += str(param[r][c]) + " "
            outString = outString[:-1] + "\n"
        
        return outString
            
        
         
