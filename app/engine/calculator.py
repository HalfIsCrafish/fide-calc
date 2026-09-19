import math
from app.engine.models import Game
from app.engine.tables import DP_TABLE, RATING_FLOORS_TABLE


def filter_played_games(games: list[Game]) -> list[Game]:
    """Function to filter the list of games to only include those that 
    have been played and have an opponent."""

    valid_games: list[Game] = []
    for game in games:
        if game.is_played and game.opponent is not None: 
            valid_games.append(game) 
    return valid_games

def apply_rating_floor(ratings: list[int], target_title: str) -> list[int]:
    """Function to apply the rating floor for the target title to the list of ratings."""

    if not ratings:
        return []

    adjusted_ratings = sorted(ratings) 
    floor = RATING_FLOORS_TABLE.get(target_title, 1400) # get the rating floor for the target title, default to 1400 if not found

    if adjusted_ratings[0] < floor:
        adjusted_ratings[0] = floor

    return adjusted_ratings

def calculate_rating_average(games: list[Game], target_title: str) -> int:
    """Function to calculate the average rating based on the games played, the target title and 1.4.7 with rounding half up to the nearest integer."""

    played_games = filter_played_games(games)
    if not played_games:
        return 0

    raw_ratings: list[int] = []
    for game in played_games:
        raw_ratings.append(game.opponent.rating)

    adjusted_ratings = apply_rating_floor(raw_ratings, target_title)

    total_rating = 0
    for r in adjusted_ratings: 
        total_rating += r

    avg = total_rating / len(adjusted_ratings)
    return math.floor(avg + 0.5) # round half up to the nearest integer

def calculate_total_points(games: list[Game]) -> float:
    """Function to calculate the total points scored in the tournament 
    based on the games played."""    

    played_games = filter_played_games(games)
    total_points = 0.0
    for game in played_games: 
        total_points += game.points 
    return total_points

def get_dp(score_percentage: float) -> int:
    """Function to get the DP value based on the score percentage using the DP_TABLE. All percentages are rounded to the nearest whole number. 0.5% is rounded up."""

    p_percent = math.floor(score_percentage * 100 + 0.5) # round the score percentage to the nearest integer
    p_clamped = max(0, min(100, p_percent)) # clamp the percentage to be between 0 and 100
    return DP_TABLE[round(p_clamped / 100, 2)] # return the DP value from the DP_TABLE based on the clamped percentage

def calculate_performance(games: list[Game], target_title: str) -> int:
    """Function to calculate the performance rating based on the games played and the target title."""

    played_games = filter_played_games(games)
    if not played_games: 
        return 0

    ra = calculate_rating_average(played_games, target_title)
    total_points = calculate_total_points(played_games) 
    
    score_percentage = total_points / len(played_games) 
    dp = get_dp(score_percentage) # get the DP value based on the score percentage

    return ra + dp 