from board import Board


def main():
    matrix = []
    for _ in range(8):
        line = input()
        line = line.split("', '")
        line[0] = line[0][2:]
        line[7] = line[7][:2]
        matrix.append(line)
    board = Board(matrix)
    print(board.print_checkmate())


if __name__ == '__main__':
    main()
