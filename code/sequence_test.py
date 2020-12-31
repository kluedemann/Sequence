def check_right(row_ind, col_ind, color):
    sequence = []
    if 0 <= row_ind < len(board) and 0 <= col_ind < len(board[0]):
        if board[row_ind][col_ind] == color:
            sequence.append((row_ind, col_ind))
            sequence.extend(check_right(row_ind, col_ind + 1, color))
    return sequence


def check_down(row_ind, col_ind, color):
    sequence = []
    if 0 <= row_ind < len(board) and 0 <= col_ind < len(board[0]):
        if board[row_ind][col_ind] == color:
            sequence.append((row_ind, col_ind))
            sequence.extend(check_down(row_ind + 1, col_ind, color))
    return sequence


def check_down_right(row_ind, col_ind, color):
    sequence = []
    if 0 <= row_ind < len(board) and 0 <= col_ind < len(board[0]):
        if board[row_ind][col_ind] == color:
            sequence.append((row_ind, col_ind))
            sequence.extend(check_down_right(row_ind + 1, col_ind + 1, color))
    return sequence


def check_sequence(row_ind, col_ind, color):
    right = check_right(row_ind, col_ind, color)
    down = check_down(row_ind, col_ind, color)
    down_right = check_down_right(row_ind, col_ind, color)
    sequences = [right, down, down_right]
    valid_sequences = []
    for sequence in sequences:
        if len(sequence) == 5:
            valid_sequences.append(sequence)
    return valid_sequences


def check_sequences(color):
    sequences = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            sequences += check_sequence(i, j, color)
    return sequences


board = [[1, 1, 1, 1, 1],
         [1, 1, 0, 0, 0],
         [1, 0, 1, 0, 0],
         [1, 0, 0, 1, 0],
         [1, 0, 0, 0, 1],
         [1, 0, 0, 0, 0]]


def main():

    sequences = check_sequences(1)
    print(len(sequences))
    print(sequences)


main()
