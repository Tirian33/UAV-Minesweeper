import random #randomness

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
        """Determines fitness score"""
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
        
        #Compare scores
        for r in range(len(testField)):
            for c in range(len(testField[0])):
                if testField[r][c] == self.boardToSolve[r][c]:
                    score += 1
                else:
                    #Mark it a problem
                    problems[r][c] = 1

                    #If its an edge case 0 or 9 give extra penalty
                    if self.boardToSolve[r][c] == 0 or self.boardToSolve[r][c] == 9:
                        score -=1
        #Update personal problemBoard
        self.problemBoard = problems
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
        
    def mutate(self, moveAdjChance=0.6) -> bool:
        """Change a random mine"""
        #Make a list and determine which value is getting changed
        mines = list(self.chromosome)
        possibilities = [(x) for x in range(len(mines))]
        index = random.choice(possibilities)

        #Find a problem gene, move it to an adjacent problem tile
        if random.random() < moveAdjChance:
            shiftCells = self.effectedCells[:4] + self.effectedCells[5:]

            while True:
                x,y = mines[index]
                #Don't need to change correct genes pick another
                if self.problemBoard[x][y] == 0:
                    if len(possibilities) == 1:
                        #All mine placemnts have no neighbors that are wrong
                        possibilities = [(x) for x in range(len(mines))]
                        index = random.choice(possibilities)
                        break
                    possibilities.remove(index)
                    index = random.choice(possibilities)
                    continue

                #Found a gene that isn't correct, move it adjacent
                swapto = []
                for dx, dy in shiftCells:
                    checkX = x + dx
                    checkY = y + dy
                    #Inbounds, is also in error, doesn't have a mine on it already (NO DUPES!)
                    if 0 <= checkX < len(self.boardToSolve) and 0 <= checkY < len(self.boardToSolve[0]) and self.problemBoard[checkX][checkY] == 1 and (checkX,checkY) not in self.chromosome:
                        swapto.append((checkX,checkY))
                
                #Selected cell is incorrect, but all neigbors havea mine on them so I can't move it adjacent - mutate other way
                if not swapto:
                    break

                #Local Maxima handler for diagnal issue
                if len(swapto) >= 2:
                    #Down left
                    if (x-1, y) in swapto and (x, y+1) in swapto and (x-1, y+1) in mines and self.problemBoard[x-1][y+1]:
                        #print(f"Changing {mines[index]} -> {(x+1, y)} & {mines[mines.index((x-1, y+1))]} -> {(x, y+1)}")
                        mines[index] = (x-1, y)
                        mines[mines.index((x-1, y+1))] = (x, y+1)
                        self.chromosome = set(mines)
                        self.fitness = self.calcFitness()
                        return True

                    #Down right
                    elif (x+1, y) in swapto and (x, y+1) in swapto and (x+1, y+1) in mines and self.problemBoard[x+1][y+1]:
                        #print(f"Changing {mines[index]} -> {(x+1, y)} & {mines[mines.index((x+1, y+1))]} -> {(x, y+1)}")
                        mines[index] = (x+1, y)
                        mines[mines.index((x+1, y+1))] = (x, y+1)
                        self.chromosome = set(mines)
                        self.fitness = self.calcFitness()
                        return True

                #Now for every FP there is a FN adjacent & vice versa There WILL be a neighbor that is incorrect
                mines[index] = random.choice(swapto)
                self.chromosome = set(mines)
                self.fitness = self.calcFitness()
                return True
        
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
        return True
        
    def chromTo2D(self) -> list[list[int]]:
        """Turn the set of mine locations into a 2D array; 1 = mine 0 = safe"""
        field = [[0 for _ in range(len(self.boardToSolve[0]))] for _ in range(len(self.boardToSolve))]
        mines = list(self.chromosome)

        for x,y in mines:
            field[x][y] = 1
        
        return field