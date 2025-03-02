import random
from math import floor as floor

def genetic_algorithm(popSize = 10, generations = 100, mutationRate = 0.1, toSolve = [[1]], numMines = 1):
    #setup the Individual class properties
    Individual.boardToSolve = toSolve
    print(Individual.boardToSolve)
    Individual.startingMines = numMines
    print(Individual.startingMines)
    
    #Create initial population
    pop = [Individual() for _ in range(popSize)]

    #Begin the generations
    for gen in range(generations):
        #Sort by fitness value
        pop.sort(key=lambda indiv: indiv.fitness, reverse=True)
        
        #Are we done?
        if pop[0].fitness == numMines:
            print(f"Exiting early! Generation {gen} was a perfect solution!")
            return pop[0].chromosome
        
        print(f"Generation {gen} best value is {pop[0].fitness}.")
        #Let the best 50% mate
        parents = pop[: popSize//2]

        #The parents go into next generation to reduce slideback
        nextGeneration = [parent for parent in parents]

        #Mate each of the parents with a random entity (can mate with self)
        for i in range(len(parents)):
            #print(f"Rank {i} with value {parents[i].fitness}")
            p1 = parents[i]
            p2 = parents[random.randint(0, len(parents)-1)]
            child = p1.mate(p2)
            nextGeneration.append(child)
        
        #Mutations
        for i in range(len(nextGeneration)):
            if random.random() < mutationRate:
                nextGeneration[i].mutate()
        
        pop = nextGeneration
    
    print(f"No exact solution found after {generations} generations.")
    pop.sort(key=lambda indiv: indiv.fitness, reverse=True)
    return pop[0].chromosome




class Individual:
    """Represents a member of the population"""

    adjacents = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0,1), (1, -1), (1, 0), (1, 1)]
    boardToSolve = [[1]]
    startingMines = 1

    def __init__(self):
        self.chromosome = self.createIndividual()
        self.fitness = self.calcFitness()
    
    def createIndividual(self) -> list[list[int]]:
        """Creates a guess at what the minefield might be"""
        rows = len(self.boardToSolve)
        cols = len(self.boardToSolve[0])
        field = [[0 for _ in range(rows)] for _ in range(cols)]
        mockField = [(r, c) for r in range(rows) for c in range(cols)]
        minePositions = random.sample(mockField, self.startingMines)
        for r, c in minePositions:
                field[r][c] += 1
        return field
    
    def calcFitness(self) -> int:
        fitnessScore = 0
        for x in range(len(self.boardToSolve)):
            for y in range(len(self.boardToSolve[0])):
                #Only need to check if we have a mine on the cell
                if self.chromosome[x][y] == 1:
                    count = 0
                    for dx, dy in self.adjacents:
                        checkX, checkY = x + dx, y + dy
                        #Only check cells that exist on the board
                        if 0 <= checkX < len(self.boardToSolve) and 0 <= checkY < len(self.boardToSolve[0]):
                            #Count adjacent mines
                            if self.chromosome[checkX][checkY] == 1:
                                count += 1

                    #There are the correct amount of adjacent mines
                    if count == self.boardToSolve[x][y]:
                            fitnessScore += 1
        return fitnessScore
    
    def mate(self, other: "Individual") -> "Individual":
        """Mate two parents to make a child instance. Can increase / decrease minecount"""
        child = Individual()
        #Randomly takes each cell's mine value from a parent.
        for x in range(len(self.chromosome)):
            for y in range(len(self.chromosome[0])):
                fromSelf = random.random() < 0.5
                if fromSelf:
                    child.chromosome[x][y] = self.chromosome[x][y]
                else:
                    child.chromosome[x][y] = other.chromosome[x][y]
        
        #Update the fitness value and return
        child.fitness = child.calcFitness()
        return child
    


        
    
    def mutate(self) -> bool:
        """Adds or removes a random mine"""
        newX = random.randint(0,len(self.chromosome)-1)
        newY = random.randint(0,len(self.chromosome[0])-1)

        #Change the random position
        if self.chromosome[newX][newY] == 0:
            self.chromosome[newX][newY] = 1
        elif self.chromosome[newX][newY] == 1:
            self.chromosome[newX][newY] = 0
        else:
            #Shouldn't be possible unless you modified chromosome illegally
            return False
        
        #Finished the swap
        return True
            
        
         
