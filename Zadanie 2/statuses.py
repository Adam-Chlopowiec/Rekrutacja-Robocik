from enum import Enum


class Statuses(Enum):
    """
    Statuses mark fields on board
    """
    NULL = 0
    PIECE = 1
    ATTACKED_WHITE = 2
    ATTACKED_WHITE_KING = 3
    DEFENDED_WHITE = 4
    DEFENDED_WHITE_KING = 5
    ATTACKED_BLACK = 6
    ATTACKED_BLACK_KING = 7
    DEFENDED_BLACK = 8
    DEFENDED_BLACK_KING = 9
