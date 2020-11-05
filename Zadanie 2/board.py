from typing import List
from pieces import *
from field import Field
from statuses import Statuses


class Board:
    def __init__(self, matrix: List[List[str]]):
        self.white_king_position = ()
        self.black_king_position = ()
        self.board = self.__parse_board(matrix)
        self.__fill_field_statuses()

    def __parse_board(self, matrix: List[List[str]]) -> List[List[Field]]:
        board = []
        for _ in matrix:
            board.append([])
        i = 0
        colors = ("white", "black")
        for row in matrix:
            j = 0
            for field in row:
                if field == '--':
                    board[i].append(Field(Piece(), j, i, Statuses.NULL))
                else:
                    color, piece = field.split('')
                    if color == 'w':
                        if piece == 'p':
                            board[i].append(Field(WPawn(), j, i, Statuses.PIECE))
                        elif piece == 'r':
                            board[i].append(Field(Rook(colors[0]), j, i, Statuses.PIECE))
                        elif piece == 'k':
                            board[i].append(Field(Knight(colors[0]), j, i, Statuses.PIECE))
                        elif piece == 'b':
                            board[i].append(Field(Bishop(colors[0]), j, i, Statuses.PIECE))
                        elif piece == 'q':
                            board[i].append(Field(Queen(colors[0]), j, i, Statuses.PIECE))
                        elif piece == 'W':
                            board[i].append(Field(King(colors[0]), j, i, Statuses.PIECE))
                            self.white_king_position = (j, i)
                    else:
                        if piece == 'p':
                            board[i].append(Field(BPawn(), j, i, Statuses.PIECE))
                        elif piece == 'r':
                            board[i].append(Field(Rook(colors[1]), j, i, Statuses.PIECE))
                        elif piece == 'k':
                            board[i].append(Field(Knight(colors[1]), j, i, Statuses.PIECE))
                        elif piece == 'b':
                            board[i].append(Field(Bishop(colors[1]), j, i, Statuses.PIECE))
                        elif piece == 'q':
                            board[i].append(Field(Queen(colors[1]), j, i, Statuses.PIECE))
                        elif piece == 'W':
                            board[i].append(Field(King(colors[1]), j, i, Statuses.PIECE))
                            self.black_king_position = (j, i)
                j += 1
            i += 1
        return board

    def __fill_field_statuses(self) -> None:
        for row in self.board:
            for field in row:
                for move in field.piece.valid_moves:
                    if isinstance(field.piece, BPawn) or isinstance(field.piece, WPawn):
                        x_move = field.x + field.piece.attack_moves[0]
                        y_move = field.y + field.piece.attack_moves[1]
                    else:
                        x_move = field.x + move[0]
                        y_move = field.y + move[1]
                    if not (y_move >= len(self.board) or y_move < 0) and (x_move >= len(row) or x_move < 0):
                        if not self.__is_move_blocked(field.piece, (field.x, field.y), move):
                            if self.board[y_move][x_move].status[0] is not Statuses.NULL:
                                if self.board[y_move][x_move].piece.color == field.piece.color:
                                    field.status.append(Statuses.DEFENDED)
                                else:
                                    field.status.append(Statuses.ATTACKED)
                            else:
                                field.status.append(Statuses.ATTACKED)

    def __is_move_blocked(self, piece: Piece, position: tuple, move: tuple) -> bool:
        if isinstance(piece, Knight) or isinstance(piece, King) or isinstance(piece, WPawn) or isinstance(piece, BPawn):
            return False
        else:
            if isinstance(piece, Rook):
                return self.__is_rook_move_blocked(position, move)
            elif isinstance(piece, Bishop):
                return self.__is_bishop_move_blocked(position, move)
            elif isinstance(piece, Queen):
                if move[0] == 0 or move[1] == 0:
                    return self.__is_rook_move_blocked(position, move)
                else:
                    return self.__is_bishop_move_blocked(position, move)

    def __is_rook_move_blocked(self, position: tuple, move: tuple) -> bool:
        if move[0] == 0:
            for y in range(position[1] + 1, position[1] + move[1]):
                if self.board[y][position[0]].status[0] == Statuses.PIECE:
                    return True
            return False
        else:
            for x in range(position[0] + 1, position[0] + move[0]):
                if self.board[position[1]][x].status[0] == Statuses.PIECE:
                    return True
            return False

    def __is_bishop_move_blocked(self, position: tuple, move: tuple) -> bool:
        x, y = [], []
        if move[0] > 0:
            x = range(1, move[0])
        else:
            x = range(-1, move[0], -1)
        if move[1] > 0:
            y = range(1, move[1])
        else:
            y = range(-1, move[1], -1)
        for i, j in zip(x, y):
            if self.board[position[1] + j][position[0] + i].status[0] == Statuses.PIECE:
                return True
        return False

    def __is_check(self, king_position):
        def is_check_after_move(piece: Piece, move: tuple, position: tuple):
            x_move = position[0] + move[0]
            y_move = position[1] + move[1]
            if not (y_move >= len(self.board) or y_move < 0) and (x_move >= len(row) or x_move < 0):
                if not self.__is_move_blocked(piece, position, move):
                    return isinstance(self.board[position[1] + move[1]][position[0] + move[0]].piece, King)
                else:
                    return False
            else:
                return False

        if self.board[king_position[0]][king_position[1]].status.__contains__(Statuses.ATTACKED):
            return ()
        else:
            for row in self.board:
                for field in row:
                    for move in field.piece.valid_moves:
                        x_move = field.x + move[0]
                        y_move = field.y + move[1]
                        if not (y_move >= len(self.board) or y_move < 0) and (x_move >= len(row) or x_move < 0):
                            if not self.__is_move_blocked(field.piece, (field.x, field.y), move):
                                if self.board[y_move][x_move].piece.color != field.piece.color:
                                    if is_check_after_move(field.piece, move, (x_move, y_move)):
                                        return x_move, y_move
            return -1, -1




