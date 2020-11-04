class Piece:
    def __init__(self):
        self.valid_moves = None


class King(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((-1, -1), (-1, 0), (-1, 1), (1, 0), (1, 1), (1, 0), (1, -1))


class Queen(Piece):
    def __init__(self):
        super().__init__()
        positive_diagonal = range(-7, 7)
        negative_diagonal = range(7, -7)
        y = range(-7, 7)
        distances = range(-7, 7)
        x_moves = [(distance, 0) for distance in distances]
        y_moves = [(0, distance) for distance in distances]
        self.valid_moves = (zip(positive_diagonal, y), zip(negative_diagonal, y),
                            (move for move in x_moves),(move for move in y_moves))


class Rook(Piece):
    def __init__(self):
        super().__init__()
        distances = range(-7, 7)
        x_moves = [(distance, 0) for distance in distances]
        y_moves = [(0, distance) for distance in distances]
        self.valid_moves = ((move for move in x_moves), (move for move in y_moves))


class Bishop(Piece):
    def __init__(self):
        super().__init__()
        positive_diagonal = range(-7, 7)
        negative_diagonal = range(7, -7)
        y = range(-7, 7)
        self.valid_moves = (zip(positive_diagonal, y), zip(negative_diagonal, y))


class Knight(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2))


class WPawn(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((0, 1), (0, 2))


class BPawn(Piece):
    def __init__(self):
        super().__init__()
        self.valid_moves = ((0, -1), (0, -2))

