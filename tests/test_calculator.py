import pytest

from app.engine.calculator import (
    apply_rating_floor,
    calculate_performance,
    calculate_rating_average,
    calculate_total_points,
    filter_played_games,
    get_dp,
)
from app.engine.models import Game, Opponent

def test_filter_played_games():
    """function to test the filter_played_games function to ensure it correctly filters out games that have not been played or do not have an opponent."""

    opp = Opponent(id=1, name="P1", rating=2400, title="IM", federation="POL")
    games = [
        Game(round_number=1, opponent=opp, points=1.0, color="w", is_played=True),
        Game(
            round_number=2, opponent=opp, points=1.0, color="b", is_played=False
        ),
        Game(
            round_number=3, opponent=None, points=0.0, color=None, is_played=False
        ),
    ]
    filtered = filter_played_games(games)
    assert len(filtered) == 1
    assert filtered[0].round_number == 1


def test_apply_rating_floor():
    """function to test the apply_rating_floor function to ensure it correctly applies the rating floor for the target title."""

    assert apply_rating_floor([], "GM") == []

    ratings = [2100, 2050, 2450]
    assert apply_rating_floor(ratings, "GM") == [2200, 2100, 2450]

    ratings_im = [2200, 2300, 2400]
    assert apply_rating_floor(ratings_im, "IM") == [2200, 2300, 2400]


def test_calculate_rating_average():
    """function to test the calculate_rating_average function to ensure it correctly calculates the average rating based on the games played and the target title."""

    opp1 = Opponent(id=1, name="P1", rating=2400, title="IM", federation="POL")
    opp2 = Opponent(id=2, name="P2", rating=2401, title="IM", federation="POL")
    games = [
        Game(round_number=1, opponent=opp1, points=0.5, color="w", is_played=True),
        Game(round_number=2, opponent=opp2, points=0.5, color="b", is_played=True),
    ]
    assert calculate_rating_average(games, "IM") == 2401
    assert calculate_rating_average([], "IM") == 0


def test_calculate_total_points():
    """function to test the calculate_total_points function to ensure it correctly calculates the total points scored in the tournament."""

    games = [
        Game(round_number=1, opponent=None, points=1.0, color="w", is_played=True),
        Game(round_number=2, opponent=None, points=0.5, color="b", is_played=True),
        Game(round_number=3, opponent=None, points=0.0, color="w", is_played=True),
    ]
    assert calculate_total_points(games) == 1.5
    assert calculate_total_points([]) == 0.0


def test_get_dp():
    """function to test the get_dp function to ensure it correctly retrieves the DP value based on the score percentage using the DP_TABLE."""

    assert get_dp(0.50) == 0
    assert get_dp(6.0 / 9) == 125
    assert get_dp(0.35) == -110
    assert get_dp(1.0) == 800
    assert get_dp(0.0) == -800


def test_calculate_performance():
    """function to test the calculate_performance function to ensure it correctly calculates the performance rating based on the games played and the target title."""
    
    ratings = [2580, 2510, 2460, 2490, 2430, 2390, 2420, 2350, 2120]
    points = [1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5, 0.5]

    games = [
        Game(
            round_number=i + 1,
            opponent=Opponent(
                id=i, name=f"P{i}", rating=r, title=None, federation="GER"
            ),
            points=pts,
            color="w",
            is_played=True,
        )
        for i, (r, pts) in enumerate(zip(ratings, points))
    ]

    assert calculate_performance(games, "GM") == 2551
    assert calculate_performance([], "GM") == 0