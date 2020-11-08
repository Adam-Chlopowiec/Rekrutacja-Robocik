from pieces import Piece
from statuses import Statuses


class Field:
    def __init__(self, piece: Piece, x: int, y: int, status: Statuses):
        self.piece = piece
        self.status = [status]
        self.x = x
        self.y = y
