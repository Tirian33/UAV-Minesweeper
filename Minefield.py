import math
import random #for .randint

class Minefield:
    """Abstraction of the minefield"""
    #Class variable - all instances use need this
    adjacents = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0,1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, r = 10, c = 10, mines = 20):
        #Instance variables
        print(f"r {r} c {c} m {mines}")
        self.rows = r
        self.cols = c
        self.field = [[0 for _ in range(r)] for _ in range(c)]
        self.mineLoc = [row[:] for row in self.field] #Rather than importing copy, create slices of each row

        #Throwing away results, no logic changes on T/F
        _ =self._plantMines(math.floor(mines/100 * r * c))
    
    #
    def _incrementAdjacent(self, x: int, y: int) -> None:
        """
        Increment minecount for adjacent cells for given cell.
        @param x The row of initial cell
        @param y the column of initial cell
        """
        for dx, dy in self.adjacents:
            checkX, checkY = x + dx, y + dy
            #Only increment if: Cell is in the field & cell is not a mine
            if 0 <= checkX < self.rows and 0 <= checkY < self.cols and self.field[checkX][checkY] != -1:
                self.field[checkX][checkY] += 1


    def _plantMines(self, numMines: int) -> bool:
        """
        Increment minecount for adjacent cells for given cell.
        @param numMines Number of mines to place onto the field
        @return Success/Fail of operation
        """
        #Safety
        maxCells = self.rows * self.cols
        #Bootleg case statement
        if numMines == 0:
            #Nothing is a mine
            pass
        elif numMines > maxCells:
            #Idiot check
            return False
        elif numMines == maxCells:
            #Everything is a mine
            for r in range(self.rows):
                for c in range(self.cols):
                    self.field[r][c] +=1
                    self.mineLoc[r][c] = 1
                    self._incrementAdjacent(r, c)
        else:
            #Create a X,Y coordinate for all cells
            mockField = [(r, c) for r in range(self.rows) for c in range(self.cols)]
            print(f"There are {len(mockField)} cells. Placing {numMines} mines...")
            minePositions = random.sample(mockField, numMines)

            #Place mines at random sample'd locations
            for r, c in minePositions:
                self.field[r][c] +=1
                self.mineLoc[r][c] = 1
                self._incrementAdjacent(r,c)
        
        return True

    #Means of accessing data
    def getUAVInfo(self) -> list[list[int]]:
        return self.field

    def getActualField(self) -> list[list[int]]:
        return self.mineLoc
    
    #Means of printing data
    def stringUAV(self) -> str:
        outString = ""
        for r in range(self.rows):
            for c in range(self.cols):
                outString += str(self.field[r][c]) + " "
            outString = outString[:-1] + "\n"
        
        return outString
    
    def stringMines(self) -> str:
        outString = ""
        for r in range(self.rows):
            for c in range(self.cols):
                outString += str(self.mineLoc[r][c]) + " "
            outString = outString[:-1] + "\n"
        
        return outString
