from typing import List
from pieces import *
from field import Field
from statuses import Statuses
from copy import deepcopy

BOARD_LENGTH = 8


class Board:
    def __init__(self, matrix: List[List[str]]):
        self.white_king_position: tuple = ()
        self.black_king_position: tuple = ()
        self.board = self.__parse_board(matrix)

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
        def fill_statuses_at(move: tuple) -> None:
            x_move = field.x + move[0]
            y_move = field.y + move[1]
            if not (y_move >= BOARD_LENGTH or y_move < 0 or x_move >= BOARD_LENGTH or x_move < 0):
                if isinstance(field.piece, King):
                    if self.board[y_move][x_move].status[0] != Statuses.NULL:
                        if self.board[y_move][x_move].piece.color == field.piece.color:
                            if field.piece.color == "black":
                                self.board[y_move][x_move].status.append(Statuses.DEFENDED_BLACK_KING)
                            else:
                                self.board[y_move][x_move].status.append(Statuses.DEFENDED_WHITE_KING)
                        else:
                            if field.piece.color == "black":
                                self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK_KING)
                            else:
                                self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE_KING)
                    else:
                        if field.piece.color == "black":
                            self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK_KING)
                        else:
                            self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE_KING)
                else:
                    if not self.__is_move_blocked(field.piece, (field.x, field.y), move):
                        if self.board[y_move][x_move].status[0] != Statuses.NULL:
                            if self.board[y_move][x_move].piece.color == field.piece.color:
                                if field.piece.color == "black":
                                    self.board[y_move][x_move].status.append(Statuses.DEFENDED_BLACK)
                                else:
                                    self.board[y_move][x_move].status.append(Statuses.DEFENDED_WHITE)
                            else:
                                if field.piece.color == "black":
                                    self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK)
                                else:
                                    self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE)
                        else:
                            if field.piece.color == "black":
                                self.board[y_move][x_move].status.append(Statuses.ATTACKED_BLACK)
                            else:
                                self.board[y_move][x_move].status.append(Statuses.ATTACKED_WHITE)

        for row in self.board:
            for field in row:
                if not (isinstance(field.piece, BPawn) or isinstance(field.piece, WPawn)):
                    for move in field.piece.valid_moves:
                        fill_statuses_at(move)
                else:
                    for move in field.piece.moves:
                        fill_statuses_at(move)

    def __is_move_blocked(self, piece: Piece, position: tuple, move: tuple) -> bool:
        if isinstance(piece, Knight):
            return False
        elif isinstance(piece, King):
            new_field = (position[0] + move[0], position[1] + move[1])
            return self.__is_attacked_no_king(new_field, piece.color) or self.__is_attacked_king(new_field, piece.color)
        elif isinstance(piece, WPawn) or isinstance(piece, BPawn):
            if move[0] == 0:
                if move[1] == 2 and position[1] == 1:
                    return self.board[position[1] + move[1]][position[0] + move[0]].status[0] == Statuses.PIECE
                if move[1] == -2 and position[1] == 6:
                    return self.board[position[1] + move[1]][position[0] + move[0]].status[0] == Statuses.PIECE
                if not (move[1] == 2 or move[1] == -2):
                    return self.board[position[1] + move[1]][position[0] + move[0]].status[0] == Statuses.PIECE
                return True
            else:
                return self.board[position[1] + move[1]][position[0] + move[0]].status[0] == Statuses.NULL
        elif isinstance(piece, Rook):
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

    def __is_move_blockable(self, piece: Piece, position: tuple, move: tuple) -> bool:
        if isinstance(piece, Knight) or isinstance(piece, King) or isinstance(piece, WPawn) or isinstance(piece, BPawn):
            return False
        else:
            if isinstance(piece, Rook):
                return self.__is_rook_move_blockable(position, move, piece.color)
            elif isinstance(piece, Bishop):
                return self.__is_bishop_move_blockable(position, move, piece.color)
            elif isinstance(piece, Queen):
                if move[0] == 0 or move[1] == 0:
                    return self.__is_rook_move_blockable(position, move, piece.color)
                else:
                    return self.__is_bishop_move_blockable(position, move, piece.color)

    def __is_rook_move_blockable(self, position: tuple, move: tuple, color: str) -> bool:
        if move[0] == 0:
            if move[1] > 0:
                for y in range(position[1] + 1, position[1] + move[1]):
                    if not (isinstance(self.board[y][position[0]].piece, King)
                            and self.board[y][position[0]].piece.color != color):
                        if color == "black":
                            if Statuses.ATTACKED_WHITE in self.board[y][position[0]].status:
                                return True
                        else:
                            if Statuses.ATTACKED_BLACK in self.board[y][position[0]].status:
                                return True
                return False
            else:
                for y in range(position[1] - 1, position[1] + move[1], -1):
                    if not (isinstance(self.board[y][position[0]].piece, King)
                            and self.board[y][position[0]].piece.color != color):
                        if color == "black":
                            if Statuses.ATTACKED_WHITE in self.board[y][position[0]].status:
                                return True
                        else:
                            if Statuses.ATTACKED_BLACK in self.board[y][position[0]].status:
                                return True
                return False
        else:
            if move[0] > 0:
                for x in range(position[0] + 1, position[0] + move[0]):
                    if not (isinstance(self.board[position[1]][x].piece, King)
                            and self.board[position[1]][x].piece.color != color):
                        if color == "black":
                            if Statuses.ATTACKED_WHITE in self.board[position[1]][x].status:
                                return True
                        else:
                            if Statuses.ATTACKED_BLACK in self.board[position[1]][x].status:
                                return True
                return False
            else:
                for x in range(position[0] - 1, position[0] + move[0], -1):
                    if not (isinstance(self.board[position[1]][x].piece, King)
                            and self.board[position[1]][x].piece.color != color):
                        if color == "black":
                            if Statuses.ATTACKED_WHITE in self.board[position[1]][x].status:
                                return True
                        else:
                            if Statuses.ATTACKED_BLACK in self.board[position[1]][x].status:
                                return True
                return False

    def __is_bishop_move_blockable(self, position: tuple, move: tuple, color: str) -> bool:
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
                if color == "black":
                    if Statuses.ATTACKED_WHITE in self.board[position[1] + j][position[0] + i].status:
                        return True
                else:
                    if Statuses.ATTACKED_BLACK in self.board[position[1] + j][position[0] + i].status:
                        return True
                return True
        return False

    def __get_checks(self) -> list:
        checks = []

        # TODO: ruch o 2 pionkiem
        def is_check_after_move(piece: Piece, position: tuple) -> tuple:
            def check_move(move: tuple) -> tuple:
                x_move = position[0] + move[0]
                y_move = position[1] + move[1]
                if not (y_move >= BOARD_LENGTH or y_move < 0 or x_move >= BOARD_LENGTH or x_move < 0):
                    if not self.__is_move_blocked(piece, position, move):
                        if piece.color != self.board[y_move][x_move].piece.color:
                            if isinstance(self.board[y_move][x_move].piece, King):
                                return True, move
                return False, None

            if not (isinstance(field.piece, BPawn) or isinstance(field.piece, WPawn)):
                for move in field.piece.valid_moves:
                    checking_move = check_move(move)
                    if checking_move[0]:
                        return checking_move
            else:
                for move in field.piece.moves:
                    checking_move = check_move(move)
                    if checking_move[0]:
                        return checking_move

            return False, None

        def find_check(move: tuple):
            x_move = field.x + move[0]
            y_move = field.y + move[1]
            if not (y_move >= BOARD_LENGTH or y_move < 0
                    or x_move >= BOARD_LENGTH or x_move < 0):
                if not self.__is_move_blocked(field.piece, (field.x, field.y), move):
                    if self.board[y_move][x_move].piece.color != field.piece.color:
                        checking_move = is_check_after_move(field.piece, (x_move, y_move))
                        if checking_move[0]:
                            initial_move = (x_move, y_move)
                            checks.append((initial_move, field, checking_move[1]))

        for row in self.board:
            for field in row:
                for move in field.piece.valid_moves:
                    find_check(move)
                if isinstance(field.piece, BPawn) or isinstance(field.piece, WPawn):
                    for move in field.piece.moves:
                        find_check(move)
        return checks

    def __move_piece(self, old: tuple, new: tuple, piece: Piece):
        self.board[old[1]][old[0]].status[0] = Statuses.NULL
        self.board[old[1]][old[0]].piece = Piece()
        self.board[new[1]][new[0]].status[0] = Statuses.PIECE
        self.board[new[1]][new[0]].piece = piece

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

    def __has_valid_move(self, king: Piece, field: Field, temp_king_position: tuple) -> bool:
        temp = deepcopy(self.board)
        for move in king.valid_moves:
            x_move = field.x + move[0]
            y_move = field.y + move[1]
            if not (y_move >= BOARD_LENGTH or y_move < 0 or x_move >= BOARD_LENGTH or x_move < 0):
                if self.board[y_move][x_move].status[0] == Statuses.NULL:
                    self.__move_piece((field.x, field.y), (x_move, y_move), field.piece)
                    if king.color == "white":
                        self.white_king_position = (x_move, y_move)
                    else:
                        self.black_king_position = (x_move, y_move)
                    self.__clear_statuses()
                    self.__fill_field_statuses()
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
            if king.color == "white":
                self.white_king_position = temp_king_position
            else:
                self.black_king_position = temp_king_position
            self.board = deepcopy(temp)
        return False

    def __find_checkmate(self):
        def check_checks(checks: tuple, color: str):
            if color == "white":
                temp_king_position = self.black_king_position
            else:
                temp_king_position = self.white_king_position
            for check in checks:
                x_move, y_move = check[0]
                field = self.board[check[1].y][check[1].x]
                checking_move = check[2]
                self.__move_piece((field.x, field.y), (x_move, y_move), field.piece)
                self.__clear_statuses()
                self.__fill_field_statuses()
                new_field = self.board[y_move][x_move]
                if x_move != -1:
                    position = (x_move, y_move)
                    if not self.__is_attacked_no_king(position, color):
                        if self.__is_attacked_king(position, color):
                            if self.__is_defended(position, color):
                                if not self.__is_move_blockable(new_field.piece, (x_move, y_move), checking_move):
                                    if color == "white":
                                        king_field = self.board[self.black_king_position[1]][
                                            self.black_king_position[0]]

                                    else:
                                        king_field = self.board[self.white_king_position[1]][
                                            self.white_king_position[0]]

                                    king = king_field.piece
                                    if not self.__has_valid_move(king, king_field, temp_king_position):
                                        mates.append((x_move, y_move, field))
                        else:
                            if not self.__is_move_blockable(new_field.piece, (x_move, y_move), checking_move):
                                if color == "white":
                                    king_field = self.board[self.black_king_position[1]][self.black_king_position[0]]
                                else:
                                    king_field = self.board[self.white_king_position[1]][self.white_king_position[0]]
                                king = king_field.piece
                                if not self.__has_valid_move(king, king_field, temp_king_position):
                                    mates.append((x_move, y_move, field))
                if color == "white":
                    self.black_king_position = temp_king_position
                else:
                    self.white_king_position = temp_king_position
                self.board = deepcopy(temp_board)

        checks = self.__get_checks()
        white_checks = tuple(filter(lambda check: check[1].piece.color == "white", checks))
        black_checks = tuple(filter(lambda check: check[1].piece.color == "black", checks))
        mates = []
        temp_board = deepcopy(self.board)
        color = "white"
        check_checks(white_checks, color)
        if len(mates) == 0:
            color = "black"
            check_checks(black_checks, color)

        return mates, color

    def print_checkmate(self):
        self.__fill_field_statuses()
        mates, color = self.__find_checkmate()
        if len(mates) > 0:
            output = color + ' can win\n'
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
            return "Nie ma mozliwego mata"
