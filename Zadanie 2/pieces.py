from typing import List, Tuple


def generate_bishop_moves() -> List[Tuple[int, int]]:
    """
    Generates list of diagonal moves\n
    :return: Returns list of paired integer tuples
    """
    ascending_diagonal = list(range(-7, 8))
    ascending_diagonal.remove(0)
    descending_diagonal = list(range(7, -8, -1))
    descending_diagonal.remove(0)
    moves = []
    for i in ascending_diagonal:
        moves.append((i, i))
    for i, j in zip(ascending_diagonal, descending_diagonal):
        moves.append((i, j))
    return moves


def generate_rook_moves() -> List[Tuple[int, int]]:
    """
    Generates list of vertical and horizontal moves\n
    :return: Returns list of paired integer tuples
    """
    distances = list(range(-7, 8))
    distances.remove(0)
    x_moves = [(distance, 0) for distance in distances]
    y_moves = [(0, distance) for distance in distances]
    x_moves.extend(y_moves)
    return x_moves


class Piece:
    """
    Most general piece, parent to every other. Added to empty fields.
    """
    def __init__(self):
        self.valid_moves: tuple = ()
        self.color: str = ''


class King(Piece):
    def __init__(self, color: str):
        super().__init__()
        self.valid_moves = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        self.color = color


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__()
        bishop_moves = generate_bishop_moves()
        rook_moves = generate_rook_moves()
        bishop_moves.extend(rook_moves)
        self.valid_moves = tuple(bishop_moves)
        self.color = color


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__()
        self.valid_moves = tuple(generate_rook_moves())
        self.color = color


class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__()
        self.valid_moves = tuple(generate_bishop_moves())
        self.color = color


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__()
        self.valid_moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2))
        self.color = color


class WPawn(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((0, -1), (0, -2))
        self.moves: tuple = ((1, -1), (-1, -1))
        self.color = "white"


class BPawn(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((0, 1), (0, 2))
        self.moves: tuple = ((1, 1), (-1, 1))
        self.color = "black"
