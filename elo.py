K_FACTOR = 10

def get_expected_rating(A, B):
    expected = 1 / (10**((B - A)/400)+1)
    return expected


def get_new_ratings(winner_elo, loser_elo):
    winner_expected = get_expected_rating(winner_elo, loser_elo)
    loser_expected = get_expected_rating(loser_elo, winner_elo)

    winner_new = winner_elo + K_FACTOR * (1 - winner_expected)
    loser_new = loser_elo + K_FACTOR * (0 - loser_expected)

    return winner_new, loser_new