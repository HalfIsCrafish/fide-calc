import math
from app.engine.calculator import filter_played_games
from app.engine.models import Game
from app.engine.tables import HANDBOOK_TITLES, REQUIRED_TITLES_TABLE

def titled_opponent(games: list[Game]) -> int:
    """Function to check how many games were played against opponents with title. 
    1.4.5a 'At least 50% of the opponents shall be title-holders (TH) as in 0.3, excluding CM and WCM.'."""

    count = 0
    for game in games:
        if game.opponent.title in HANDBOOK_TITLES: # check if the opponent has a title
            count += 1 
    return count

def required_titled_opponent(games: list[Game], target_title: str) -> int:
    """Function to check how many games were played against opponents with the required title.
    1.4.5b-e    'For a GM norm at least 1/3 with a minimum 3 of the opponents must be GMs.'
                'For an IM norm at least 1/3 with a minimum 3 of the opponents must be IMs or GMs.
                'For a WGM norm at least 1/3 with a minimum 3 of the opponents must be WGMs, IMs or GMs.'
                'For a WIM norm at least 1/3 with a minimum 3 of the opponents must be WIMs, WGMs, IMs or GMs.'"""

    valid_titles = REQUIRED_TITLES_TABLE.get(target_title, set())
    count = 0
    for game in games:
        if game.opponent.title in valid_titles:
            count += 1
    return count

def validate_title_requirements(games: list[Game], target_title: str) -> bool:
    """Function to validate if the title requirements are met based on the games played and the target title."""

    played_games = filter_played_games(games)
    total_played_games = len(played_games)

    if total_played_games == 0:
        return False

    min_titled = math.ceil(total_played_games * 0.5)
    if titled_opponent(played_games) < min_titled:
        return False

    min_required = max(3, math.ceil(total_played_games / 3))
    if required_titled_opponent(played_games, target_title) < min_required:
        return False
    
    return True