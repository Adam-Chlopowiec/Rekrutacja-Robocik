from typing import List
from pieces import *
from field import Field
from statuses import Statuses
from copy import deepcopy


class Board:
    def __init__(self, matrix: List[List[str]]):
        self.white_king_position = ()
        self.black_king_position = ()
        self.board = self.__parse_board(matrix)
        self.BOARD_LENGTH = 8

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
                    color, piece = field[0], field[1]
                    if color == 'w':
                        fields = {
                            'p': Field(WPawn(), j, i, Statuses.PIECE),
                            'r': Field(Rook(colors[0]), j, i, Statuses.PIECE),
                            'k': Field(Knight(colors[0]), j, i, Statuses.PIECE),
                            'b': Field(Bishop(colors[0]), j, i, Statuses.PIECE),
                            'q': Field(Queen(colors[0]), j, i, Statuses.PIECE),
                            'W': Field(King(colors[0]), j, i, Statuses.PIECE)
                        }
                        board[i].append(fields[piece])
                        if piece == 'W':
                            self.white_king_position = (j, i)
                    else:
                        fields = {
                            'p': Field(BPawn(), j, i, Statuses.PIECE),
                            'r': Field(Rook(colors[1]), j, i, Statuses.PIECE),
                            'k': Field(Knight(colors[1]), j, i, Statuses.PIECE),
                            'b': Field(Bishop(colors[1]), j, i, Statuses.PIECE),
                            'q': Field(Queen(colors[1]), j, i, Statuses.PIECE),
                            'W': Field(King(colors[1]), j, i, Statuses.PIECE)
                        }
                        board[i].append(fields[piece])
                        if piece == 'W':
                            self.black_king_position = (j, i)
                j += 1
            i += 1
        return board

    def __fill_field_statuses(self) -> None:
        for row in self.board:
            for field in row:
                for move in field.piece.valid_moves:
                    x_move = field.x + move[0]
                    y_move = field.y + move[1]
                    if not (y_move >= self.BOARD_LENGTH or y_move < 0 or x_move >= self.BOARD_LENGTH or x_move < 0):
                        if not self.__is_move_blocked(field.piece, (field.x, field.y), move):
                            if isinstance(field.piece, King):
                                if self.board[y_move][x_move].status[0] != Statuses.NULL:
                                    if self.board[y_move][x_move].piece.color == field.piece.color:
                                        if field.piece.color == "black":
                                            self.board[y_move][x_move].status.append(Statuses.DEFENDED_BLACK_KING)
                                        else:
                                            self.board[y_move][x_move].status.append(Statuses.DEFENDED_WHITE_KING)
                                        field.piece.defended_fields.append(self.board[y_move][x_move])
                                    else:
                                        if field.piece.color == "black":
                                            self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK_KING)
                                        else:
                                            self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE_KING)
                                        field.piece.attacked_fields.append(self.board[y_move][x_move])
                                else:
                                    if field.piece.color == "black":
                                        self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK_KING)
                                    else:
                                        self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE_KING)
                                    field.piece.attacked_fields.append(self.board[y_move][x_move])
                            else:
                                if self.board[y_move][x_move].status[0] != Statuses.NULL:
                                    if self.board[y_move][x_move].piece.color == field.piece.color:
                                        if field.piece.color == "black":
                                            self.board[y_move][x_move].status.append(Statuses.DEFENDED_BLACK)
                                        else:
                                            self.board[y_move][x_move].status.append(Statuses.DEFENDED_WHITE)
                                        field.piece.defended_fields.append(self.board[y_move][x_move])
                                    else:
                                        if field.piece.color == "black":
                                            self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK)
                                        else:
                                            self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE)
                                        field.piece.attacked_fields.append(self.board[y_move][x_move])
                                else:
                                    if field.piece.color == "black":
                                        self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK)
                                    else:
                                        self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE)
                                    field.piece.attacked_fields.append(self.board[y_move][x_move])

    def __is_move_blocked(self, piece: Piece, position: tuple, move: tuple) -> bool:
        if isinstance(piece, Knight) or isinstance(piece, King) or isinstance(piece, WPawn) or isinstance(piece, BPawn):
            return False
        else:
            if isinstance(piece, Rook):
                return self.__is_rook_move_blocked(position, move, piece.color)
            elif isinstance(piece, Bishop):
                return self.__is_bishop_move_blocked(position, move, piece.color)
            elif isinstance(piece, Queen):
                if move[0] == 0 or move[1] == 0:
                    return self.__is_rook_move_blocked(position, move, piece.color)
                else:
                    return self.__is_bishop_move_blocked(position, move, piece.color)

    def __is_rook_move_blocked(self, position: tuple, move: tuple, color: str) -> bool:
        if move[0] == 0:
            if move[1] > 0:
                for y in range(position[1] + 1, position[1] + move[1]):
                    if not (isinstance(self.board[y][position[0]].piece, King)
                            and self.board[y][position[0]].piece.color != color):
                        if self.board[y][position[0]].status[0] == Statuses.PIECE:
                            return True
                return False
            else:
                for y in range(position[1] - 1, position[1] + move[1], -1):
                    if not (isinstance(self.board[y][position[0]].piece, King)
                            and self.board[y][position[0]].piece.color != color):
                        if self.board[y][position[0]].status[0] == Statuses.PIECE:
                            return True
                return False
        else:
            if move[0] > 0:
                for x in range(position[0] + 1, position[0] + move[0]):
                    if not (isinstance(self.board[position[1]][x].piece, King)
                            and self.board[position[1]][x].piece.color != color):
                        if self.board[position[1]][x].status[0] == Statuses.PIECE:
                            return True
                return False
            else:
                for x in range(position[0] - 1, position[0] + move[0], -1):
                    if not (isinstance(self.board[position[1]][x].piece, King)
                            and self.board[position[1]][x].piece.color != color):
                        if self.board[position[1]][x].status[0] == Statuses.PIECE:
                            return True
                return False

    def __is_bishop_move_blocked(self, position: tuple, move: tuple, color: str) -> bool:
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
            if not (isinstance(self.board[position[1] + j][position[0] + i].piece, King)
                    and self.board[position[1] + j][position[0] + i].piece.color != color):
                if self.board[position[1] + j][position[0] + i].status[0] == Statuses.PIECE:
                    return True
        return False

    def __is_check(self, king_position) -> list:
        checks = []
        # TODO: Sprawdzic czy nie mozna zamiast isinstance king zrobic position = white_king_position (albo black)
        def is_check_after_move(piece: Piece, position: tuple) -> tuple:
            for move in field.piece.valid_moves:
                x_move = position[0] + move[0]
                y_move = position[1] + move[1]
                if not (y_move >= self.BOARD_LENGTH or y_move < 0 or x_move >= self.BOARD_LENGTH or x_move < 0):
                    if not self.__is_move_blocked(piece, position, move):
                        if piece.color != self.board[y_move][x_move].piece.color:
                            if isinstance(self.board[y_move][x_move].piece, King):
                                return True, move
            return False, None

        if Statuses.ATTACKED_WHITE in self.board[king_position[1]][king_position[0]].status \
                or Statuses.ATTACKED_BLACK in self.board[king_position[1]][king_position[0]].status:
            # TODO: Do zastanowienia sie jeszcze
            return checks
        else:
            for row in self.board:
                for field in row:
                    # TODO: Do zrobienia jeszcze pionki
                    if not (isinstance(field.piece, BPawn) or isinstance(field.piece, WPawn)):
                        for move in field.piece.valid_moves:
                            x_move = field.x + move[0]
                            y_move = field.y + move[1]
                            if not (y_move >= self.BOARD_LENGTH or y_move < 0
                                    or x_move >= self.BOARD_LENGTH or x_move < 0):
                                if not self.__is_move_blocked(field.piece, (field.x, field.y), move):
                                    if self.board[y_move][x_move].piece.color != field.piece.color:
                                        checking_move = is_check_after_move(field.piece, (x_move, y_move))
                                        if checking_move[0]:
                                            initial_move = (x_move, y_move)
                                            checks.append((initial_move, field, checking_move[1]))
                                            """
                                            if field.piece.color == "white":
                                                if isinstance(field.piece, King):
                                                    self.__remove_status(field.piece.attacked_fields, Statuses.ATTACKED_WHITE_KING)
                                                    self.__remove_status(field.piece.defended_fields, Statuses.DEFENDED_WHITE_KING)
                                                    self.__add_status()
                                                else:
                                                    self.__remove_status(field.piece.attacked_fields, Statuses.ATTACKED_WHITE)
                                                    self.__remove_status(field.piece.attacked_fields, Statuses.DEFENDED_WHITE)
                                            else:
                                                if isinstance(field.piece, King):
                                                    self.__remove_status(field.piece.attacked_fields, Statuses.ATTACKED_BLACK_KING)
                                                    self.__remove_status(field.piece.defended_fields, Statuses.DEFENDED_BLACK_KING)
                                                else:
                                                    self.__remove_status(field.piece.attacked_fields, Statuses.ATTACKED_BLACK)
                                                    self.__remove_status(field.piece.attacked_fields, Statuses.DEFENDED_BLACK)
                                            """
                                            # self.__move_piece((field.x, field.y), (x_move, y_move), field.piece)
                                            # self.__clear_statuses()
                                            # self.__fill_field_statuses()
                                            # return x_move, y_move, field, checking_move[1]
            return checks

    def __move_piece(self, old: tuple, new: tuple, piece: Piece):
        self.board[old[1]][old[0]].status[0] = Statuses.NULL
        self.board[old[1]][old[0]].piece = Piece()
        self.board[new[1]][new[0]].status[0] = Statuses.PIECE
        self.board[new[1]][new[0]].piece = piece

    def __add_status(self, fields: tuple, status: Statuses):
        for field in fields:
            self.board[field[1]][field[0]].status.append(status)

    def __remove_status(self, fields: list, status: Statuses):
        for field in fields:
            field.status.remove(status)

    def __clear_statuses(self):
        for row in self.board:
            for field in row:
                field.status = [field.status[0]]

    def __is_attacked_no_king(self, position: tuple, color: str) -> bool:
        if color == "white":
            return Statuses.ATTACKED_BLACK in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_BLACK in self.board[position[1]][position[0]].status
        else:
            return Statuses.ATTACKED_WHITE in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_WHITE in self.board[position[1]][position[0]].status

    def __is_attacked_king(self, position: tuple, color: str) -> bool:
        if color == "white":
            return Statuses.ATTACKED_BLACK_KING in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_BLACK_KING in self.board[position[1]][position[0]].status
        else:
            return Statuses.ATTACKED_WHITE_KING in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_WHITE_KING in self.board[position[1]][position[0]].status

    def __is_defended(self, position: tuple, color: str) -> bool:
        if color == "white":
            return Statuses.DEFENDED_WHITE in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_WHITE_KING in self.board[position[1]][position[0]].status
        else:
            return Statuses.DEFENDED_BLACK in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_BLACK_KING in self.board[position[1]][position[0]].status

    def __has_valid_move(self, king: Piece, field: Field) -> bool:
        for move in king.valid_moves:
            x_move = field.x + move[0]
            y_move = field.y + move[1]
            if not (y_move >= self.BOARD_LENGTH or y_move < 0 or x_move >= self.BOARD_LENGTH or x_move < 0):
                if self.board[y_move][x_move].status[0] == Statuses.NULL:
                    if king.color == "white":
                        if not (Statuses.ATTACKED_BLACK in self.board[y_move][x_move].status
                                or Statuses.ATTACKED_BLACK_KING in self.board[y_move][x_move].status):
                            return True

                    else:
                        if not (Statuses.ATTACKED_WHITE in self.board[y_move][x_move].status
                                or Statuses.ATTACKED_WHITE_KING in self.board[y_move][x_move].status):
                            return True
                else:
                    if self.board[y_move][x_move].piece.color != king.color:
                        color = ''
                        if king.color == "white":
                            color = "black"
                        else:
                            color = "white"
                        if not self.__is_defended((x_move, y_move), color):
                            return True
        return False

    def __find_checkmate(self):
        checks = self.__is_check(self.black_king_position)
        mates = []
        temp_board = deepcopy(self.board)
        for check in checks:
            x_move, y_move = check[0]
            field = check[1]
            checking_move = check[2]
            self.__move_piece((field.x, field.y), (x_move, y_move), field.piece)
            self.__clear_statuses()
            self.__fill_field_statuses()
            new_field = self.board[y_move][x_move]
            if x_move != -1:
                position = (x_move, y_move)
                if not self.__is_attacked_no_king(position, "white"):
                    if self.__is_attacked_king(position, "white"):
                        if self.__is_defended(position, "white"):
                            if not self.__is_move_blocked(new_field.piece, (x_move, y_move), checking_move):
                                king_field = self.board[self.black_king_position[1]][self.black_king_position[0]]
                                king = king_field.piece
                                if not self.__has_valid_move(king, king_field):
                                    mates.append((x_move, y_move, field))
                    else:
                        if not self.__is_move_blocked(new_field.piece, (x_move, y_move), checking_move):
                            king_field = self.board[self.black_king_position[1]][self.black_king_position[0]]
                            king = king_field.piece
                            if not self.__has_valid_move(king, king_field):
                                mates.append((x_move, y_move, field))
            self.board = deepcopy(temp_board)

        return mates

    def print_checkmate(self):
        self.__fill_field_statuses()
        mates = self.__find_checkmate()
        if len(mates) > 0:
            output = 'Bialy moze wygrac\n'
            for mate in mates:
                x_axis, y_axis, field = mate
                x_map = {
                    0: 'a',
                    1: 'b',
                    2: 'c',
                    3: 'd',
                    4: 'e',
                    5: 'f',
                    6: 'g',
                    7: 'h'
                }
                y_map = {
                    0: 8,
                    1: 7,
                    2: 6,
                    3: 5,
                    4: 4,
                    5: 3,
                    6: 2,
                    7: 1
                }
                output += '(' + x_map[field.x] + str(y_map[field.y]) + '-' + x_map[x_axis] + str(y_map[y_axis]) + ')\n'
            return output
        else:
            return "Bialy nie ma mozliwego mata"
