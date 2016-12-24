def unique(array):
    has = []
    for i in range(len(array)):
        if array[i] in has:
            return False
        if array[i] is not 0:
            has += [array[i]]
    return True


class Board():
    """
      - - -   - - -   - - -   row
    |   3   | 9     |   2   |  1
    | 8     |     2 |     7 |  2
    |     1 | 4     | 6     |  3
      - - -   - - -   - - -   
    |   9   |   4   | 5   2 |  4
    |       | 6   3 |       |  5
    | 7   6 |   1   |   8   |  6
      - - -   - - -   - - -
    |     9 |     4 | 1     |  7
    | 2     | 8     |     3 |  8
    |   7   |     9 |   5   |  9
      - - -   - - -   - - -
coln  1 2 3   4 5 6   7 8 9
    """
    
    
    def __init__(self,board):
        self.board = board

    def boxes(self):
        boxes = []
        for i in range(3):
            boxes.append([])
            for j in range(3):
                boxes[i].append([])
        rows = self.rows()
        for i in range(3):
            for j in range(3):
                boxes[0][0] += [rows[i][j]]
            for j in range(3,6):
                boxes[0][1] += [rows[i][j]]
            for j in range(6,9):
                boxes[0][2] += [rows[i][j]]
        for i in range(3,6):
            for j in range(3):
                boxes[1][0] += [rows[i][j]]
            for j in range(3,6):
                boxes[1][1] += [rows[i][j]]
            for j in range(6,9):
                boxes[1][2] += [rows[i][j]]
        for i in range(6,9):
            for j in range(3):
                boxes[2][0] += [rows[i][j]]
            for j in range(3,6):
                boxes[2][1] += [rows[i][j]]
            for j in range(6,9):
                boxes[2][2] += [rows[i][j]]
        return boxes
    
    def columns(self):
        columns = []
        for i in range(9):
            columns.append([])
        for i in range(9):
            columns[i] += [row[i] for row in self.board]
        return columns        
    
    def rows(self):
        rows = []
        for i in range(9):
            rows += [self.board[i]]
        return rows
    
    def printBoard(self):
        string = ""
        for i in range(9):
            if i%3 == 0:
                print "  - - -   - - -   - - -"
            for j in range(9):
                if j%3 == 0:
                    print "|",
                if self.board[i][j] is not 0: print str(self.board[i][j]),
                else: print " ",
            print "|"
        print "  - - -   - - -   - - -"

    def add(self,x,y,entry):
        self.board[x][y] = entry
        
    def check(self, x=None, y=None):
        if x and y:
            if not unique(self.rows()[x]):
                return False
            if not unique(self.columns()[y]):
                return False
            if not unique(self.boxes()[x/3][y/3]):
                return False
            return True
        else:
            for box in self.boxes():
                if not unique(box):
                    return False
            for row in self.rows():
                if not unique(row):
                    return False
            for column in self.columns():
                if not unique(column):
                    return False
            return True,
    
    def isFull(self):
        for row in self.rows():
            if 0 in row:
                return False
        return True
    
    def final(self):
        for row in self.rows():
            if 0 in row:
                return False
        return self.check()