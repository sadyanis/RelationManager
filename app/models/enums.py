from enum import IntEnum

class MatchStatus(IntEnum):
    NOT_MATCH = -1 # un des utilisateur n'a pas souhaité de relation
    UNKNOWN = 0 # l n’y a pas encore d’information concernant la relation
    MATCH_USER1 = 1 # signifie que l’utilisateur 1 a matché avec l’utilisateur 2, mais que ce dernier n’a pas encore matché
    MATCH_USER2 = 2 # même principe 
    MATCH = 3 # les deux utilisateurs sont entrés en relation
    END_MATCH = 4 # signifie un des users a mis fin au match