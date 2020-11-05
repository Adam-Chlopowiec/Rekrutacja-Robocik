def generate_diagonals():
    ascending_diagonal = list(range(-7, 0))
    ascending_diagonal.append(range(1, 8))
    descending_diagonal = list(range(7, 0, -1))
    descending_diagonal.append(range(-1, -8, -1))
    return ascending_diagonal, descending_diagonal


def generate_rook_moves():
    distances = list(range(-7, 0))
    distances.append(range(1, 8))
    x_moves = [(distance, 0) for distance in distances]
    y_moves = [(0, distance) for distance in distances]
    return x_moves, y_moves


class Piece:
    def __init__(self):
        self.valid_moves = ()
        self.color = ''
        self.is_null = True


class King(Piece):
    def __init__(self, color: str):
        super().__init__()
        self.valid_moves = ((-1, -1), (-1, 0), (-1, 1), (1, 0), (1, 1), (1, 0), (1, -1))
        self.color = color
        self.is_null = False


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__()
        ascending_diagonal, descending_diagonal = generate_diagonals()
        x_moves, y_moves = generate_rook_moves()
        self.valid_moves = (zip(ascending_diagonal, ascending_diagonal), zip(descending_diagonal, ascending_diagonal),
                            (move for move in x_moves), (move for move in y_moves))
        self.color = color
        self.is_null = False


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__()
        x_moves, y_moves = generate_rook_moves()
        self.valid_moves = ((move for move in x_moves), (move for move in y_moves))
        self.color = color
        self.is_null = False


class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__()
        ascending_diagonal, descending_diagonal = generate_diagonals()
        self.valid_moves = (zip(ascending_diagonal, ascending_diagonal), zip(descending_diagonal, ascending_diagonal))
        self.color = color
        self.is_null = False


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__()
        self.valid_moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2))
        self.color = color
        self.is_null = False


class WPawn(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((0, 1), (0, 2))
        self.attack_moves = ((1, 1), (-1, 1))
        self.color = "white"
        self.is_null = False


class BPawn(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((0, -1), (0, -2))
        self.attack_moves = ((1, -1), (-1, -1))
        self.color = "black"
        self.is_null = False
