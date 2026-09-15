import pytest
from app.engine.models import Game, Opponent
from app.engine.validate_title import (
    titled_opponent,
    required_titled_opponent,
    validate_title_requirements,
)

def make_game(title: str | None = None, is_played: bool = True) -> Game:
    opponent = Opponent(name="Player", rating=2400, federation="POL", title=title)
    return Game(round_number=1, opponent=opponent, points=0.5, is_played=is_played)


def test_titled_opponent_counts_only_handbook_titles():
    games = [
        make_game("GM"),
        make_game("IM"),
        make_game("FM"),
        make_game("CM"),   
        make_game(None),   
        make_game("WGM"),
    ]
    assert titled_opponent(games) == 4


def test_required_titled_opponent_for_gm_and_im():
    games = [
        make_game("GM"),
        make_game("GM"),
        make_game("IM"),
        make_game("FM"),
    ]
    assert required_titled_opponent(games, "GM") == 2
    assert required_titled_opponent(games, "IM") == 3


def test_validate_title_requirements_gm_success_9_rounds():
    games = []
    for i in range(3):
        games.append(make_game("GM"))
    for i in range(2):
        games.append(make_game("FM"))
    for i in range(4):
        games.append(make_game(None))

    assert validate_title_requirements(games, "GM") is True


def test_validate_title_requirements_fails_not_enough_gms():
    games = []
    for i in range(2):
        games.append(make_game("GM"))
    for i in range(3):
        games.append(make_game("FM"))
    for i in range(4):
        games.append(make_game(None))

    assert validate_title_requirements(games, "GM") is False


def test_validate_title_requirements_fails_not_enough_titled():
    games = []
    for i in range(3):
        games.append(make_game("GM"))
    for i in range(6):
        games.append(make_game(None))

    assert validate_title_requirements(games, "GM") is False


def test_validate_title_ignores_unplayed_games():
    games = []
    for i in range(3):
        games.append(make_game("GM"))
    for i in range(2):
        games.append(make_game("FM"))
    for i in range(4):
        games.append(make_game(None))
    games.append(make_game("GM", is_played=False))

    assert validate_title_requirements(games, "GM") is True