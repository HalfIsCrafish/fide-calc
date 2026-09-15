import math
from app.engine.models import Game, Opponent

def unique_foreign_federations(games: list[Game], applicant_federation: str) -> int:
    """Function to count the number of unique foreign federations. 1.4.3 'At least two federations other than that of the title applicant must be included'."""
    
    foreign_federations: list[str] = []
    for game in games:
        if game.opponent is not None:
            federation = game.opponent.federation
            if federation != applicant_federation and federation != "FID": # 1.4.2 'Players with federation “FID” are accepted, but do not count as a foreign player.'
                if federation not in foreign_federations:
                    foreign_federations.append(federation)
    return len(foreign_federations)

def own_federation_opponents(games: list[Game], applicant_federation: str) -> int:
    """Function to count the number of opponents from the same federation. 1.4.4 maximum 3/5 games can be played against opponents from the same federation)."""

    count = 0
    for game in games:
        if game.opponent is not None:
            federation = game.opponent.federation
            if federation == applicant_federation:
                count += 1
    return count

def largest_foreign_federation_opponents(games: list[Game], applicant_federation: str) -> int:
    """Function to count the number of unique foreign federations. 1.4.4 'maximum of 2/3 of the opponents from one federation'."""

    counts: dict[str, int] = {}
    for game in games:
        if game.opponent is not None:
            federation = game.opponent.federation
            if federation != applicant_federation: # We don't give ...!=FID here because it's neutral.
                if federation in counts:
                    counts[federation] += 1
                else:
                    counts[federation] = 1

    max_count = 0
    for federation in counts:
        count = counts[federation]
        if count > max_count:
            max_count = count

    return max_count

def validate_federation_requirements(games: list[Game], applicant_federation: str) -> bool:
    """Function to validate general federation rules from 1.4.3 and 1.4.4."""

    total_games = 0
    for game in games:
        if game.opponent is not None:
            total_games += 1

    if total_games == 0:
        return False

    if unique_foreign_federations(games, applicant_federation) < 2:
        return False

    own_limit = math.floor(total_games * 3 / 5)
    if own_federation_opponents(games, applicant_federation) > own_limit:
        return False

    single_foreign_limit = math.ceil(total_games * 2 / 3)
    if largest_foreign_federation_opponents(games, applicant_federation) > single_foreign_limit:
        return False

    return True