from typing import List, Tuple
from pieces import *
from field import Field
from statuses import Statuses
from copy import deepcopy

BOARD_LENGTH = 8


class Board:
    """
    Class for finding all checkmates in given chessboard
    """
    def __init__(self, matrix: List[List[str]]):
        """
        Creates Board object used for finding all checkmates in one in given chessboard\n
        :param matrix: Input containing matrix of encoded pieces
        """
        self.white_king_position: Tuple[int, int] = (-8, -8)
        self.black_king_position: Tuple[int, int] = (-8, -8)
        self.board = self.__parse_board(matrix)

    def __parse_board(self, matrix: List[List[str]]) -> List[List[Field]]:
        """
        Parses input matrix into list of lists of fields imitating chessboard\n
        :param matrix: Input containing matrix of encoded pieces
        :return: List of lists of fields
        """
        def create_fields(color: str, y: int, x: int) -> dict:
            """
            Creates field dictionary matching code, color and coordinates with pieces\n
            :param color: Color of piece
            :param y: Vertical coordinate (0 starts at top of imaginary chessboard)
            :param x: Horizontal coordinate (0 starts at left of imaginary chessboard)
            :return: Dictionary of string, Field pairs
            """
            return {
                'p': Field(WPawn(), x, y, Statuses.PIECE),
                'r': Field(Rook(color), x, y, Statuses.PIECE),
                'k': Field(Knight(color), x, y, Statuses.PIECE),
                'b': Field(Bishop(color), x, y, Statuses.PIECE),
                'q': Field(Queen(color), x, y, Statuses.PIECE),
                'W': Field(King(color), x, y, Statuses.PIECE)
            }
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
                        fields = create_fields(colors[0], i, j)
                        if piece == 'W':
                            self.white_king_position = (j, i)
                    else:
                        fields = create_fields(colors[1], i, j)
                        fields['p'] = Field(BPawn(), j, i, Statuses.PIECE)
                        if piece == 'W':
                            self.black_king_position = (j, i)
                    board[i].append(fields[piece])
                j += 1
            i += 1
        return board

    def __is_in_board(self, x: int, y: int) -> bool:
        """
        Checks if coordinates fit in board borders\n
        :param x: Horizontal coordinate (0 starts at left of imaginary chessboard)
        :param y: Vertical coordinate (0 starts at top of imaginary chessboard)
        :return: True if x and y fit in board borders else False
        """
        return 0 <= x < BOARD_LENGTH and 0 <= y < BOARD_LENGTH

    def __fill_field_statuses(self) -> None:
        """
        Fills field statuses in board based on possible moves distinguishing attacks and defenses\n
        :return: None
        """
        def fill_statuses_at(move: Tuple[int, int]) -> None:
            """
            Fills statuses based on given move\n
            :param move:
            :return:
            """
            def append_status(x: int, y: int, attacks: List[Statuses], defenses: List[Statuses]) -> None:
                """
                Appends given statuses at given coordinates distinguishing between colors\n
                :param x: Horizontal coordinate (0 starts at left of imaginary chessboard)
                :param y: Vertical coordinate (0 starts at top of imaginary chessboard)
                :param attacks: Attack type statuses
                :param defenses: Defense type statuses
                :return: None
                """
                if self.board[y][x].status[0] != Statuses.NULL:
                    if self.board[y_move][x_move].piece.color == field.piece.color:
                        if field.piece.color == "black":
                            self.board[y_move][x_move].status.append(defenses[1])
                        else:
                            self.board[y_move][x_move].status.append(defenses[0])
                    else:
                        if field.piece.color == "black":
                            self.board[y_move][x_move].status.append(attacks[1])
                        else:
                            self.board[y_move][x_move].status.append(attacks[0])
                else:
                    if field.piece.color == "black":
                        self.board[y_move][x_move].status.append(attacks[1])
                    else:
                        self.board[y_move][x_move].status.append(attacks[0])

            x_move = field.x + move[0]
            y_move = field.y + move[1]
            if self.__is_in_board(x_move, y_move):
                if isinstance(field.piece, King):
                    attacks = [Statuses.ATTACKED_WHITE_KING, Statuses.ATTACKED_BLACK_KING]
                    defenses = [Statuses.DEFENDED_WHITE_KING, Statuses.DEFENDED_BLACK_KING]
                    append_status(x_move, y_move, attacks, defenses)
                else:
                    if not self.__is_move_blocked(field.piece, (field.x, field.y), move):
                        attacks = [Statuses.ATTACKED_WHITE, Statuses.ATTACKED_BLACK]
                        defenses = [Statuses.DEFENDED_WHITE, Statuses.DEFENDED_BLACK]
                        append_status(x_move, y_move, attacks, defenses)

        for row in self.board:
            for field in row:
                if isinstance(field.piece, BPawn) or isinstance(field.piece, WPawn):
                    for move in field.piece.moves:
                        fill_statuses_at(move)
                else:
                    for move in field.piece.valid_moves:
                        fill_statuses_at(move)

    def __is_move_blocked(self, piece: Piece, position: Tuple[int, int], move: Tuple[int, int]) -> bool:
        """
        Checks if move from position is blocked\n
        :param piece: Piece performing move
        :param position: Position of piece
        :param move: Move to check
        :return: True if move is blocked, otherwise False
        """
        if isinstance(piece, Knight):
            return False

        elif isinstance(piece, King):
            new_field = (position[0] + move[0], position[1] + move[1])
            return self.__is_attacked_no_king(new_field, piece.color) or self.__is_attacked_king(new_field, piece.color)

        elif isinstance(piece, WPawn) or isinstance(piece, BPawn):
            return self.__is_pawn_move_blocked(position, move)

        elif isinstance(piece, Rook):
            return self.__is_rook_move_blocked(position, move, piece.color)

        elif isinstance(piece, Bishop):
            return self.__is_bishop_move_blocked(position, move, piece.color)

        elif isinstance(piece, Queen):
            if move[0] == 0 or move[1] == 0:
                return self.__is_rook_move_blocked(position, move, piece.color)
            else:
                return self.__is_bishop_move_blocked(position, move, piece.color)

    def __is_pawn_move_blocked(self, position: Tuple[int, int], move: Tuple[int, int]) -> bool:
        """
        Checks if pawn move from position is blocked\n
        :param position: Position of the pawn
        :param move: Move to check
        :return: True if move is blocked, otherwise False
        """
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

    def __is_rook_move_blocked(self, position: Tuple[int, int], move: Tuple[int, int], color: str) -> bool:
        """
        Checks if rook move from position is blocked\n
        :param position: Position of the rook
        :param move: Move to check
        :param color: Color of the rook
        :return: True if move is blocked, otherwise False
        """
        def is_blocked_at(x: int, y: int) -> bool:
            """
            Checks if rook move is blocked at given coordinates\n
            :param x: Horizontal coordinate (0 starts at left of imaginary chessboard)
            :param y: Vertical coordinate (0 starts at top of imaginary chessboard)
            :return: True if move is blocked, otherwise False
            """
            if not (isinstance(self.board[y][x].piece, King)
                    and self.board[y][x].piece.color != color):
                if self.board[y][x].status[0] == Statuses.PIECE:
                    return True
            return False

        def is_blocked_at_range(coords: range, is_x: bool) -> bool:
            """
            Checks if rook move is blocked at given range of coordinates\n
            :param coords: Range of coordinates
            :param is_x: Defines whether coordinates in interval should be generated as x or y
            :return: True if move is blocked at any generated coordinate, False if is not blocked at all
            """
            if is_x:
                for x in coords:
                    if is_blocked_at(x, position[1]):
                        return True
                return False
            else:
                for y in coords:
                    if is_blocked_at(position[0], y):
                        return True
                return False

        if move[0] == 0:
            if move[1] > 0:
                return is_blocked_at_range(range(position[1] + 1, position[1] + move[1]), False)
            else:
                return is_blocked_at_range(range(position[1] - 1, position[1] + move[1], -1), False)
        else:
            if move[0] > 0:
                return is_blocked_at_range(range(position[0] + 1, position[0] + move[0]), True)
            else:
                return is_blocked_at_range(range(position[0] - 1, position[0] + move[0], -1), True)

    def __generate_bishop_coords(self, move: Tuple[int, int]) -> Tuple[range, range]:
        """
        Generates bishop coords depending on given move
        :param move: Move to be performed by bishop
        :return: Tuple of ranges of coordinates
        """
        if move[0] > 0:
            x = range(1, move[0])
        else:
            x = range(-1, move[0], -1)
        if move[1] > 0:
            y = range(1, move[1])
        else:
            y = range(-1, move[1], -1)
        return x, y

    def __is_bishop_move_blocked(self, position: Tuple[int, int], move: Tuple[int, int], color: str) -> bool:
        """
        Checks if bishop move from position is blocked\n
        :param position: Position of the rook
        :param move: Move to check
        :param color: Color of the rook
        :return: True if move is blocked, otherwise False
        """
        x, y = self.__generate_bishop_coords(move)
        for i, j in zip(x, y):
            if not (isinstance(self.board[position[1] + j][position[0] + i].piece, King)
                    and self.board[position[1] + j][position[0] + i].piece.color != color):
                if self.board[position[1] + j][position[0] + i].status[0] == Statuses.PIECE:
                    return True
        return False

    def __is_move_blockable(self, piece: Piece, position: Tuple[int, int], move: Tuple[int, int]) -> bool:
        """
        Checks whether move is blockable by piece of opposite color
        :param piece: Piece performing move
        :param position: Position from which move is to be performed
        :param move: Move to be performed
        :return: True if move is blockable by any piece of opposite color, otherwise False
        """
        if isinstance(piece, Knight) or isinstance(piece, King) or isinstance(piece, WPawn) or isinstance(piece, BPawn):
            return False
        elif isinstance(piece, Rook):
            return self.__is_rook_move_blockable(position, move, piece.color)
        elif isinstance(piece, Bishop):
            return self.__is_bishop_move_blockable(position, move, piece.color)
        elif isinstance(piece, Queen):
            if move[0] == 0 or move[1] == 0:
                return self.__is_rook_move_blockable(position, move, piece.color)
            else:
                return self.__is_bishop_move_blockable(position, move, piece.color)

    def __is_rook_move_blockable(self, position: Tuple[int, int], move: Tuple[int, int], color: str) -> bool:
        """
        Checks if rook move from position is blockable\n
        :param position: Position of the rook
        :param move: Move to check
        :param color: Color of the rook
        :return: True if move is blockable, otherwise False
        """
        def is_blocked_at(x: int, y: int) -> bool:
            """
            Checks if rook move is blocked at given coordinates\n
            :param x: Horizontal coordinate (0 starts at left of imaginary chessboard)
            :param y: Vertical coordinate (0 starts at top of imaginary chessboard)
            :return: True if move is blockable, otherwise False
            """
            if not (isinstance(self.board[y][x].piece, King)
                    and self.board[y][x].piece.color != color):
                if color == "black":
                    if Statuses.ATTACKED_WHITE in self.board[y][x].status:
                        return True
                else:
                    if Statuses.ATTACKED_BLACK in self.board[y][x].status:
                        return True
            return False

        def is_blocked_at_range(coords: range, is_x: bool) -> bool:
            """
            Checks if rook move is blocked at given range of coordinates\n
            :param coords: Range of coordinates
            :param is_x: Defines whether coordinates in interval should be generated as x or y
            :return: True if move is blockable at any generated coordinate, otherwise not
            """
            if is_x:
                for x in coords:
                    if is_blocked_at(x, position[1]):
                        return True
                return False
            else:
                for y in coords:
                    if is_blocked_at(position[0], y):
                        return True
                return False

        if move[0] == 0:
            if move[1] > 0:
                return is_blocked_at_range(range(position[1] + 1, position[1] + move[1]), False)
            else:
                return is_blocked_at_range(range(position[1] - 1, position[1] + move[1], -1), False)
        else:
            if move[0] > 0:
                return is_blocked_at_range(range(position[0] + 1, position[0] + move[0]), True)
            else:
                return is_blocked_at_range(range(position[0] - 1, position[0] + move[0], -1), True)

    def __is_bishop_move_blockable(self, position: Tuple[int, int], move: Tuple[int, int], color: str) -> bool:
        """
        Checks if bishop move from position is blockable\n
        :param position: Position of the rook
        :param move: Move to check
        :param color: Color of the rook
        :return: True if move is blockable, otherwise False
        """
        x, y = self.__generate_bishop_coords(move)
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

    def __get_checks(self) -> List[Tuple[Tuple[int, int], Field, Tuple[int, int]]]:
        """
        Returns all possible checks on current chessboard state
        :return: List of tuples of move, field and checking move
        """
        checks = []

        def is_check_after_move(piece: Piece, position: Tuple[int, int]) -> Tuple[bool, Tuple[int, int]]:
            """
            Checks whether there is any possible check after move
            :param piece: Piece performing move
            :param position: Position of the piece
            :return: True and move which results in check if there is any, False and (0, 0) if not
            """
            def check_move(move: Tuple[int, int]) -> Tuple[bool, Tuple[int, int]]:
                """
                Checks if given move results in check
                :param move: Move with possibility of checking
                :return: True and move which results in check if there is any, False and (0, 0) if not
                """
                x_move = position[0] + move[0]
                y_move = position[1] + move[1]
                if self.__is_in_board(x_move, y_move):
                    if not self.__is_move_blocked(piece, position, move):
                        if piece.color != self.board[y_move][x_move].piece.color:
                            if isinstance(self.board[y_move][x_move].piece, King):
                                return True, move
                return False, (0, 0)

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

            return False, (0, 0)

        def find_check(move: Tuple[int, int]) -> None:
            """
            Searches for possibilities of checks after given move
            :param move: Move to check in terms of possibility of finding checks
            :return: None
            """
            x_move = field.x + move[0]
            y_move = field.y + move[1]
            if self.__is_in_board(x_move, y_move):
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

    def __move_piece(self, old: Tuple[int, int], new: Tuple[int, int], piece: Piece) -> None:
        """
        Moves piece from old to new position
        :param old: Position to be moved from
        :param new: Position to be moved to
        :param piece: Piece to be moved
        :return: None
        """
        self.board[old[1]][old[0]].status[0] = Statuses.NULL
        self.board[old[1]][old[0]].piece = Piece()
        self.board[new[1]][new[0]].status[0] = Statuses.PIECE
        self.board[new[1]][new[0]].piece = piece

    def __clear_statuses(self) -> None:
        """
        Clears statuses of all fields besides first
        :return: None
        """
        for row in self.board:
            for field in row:
                field.status = [field.status[0]]

    def __is_attacked_no_king(self, position: Tuple[int, int], color: str) -> bool:
        """
        Checks whether position is attacked by any piece but not king
        :param position: Position to check
        :param color: Color of piece on position
        :return: True if position is attacked
        """
        if color == "white":
            return Statuses.ATTACKED_BLACK in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_BLACK in self.board[position[1]][position[0]].status
        else:
            return Statuses.ATTACKED_WHITE in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_WHITE in self.board[position[1]][position[0]].status

    def __is_attacked_king(self, position: Tuple[int, int], color: str) -> bool:
        """
        Checks whether position is attacked by king of opposite color
        :param position: Position to check
        :param color: Color of piece on position
        :return: True if position is attacked
        """
        if color == "white":
            return Statuses.ATTACKED_BLACK_KING in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_BLACK_KING in self.board[position[1]][position[0]].status
        else:
            return Statuses.ATTACKED_WHITE_KING in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_WHITE_KING in self.board[position[1]][position[0]].status

    def __is_defended(self, position: Tuple[int, int], color: str) -> bool:
        """
        Checks whether position is defended by piece of the same color
        :param position: Position to check
        :param color: Color of piece on position
        :return: True if position is attacked
        """
        if color == "white":
            return Statuses.DEFENDED_WHITE in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_WHITE_KING in self.board[position[1]][position[0]].status
        else:
            return Statuses.DEFENDED_BLACK in self.board[position[1]][position[0]].status \
                   or Statuses.DEFENDED_BLACK_KING in self.board[position[1]][position[0]].status

    def __has_valid_move(self, king: Piece, field: Field, temp_king_position: Tuple[int, int]) -> bool:
        """
        Checks whether king has valid move
        :param king: King which will be checked
        :param field: Field of king
        :param temp_king_position: Original position of king
        :return: True if king has valid move
        """
        temp = deepcopy(self.board)
        for move in king.valid_moves:
            x_move = field.x + move[0]
            y_move = field.y + move[1]
            if self.__is_in_board(x_move, y_move):
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

    def __find_checkmate(self) -> Tuple[List[Tuple[int, int, Field]], str]:
        """
        Finds all possible checkmates in one for white or for black if there are no checkmates for white
        :return: Tuple of list of tuples of checkmating moves and color of checkmating piece
        """
        def check_checks(checks: Tuple[Tuple[Tuple[int, int], Field, Tuple[int, int]]], color: str) -> None:
            """
            Checks whether given checks are checkmates
            :param checks: Possible checkmates
            :param color: Color of checking pieces
            :return: None
            """
            def append_possible_checkmates(piece: Piece, position: Tuple[int, int], move) -> None:
                """
                Appends move to list if it results in checkmate
                :param piece: Piece performing check
                :param position: Position of check
                :param move: Move attacking king's field
                :return: None
                """
                if not self.__is_move_blockable(piece, position, move):
                    if color == "white":
                        king_field = self.board[self.black_king_position[1]][
                            self.black_king_position[0]]
                    else:
                        king_field = self.board[self.white_king_position[1]][
                            self.white_king_position[0]]
                    king = king_field.piece
                    if not self.__has_valid_move(king, king_field, temp_king_position):
                        mates.append((x_move, y_move, field))

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
                                append_possible_checkmates(new_field.piece, (x_move, y_move), checking_move)
                        else:
                            append_possible_checkmates(new_field.piece, (x_move, y_move), checking_move)
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

    def print_checkmate(self) -> str:
        """
        Creates string containing possible checkmates
        :return: Output string
        """
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
            return "There is no checkmate"
