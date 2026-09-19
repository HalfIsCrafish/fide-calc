from pathlib import Path
import pytest

from app.parser.chess_results import parse_player_matches


@pytest.fixture
def player_matches_html() -> str:
    """Loads player card HTML fixture."""

    fixture_path = Path(__file__).parent / "fixtures" / "player_cards_1.html"

    return fixture_path.read_text(encoding="utf-8")


def test_parse_player_matches_total_rounds(player_matches_html: str):
    """Function to test parse_player_matches parses all rounds correctly."""

    matches = parse_player_matches(player_matches_html)

    assert len(matches) == 9


def test_parse_player_matches_first_round(player_matches_html: str):
    """Function to test parse_player_matches extracts first round details."""

    matches = parse_player_matches(player_matches_html)
    first_match = matches[0]

    assert first_match["Rd."] == "1"
    assert first_match["Name"] == "Filippone, Matteo"
    assert first_match["Rtg"] == "2016"
    assert first_match["FED"] == "ITA"
    assert first_match["Res."] == "½"
    assert first_match["Color"] in ["w", "b"]


def test_parse_player_matches_win_and_loss_results(player_matches_html: str):
    """Function to test parse_player_matches handles win and loss results."""

    matches = parse_player_matches(player_matches_html)

    assert matches[5]["Rd."] == "6"
    assert matches[5]["Name"] == "Pultinevicius, Paulius"
    assert matches[5]["Rtg"] == "2529"
    assert matches[5]["FED"] == "LTU"
    assert matches[5]["Res."] == "1"
    assert matches[5]["Color"] in ["w", "b"]

    assert matches[6]["Rd."] == "7"
    assert matches[6]["Name"] == "Glek, Igor"
    assert matches[6]["Rtg"] == "2429"
    assert matches[6]["FED"] == "BEL"
    assert matches[6]["Res."] == "0"
    assert matches[6]["Color"] in ["w", "b"]

def test_parse_player_matches_colors_extracted(player_matches_html: str):
    """Function to test parse_player_matches extracts piece colors correctly."""

    matches = parse_player_matches(player_matches_html)

    assert matches[0]["Color"] == "b"
    assert matches[1]["Color"] == "w"

def test_parse_player_matches_missing_table():
    """Function to test parse_player_matches raises ValueError when table is missing."""

    invalid_html = "<html><body><p>No table</p></body></html>"

    with pytest.raises(ValueError, match="Did not find matches table"):
        parse_player_matches(invalid_html)


def test_parse_player_matches_missing_required_column():
    """Function to test parse_player_matches raises KeyError when required column is absent."""

    incomplete_html = """<table class="CRs1"><tr><th>Rd.</th><th>Name</th><th>Rtg</th></tr></table>"""

    with pytest.raises(KeyError, match="Missing columns"):
        parse_player_matches(incomplete_html)