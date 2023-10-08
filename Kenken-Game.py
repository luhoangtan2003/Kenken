import math

class Coord:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def Index_Of(self):
        return GRID*self.x+self.y

def Get_Point(Index):
    return Coord(Index//GRID, Index%GRID)

class Constrains:
    def __init__(self, Operator = None, Value = 0):
        self.List_Coord = []
        self.Operator = Operator
        self.Value = Value

class Kenken:
    def __init__(self):
        self.Cells = []
        self.Cages = []

    def Value_Of_Cell(self, Point):
        return self.Cells[Point.x][Point.y]

    def Get_Cage(self, Point):
        for Index_Of_Cage in range(len(self.Cages)):
            for Element in self.Cages[Index_Of_Cage].List_Coord:
                if Element.x == Point.x and Element.y == Point.y:
                    return Index_Of_Cage

    def Is_Filled(self):
        for Row, Rows in enumerate(self.Cells):
            for Col, Cell in enumerate(Rows):
                if Cell == 0:
                    return False
        return True

    def Is_Full_Cage(self, Index):
        for Element in self.Cages[Index].List_Coord:
            if self.Value_Of_Cell(Element) == 0:
                return False
        return True

    def Check_Duplicate(self,Point, Value):
        for i in range(GRID):
            if self.Cells[i][Point.y] == Value:
                return False
        for i in range(GRID):
            if self.Cells[Point.x][i] == Value:
                return False
        return True

    def Total(self, Index):
        Total = 0
        for Coord in self.Cages[Index].List_Coord:
            Total += self.Value_Of_Cell(Coord)
        Yes_1 = True if Total == self.Cages[Index].Value and self.Is_Full_Cage(Index) else False
        Yes_2 = True if Total<self.Cages[Index].Value and not self.Is_Full_Cage(Index) else False
        return True if Yes_1 or Yes_2 else False

    def Diff(self, Index):
        if not self.Is_Full_Cage(Index):
            return True
        Diff = 0
        for Coord in self.Cages[Index].List_Coord:
            Diff -= self.Value_Of_Cell(Coord)
            Diff = abs(Diff)
        return True if Diff == self.Cages[Index].Value else False

    def Mult(self, Index):
        Mult = 1
        for Coord in self.Cages[Index].List_Coord:
            Cell_Value = self.Value_Of_Cell(Coord)
            Mult = Mult * (1 if Cell_Value == 0 else Cell_Value)
        Yes_1 = True if Mult == self.Cages[Index].Value and self.Is_Full_Cage(Index) else False
        Yes_2 = True if Mult<=self.Cages[Index].Value and not self.Is_Full_Cage(Index) else False
        return True if Yes_1 or Yes_2 else False

    def Divi(self, Index):
        if not self.Is_Full_Cage(Index):
            return True
        Divi = 1
        for Coord in self.Cages[Index].List_Coord:
            Cell_Value = self.Value_Of_Cell(Coord)
            x = 1 if Cell_Value==0 else Cell_Value
            Divi = Divi//x if Divi>x else x//Divi
        if Divi == self.Cages[Index].Value:
            return True
        else:
            return False

    def Check_Constrains(self, Point):
        Index = self.Get_Cage(Point)
        Calculation = self.Cages[Index].Operator
        if Calculation == '+':
            return self.Total(Index)
        elif Calculation == '-':
            return self.Diff(Index)
        elif Calculation == 'x':
            return self.Mult(Index)
        elif Calculation == '/':
            return self.Divi(Index)
        elif Calculation == '=':
            return True if self.Cages[Index].Value == self.Value_Of_Cell(Point) else False
        else: return False

    def Show_Board(self):
        print("Kenken board:")
        for i in range(GRID):
            for j in range(GRID):
                if j % GRID == 0:
                    print("|",end='')
                print("{:>2} |".format(self.Cells[i][j]),end='')
            print()
        print()

    def Show_Cage_Board(self):
        print("Board of cages:")
        for i in range(GRID):
            for j in range(GRID):
                Point = Coord(i,j)
                if j % GRID == 0:
                    print("|",end='')
                Total_Value = self.Cages[self.Get_Cage(Point)].Value
                Operator = self.Cages[self.Get_Cage(Point)].Operator
                print("{:>5}{}|".format(Total_Value,Operator),end='')
            print()
        print()

    def Input_Data(self):
        with open("D:\Github\Kenken\Kenken.txt",'r') as File:
            Lines = File.readlines()
            Num_Line = int(Lines.pop(0))
            self.Cages = [Constrains() for i in range(Num_Line)]
            Num_Cell = 0
            global GRID
            for i in range(Num_Line):
                Line = Lines[i].split()
                self.Cages[i].Value = int(Line[0])
                self.Cages[i].Operator = Line[1]
                Step = 3
                for j in range(int(Line[2])):
                    x = int(Line[Step+0])
                    y = int(Line[Step+1])
                    self.Cages[i].List_Coord.append(Coord(x,y))
                    Num_Cell += 1
                    Step += 2
            GRID = int(math.sqrt(Num_Cell))
            self.Cells = [[0 for Cols in range(GRID)] for Rows in range(GRID)]


    def Solve_Board(self, Row, Col):
        if self.Is_Filled():
            return True
        if Col == GRID:
            Row += 1
            Col = 0
        global Num_State
        for Value in range(1,GRID+1,1):
            Point = Coord(Row,Col)
            if self.Check_Duplicate(Point, Value):
                self.Cells[Row][Col] = Value
                Num_State += 1
                if self.Check_Constrains(Point):
                    if self.Solve_Board(Row, Col+1) == True:
                        return True
            self.Cells[Row][Col] = 0
        return False

Num_State = 0
GRID = 0
if __name__ == "__main__":
    Puzzle = Kenken()
    Puzzle.Input_Data()
    Puzzle.Show_Board()
    Puzzle.Show_Cage_Board()
    if Puzzle.Solve_Board(0,0):
        print("Tìm lời giải thành công!!!")
        Puzzle.Show_Board()
    else:
        print("Không thể tìm ra đáp án!!!")
    print("Số lượng trạng thái:",Num_State)