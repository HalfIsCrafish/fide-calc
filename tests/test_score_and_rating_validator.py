import pytest
from app.engine.models import Game, Opponent
from app.engine.score_and_rating_validator import (
    minimum_score_percentage,
    validate_minimum_average_rating,
    validate_minimum_score,
)

def make_test_game(points: float, rating: int = 2400, is_played: bool = True) -> Game:
    opponent = Opponent(
        fide_id=1,
        name="Opponent",
        rating=rating,
        title="IM",
        federation="POL",
    )
    return Game(
        round_number=1,
        opponent=opponent,
        points=points,
        is_played=is_played,
    )

def test_minimum_score_percentage_calculation():
    games = [
        make_test_game(1.0),
        make_test_game(0.5),
        make_test_game(0.0),
        make_test_game(0.5),
    ]
    assert minimum_score_percentage(games) == 0.5

def test_minimum_score_percentage_ignores_unplayed():
    games = [
        make_test_game(1.0),
        make_test_game(0.0),
        make_test_game(1.0, is_played=False),
    ]
    assert minimum_score_percentage(games) == 0.5

def test_minimum_score_percentage_empty():
    assert minimum_score_percentage([]) == 0.0

def test_validate_minimum_score_thresholds():
    games_exact = [make_test_game(0.5) for _ in range(7)] + [
        make_test_game(0.0) for _ in range(3)
    ]
    assert validate_minimum_score(games_exact) is True

    games_below = [make_test_game(1.0) for _ in range(3)] + [
        make_test_game(0.0) for _ in range(6)
    ]
    assert validate_minimum_score(games_below) is False

def test_validate_minimum_average_rating_gm():
    games_gm_pass = [make_test_game(0.5, rating=2380) for _ in range(9)]
    assert validate_minimum_average_rating(games_gm_pass, "GM") is True

    games_gm_fail = [make_test_game(0.5, rating=2379) for _ in range(9)]
    assert validate_minimum_average_rating(games_gm_fail, "GM") is False

def test_validate_minimum_average_rating_invalid_title_or_empty():
    games = [make_test_game(0.5, rating=2450) for _ in range(9)]
    assert validate_minimum_average_rating(games, "INVALID_TITLE") is False
    assert validate_minimum_average_rating([], "GM") is False