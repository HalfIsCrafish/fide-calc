import pytest
from app.engine.models import Game, Opponent
from app.engine.validate_federation import (
    largest_foreign_federation_opponents,
    own_federation_opponents,
    unique_foreign_federations,
    validate_federation_requirements,
)


def create_mock_game(federation: str) -> Game:
    opponent = Opponent(
        fide_id=100000,
        name="Test Player",
        title="GM",
        federation=federation,
        rating=2500,
    )
    return Game(
        round_number=1,
        opponent=opponent,
        points=1.0,
        is_played=True,
    )


def test_validate_federation_empty_games():
    assert validate_federation_requirements([], "POL") is False


def test_validate_federation_valid_9_rounds():
    feds = ["POL", "POL", "POL", "POL", "POL", "GER", "GER", "CZE", "CZE"]
    games = [create_mock_game(fed) for fed in feds]
    assert validate_federation_requirements(games, "POL") is True


def test_validate_federation_too_few_foreign_federations():
    feds = ["POL"] * 5 + ["GER"] * 4
    games = [create_mock_game(fed) for fed in feds]
    assert validate_federation_requirements(games, "POL") is False


def test_validate_federation_fid_does_not_count_as_foreign():
    feds = ["POL"] * 5 + ["GER"] * 2 + ["FID"] * 2
    games = [create_mock_game(fed) for fed in feds]
    assert validate_federation_requirements(games, "POL") is False


def test_validate_federation_fid_valid_with_two_other_foreign():
    feds = ["POL"] * 4 + ["GER"] * 2 + ["CZE"] * 2 + ["FID"]
    games = [create_mock_game(fed) for fed in feds]
    assert validate_federation_requirements(games, "POL") is True


def test_validate_federation_exceeds_own_federation_limit():
    feds = ["POL"] * 6 + ["GER"] * 2 + ["CZE"] * 1
    games = [create_mock_game(fed) for fed in feds]
    assert validate_federation_requirements(games, "POL") is False


def test_validate_federation_exceeds_single_foreign_federation_limit():
    feds = ["GER"] * 7 + ["CZE"] * 1 + ["POL"] * 1
    games = [create_mock_game(fed) for fed in feds]
    assert validate_federation_requirements(games, "POL") is False


def test_validate_federation_fid_exceeds_single_limit():
    feds = ["FID"] * 7 + ["GER"] * 1 + ["CZE"] * 1
    games = [create_mock_game(fed) for fed in feds]
    assert validate_federation_requirements(games, "POL") is False


def test_validate_federation_with_none_opponent():
    games = [
        create_mock_game("POL"),
        create_mock_game("POL"),
        create_mock_game("POL"),
        create_mock_game("GER"),
        create_mock_game("GER"),
        create_mock_game("CZE"),
        create_mock_game("CZE"),
        create_mock_game("FRA"),
        Game(round_number=9, opponent=None, points=1.0, is_played=False),
    ]
    assert validate_federation_requirements(games, "POL") is True