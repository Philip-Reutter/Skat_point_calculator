from .base_values import GAME_BASE_VALUES, NULL_BASE_VALUES

def calculate_score(
    game_type: str,
    jacks: int,
    hand: bool,
    schneider_announced: bool,
    schneider: bool,
    schwarz_announced: bool,
    schwarz: bool,
    ouvert: bool,
    kontra: bool,
    re: bool,
    won: bool
) -> int:
    """
    Calculates points for a game of Skat based on provided parameters.
    """
    if game_type == "Null":
        if hand and ouvert:
            score = NULL_BASE_VALUES["Null_hand_ouvert"]
        elif ouvert:
            score = NULL_BASE_VALUES["Null_ouvert"]
        elif hand: 
            score = NULL_BASE_VALUES["Null_hand"]
        else:
            score = NULL_BASE_VALUES["Null"]
    else:
        multiplier = jacks + 1 + sum([hand, schneider_announced, schneider, schwarz_announced, schwarz, ouvert])
        if kontra:
            multiplier *= 2
        if re:
            multiplier *= 2
        score = multiplier * GAME_BASE_VALUES[game_type]
    if not won:
        if hand:
            score *= -1
        else:
            score *= -2
    return score
