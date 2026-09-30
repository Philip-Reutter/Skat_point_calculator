from src.logic.skat_calculator import calculate_score

def test_grand_hand_won():
    score = calculate_score(
        game_type="Grand",
        jacks=2,
        hand=True,
        schneider_announced=False,
        schneider=False,
        schwarz_announced=False,
        schwarz=False,
        ouvert=False,
        kontra=False,
        re=False,
        won=True
    )
    assert score == 96
    print("Grand hand won:", score)

def test_grand_hand_lost():
    score = calculate_score(
        game_type="Grand",
        jacks=2,
        hand=True,
        schneider_announced=False,
        schneider=False,
        schwarz_announced=False,
        schwarz=False,
        ouvert=False,
        kontra=False,
        re=False,
        won=False
    )
    assert score == -96
    print("Grand hand lost:", score)

def test_null_ouvert_won():
    score = calculate_score(
        game_type="Null",
        jacks=0,
        hand=False,
        schneider_announced=False,
        schneider=False,
        schwarz_announced=False,
        schwarz=False,
        ouvert=True,
        kontra=False,
        re=False,
        won=True
    )
    assert score == 46
    print("Null ouvert won:", score)

def test_null_ouvert_lost():
    score = calculate_score(
        game_type="Null",
        jacks=0,
        hand=False,
        schneider_announced=False,
        schneider=False,
        schwarz_announced=False,
        schwarz=False,
        ouvert=True,
        kontra=False,
        re=False,
        won=False
    )
    assert score == -92
    print("Null ouvert lost:", score)
