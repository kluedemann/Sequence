def check_right(row_ind, col_ind, color):
    if 0 <= col_ind < len(board[0]):
        if board[row_ind][col_ind] == color:
            return 1 + check_right(row_ind, col_ind + 1, color)
    return 0


def check_down(row_ind, col_ind, color):
    if 0 <= row_ind < len(board):
        if board[row_ind][col_ind] == color:
            return 1 + check_down(row_ind + 1, col_ind, color)
    return 0


def check_down_right(row_ind, col_ind, color):
    if 0 <= row_ind < len(board) and 0 <= col_ind < len(board[0]):
        if board[row_ind][col_ind] == color:
            return 1 + check_down_right(row_ind + 1, col_ind + 1, color)
    return 0


def check_down_left(row_ind, col_ind, color):
    if 0 <= row_ind < len(board) and 0 <= col_ind < len(board[0]):
        if board[row_ind][col_ind] == color:
            return 1 + check_down_left(row_ind + 1, col_ind - 1, color)
    return 0


def check_sequence(row_ind, col_ind, color):
    right = check_right(row_ind, col_ind, color)
    down = check_down(row_ind, col_ind, color)
    down_right = check_down_right(row_ind, col_ind, color)
    down_left = check_down_left(row_ind, col_ind, color)
    sequences = [right, down, down_right, down_left]
    count = 0
    for sequence in sequences:
        if sequence == 5 or sequence == 10:
            count += 1
    return count


def check_sequences(color):
    sequences = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            sequences += check_sequence(i, j, color)
    return sequences


board = [[1, 1, 1, 1, 1, 1],
         [1, 1, 0, 0, 1, 0],
         [1, 0, 1, 1, 0, 0],
         [1, 0, 1, 1, 0, 0],
         [1, 1, 0, 0, 1, 0],
         [1, 0, 0, 0, 0, 1]]
# board = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]


def main():

    sequences = check_sequences(1)
    print(sequences)


main()
