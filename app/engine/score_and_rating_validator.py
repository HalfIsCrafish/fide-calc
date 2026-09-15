from app.engine.calculator import filter_played_games, calculate_rating_average, calculate_performance
from app.engine.models import Game
from app.engine.tables import MIN_AVERAGE_RATING_TABLE, PERFORMANCE_TABLE

def minimum_score_percentage(games: list[Game]) -> float:
    """Function to count score percentage based on the games played. 
    1.4.8b 'The minimum score is 35% for all norms.' """
 
    played_games = filter_played_games(games)
    if not played_games:
        return 0.0

    total_points = sum(g.points for g in played_games)
    return total_points / len(played_games)

def validate_minimum_score(games: list[Game]) -> bool:
    """Validate 1.4.8b: True if score percentage is at least 35%."""
    return minimum_score_percentage(games) >= 0.35

def validate_minimum_average_rating(games: list[Game], target_title: str) -> bool:
    """Function to validate 1.4.8a: The minimum average ratings Ra of the opponents.
    The minimum average ratings Ra of the opponents are as follows:
    GM 2380; IM 2230; WGM 2180; WIM 2030"""

    played_games = filter_played_games(games)
    if not played_games:
        return False

    min_ra = MIN_AVERAGE_RATING_TABLE.get(target_title)
    if min_ra is None:
        return False

    ra = calculate_rating_average(played_games, target_title)
    return ra >= min_ra

def validate_performance_rating(games: list[Game], target_title: str) -> bool:
    """Function to validate 1.4.8: The minimum performance rating."""
    played_games = filter_played_games(games)
    if not played_games:
        return False

    min_rp = PERFORMANCE_TABLE.get(target_title)
    if min_rp is None:
        return False

    rp = calculate_performance(played_games, target_title)
    return rp >= min_rp