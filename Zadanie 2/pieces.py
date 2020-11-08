def generate_bishop_moves():
    ascending_diagonal = list(range(-7, 0))
    ascending_diagonal.extend(list(range(1, 8)))
    descending_diagonal = list(range(7, 0, -1))
    descending_diagonal.extend(list(range(-1, -8, -1)))
    moves = []
    for i, j in zip(ascending_diagonal, ascending_diagonal):
        moves.append((i, j))
    for i, j in zip(ascending_diagonal, descending_diagonal):
        moves.append((i, j))
    return moves


def generate_rook_moves():
    distances = list(range(-7, 0))
    distances.extend(list(range(1, 8)))
    x_moves = [(distance, 0) for distance in distances]
    y_moves = [(0, distance) for distance in distances]
    x_moves.extend(y_moves)
    moves = x_moves
    return moves


class Piece:
    def __init__(self):
        self.valid_moves = ()
        self.attacked_fields = []
        self.defended_fields = []
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
        bishop_moves = generate_bishop_moves()
        rook_moves = generate_rook_moves()
        bishop_moves.extend(rook_moves)
        moves = bishop_moves
        self.valid_moves = tuple(moves)
        self.color = color
        self.is_null = False


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__()
        moves = generate_rook_moves()
        self.valid_moves = tuple(moves)
        self.color = color
        self.is_null = False


class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__()
        moves = generate_bishop_moves()
        self.valid_moves = tuple(moves)
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
        self.valid_moves = ((1, 1), (-1, 1))
        self.moves = ((0, 1), (0, 2))
        self.color = "white"
        self.is_null = False


class BPawn(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((1, -1), (-1, -1))
        self.moves = ((0, -1), (0, -2))
        self.color = "black"
        self.is_null = False
