import math
from app.engine.calculator import filter_played_games
from app.engine.models import Game

def unique_foreign_federations(games: list[Game], applicant_federation: str) -> int:
    """Function to count the number of unique foreign federations. 1.4.3 'At least two federations other than that of the title applicant must be included'."""
    
    foreign_federations: set[str] = set()
    for game in games:
        fed = game.opponent.federation
        if fed != applicant_federation and fed != "FID":
            foreign_federations.add(fed)
    return len(foreign_federations)

def own_federation_opponents(games: list[Game], applicant_federation: str) -> int:
    """Function to count the number of opponents from the same federation. 1.4.4 maximum 3/5 games can be played against opponents from the same federation)."""

    count = 0
    for game in games:
        if game.opponent.federation == applicant_federation:
            count += 1
    return count

def largest_foreign_federation_opponents(games: list[Game], applicant_federation: str) -> int:
    """Function to count the number of unique foreign federations. 1.4.4 'maximum of 2/3 of the opponents from one federation'."""

    counts: dict[str, int] = {}
    for game in games:
        fed = game.opponent.federation
        if fed != applicant_federation:
            counts[fed] = counts.get(fed, 0) + 1

    return max(counts.values(), default=0)

def validate_federation_requirements(games: list[Game], applicant_federation: str) -> bool:
    """Function to validate general federation rules from 1.4.3 and 1.4.4."""

    played_games = filter_played_games(games)
    total_played_games = len(played_games)

    if total_played_games == 0:
        return False

    if unique_foreign_federations(played_games, applicant_federation) < 2:
        return False

    own_limit = math.floor(total_played_games * 3 / 5)
    if own_federation_opponents(played_games, applicant_federation) > own_limit:
        return False

    single_foreign_limit = math.ceil(total_played_games * 2 / 3)
    if largest_foreign_federation_opponents(played_games, applicant_federation) > single_foreign_limit:
        return False

    return True