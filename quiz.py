def reverse_list(l:list):

    """

    TODO: Reverse a list without using any built in functions

 

    The function should return a sorted list.

    Input l is a list which can contain any type of data.

    """
    # 1. reverse the list using two pointers
    n = len(l)
    for i in range(n // 2):
        l[i], l[n - i - 1] = l[n - i - 1], l[i]

    # 2. sort the reversed list using bubble sort
    for i in range(len(l)):
        for j in range(len(l) - i - 1):
            # Compare the string representation of the elements for compare for any type of data
            if str(l[j]) < str(l[j + 1]):
                l[j], l[j + 1] = l[j + 1], l[j]
    return l

def solve_sudoku(matrix):

    """

    TODO: Write a programme to solve 9x9 Sudoku board.

 

    Sudoku is one of the most popular puzzle games of all time. The goal of Sudoku is to fill a 9×9 grid with numbers so that each row, column and 3×3 section contain all of the digits between 1 and 9. As a logic puzzle, Sudoku is also an excellent brain game.

 

    The input matrix is a 9x9 matrix. You need to write a program to solve it.

    """
    def isValid(row,col,k,matrix):
        # determine whether the board is valid
        # determine whether there is conflict in row
        for i in range(9):
            if matrix[row][i] == k:
                return False
        # determine whether there is conflict in col
        for j in range(9):
            if matrix[j][col] == k:
                return False
        # determine whether there is conflict within the board
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if matrix[i][j] == k:
                    return False
        return True

    # Return bool, as long as we only need to find one sudoku, return
    def backtrack(matrix) -> bool:
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                # do action when it is not filled by digit
                if matrix[i][j].isdigit():
                    continue
                for k in range(1,10):
                    if isValid(i, j, str(k), matrix):
                        matrix[i][j] = str(k)
                        # if it is filled
                        res = backtrack(matrix)
                        if res == True:
                            return True
                        matrix[i][j] = '.' # backtrack
                return False
        return True
    
    # Change all the element type in the matrix into string
    matrix = [[str(element) for element in row] for row in matrix]
    backtrack(matrix)
    return matrix

