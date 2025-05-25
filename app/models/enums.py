from enum import IntEnum

class MatchStatus(IntEnum):
    NOT_MATCH = -1
    UNKNOWN = 0
    MATCH_USER1 = 1
    MATCH_USER2 = 2
    MATCH = 3
    END_MATCH = 4