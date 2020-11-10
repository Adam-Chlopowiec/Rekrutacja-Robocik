from pieces import Piece
from statuses import Statuses


class Field:
    def __init__(self, piece: Piece, x: int, y: int, status: Statuses):
        """
        Creates field object for chessboard\n
        :param piece: Piece to be put in the field
        :param x: Horizontal coordinate (0 starts at left of imaginary chessboard)
        :param y: Vertical coordinate (0 starts at top of imaginary chessboard)
        :param status: initial status of the field
        """
        self.piece = piece
        self.status: list = [status]
        self.x = x
        self.y = y
