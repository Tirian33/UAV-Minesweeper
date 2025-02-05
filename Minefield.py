import math #for ceil()
import random #for .randint

class Minefield:
    """Abstraction of the minefield"""

    field = [[]]
    visibleField = [[]]
    adjacents = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0,1), (1, -1), (1, 0), (1, 1)]
    rows = 0
    cols = 0

    def __init__(self, rows, cols, mines, isAmount, firstX, firstY):
        self.rows = rows-1
        self.cols = cols-1
        self.field = [[0]*cols]*rows
        self.visibleField = [['?']*cols]*rows

        if (isAmount):
            for i in range(mines):
                self.plantMine(firstX, firstY)
        else:
            for i in range(math.ceil(mines/100 * rows * cols)):
                self.plantMine(firstX, firstY)
        
        self.select(firstX, firstY)
    
    #The selecting action - returns T/F depending on if you lived/died
    def select(self, x, y):
        selCellValue = self.field[x][y]
        #Check for death
        if selCellValue == -1:
            return False
        
        elif selCellValue == 0:
            #mark cell & then recursive calls
            self.visibleField[x][y] = 0

            for dx, dy in self.adjacents:
                checkX, checkY = x + dx, y + dy
                #Only recursive if: Cell is in the field & cell is not a mine
                if 0 < checkX <= self.rows and 0 < checkY <= self.cols and self.field[checkX][checkY] != -1:
                    self.select(checkX,checkY)
        
        #Reveal non-0 mine adjacent cell
        else:
            self.visibleField[x,y] = selCellValue

        return True

    #This can be optimized to be selecting candidates from a set
    def genMineCandidate(self):
        xLoc = random.randint(0, self.cols)
        yLoc = random.randint(0, self.rows)
        return [xLoc, yLoc]

    def incrementAdjacent(self, x, y):
        #The 8 adjacent cells to a cell

        for dx, dy in self.adjacents:
            checkX, checkY = x + dx, y + dy
            #Only increment if: Cell is in the field & cell is not a mine
            if 0 < checkX <= self.rows and 0 < checkY <= self.cols and self.field[checkX][checkY] != -1:
                self.field[checkX][checkY] += 1


    def plantMine(self, safeX, safeY):
        while(True):
            candidateX, candidateY = self.genMineCandidate()

            #No mines on safe 3x3 about start point
            if (safeX -1 <= candidateX <= safeX + 1) and (safeY -1 <= candidateY <= safeY + 1):
                #No mines on same tile
                if self.field[candidateX][candidateY] != -1:
                    self.field[candidateX][candidateY] = -1
                    self.incrementAdjacent(candidateX, candidateY)
                    
                    #success - now leave
                    break
    
    def printVision(self):
        outString = ""

        for r in self.rows:
            for c in range(0, self.cols):
                if c!= self.cols:
                    outString += self.visibleField[c][r] + "\t"
                else:
                    outString += self.visibleField[c][r] + "\n"


        print(outString)
        print("\n VS \n")
        print(self.visibleField)