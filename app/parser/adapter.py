from app.engine.models import Game, Opponent, TournamentPerformance


def parse_result_and_played_status(raw_res: str) -> tuple[float, bool]:
    """Function to parse the result string and determine whether the game was played or not."""

    cleaned = raw_res.strip().lower()

    played_scores = {
        "1": 1.0,
        "½": 0.5,
        "1/2": 0.5,
        "0": 0.0,
    }

    if cleaned in played_scores:
        return played_scores[cleaned], True

    unplayed_scores = {
        "1k": 1.0,
        "+ -": 1.0,
        "+": 1.0,
        "½k": 0.5,
        "0.5k": 0.5,
        "bye": 0.5,
        "- ½": 0.5,
        "- 1/2": 0.5,
        "½ -": 0.5,
        "1/2 -": 0.5,
        "0k": 0.0,
        "- +": 0.0,
        "-": 0.0,
        "- -": 0.0,
    }
    if cleaned in unplayed_scores:
        return unplayed_scores[cleaned], False

    return 0.0, False


def map_chess_results_to_games(matches: list[dict]) -> list[Game]:
    """Maps parsed chess-results match records to engine game models."""

    games: list[Game] = []

    for match in matches:
        points, is_played = parse_result_and_played_status(match["Res."])

        opponent = None
        if is_played:
            raw_rating = match["Rtg"].strip()
            rating = int(raw_rating) if raw_rating.isdigit() else 1400

            opponent = Opponent(
                name=match["Name"],
                federation=match["FED"],
                rating=rating,
                title=match.get("Title"),
            )
        
        games.append(
            Game(
                round_number=int(match["Rd."]),
                opponent=opponent,
                color=match.get("Color"),
                points=points,
                is_played=is_played,
            )
        )

    return games

def map_chess_results_to_performance(
    matches: list[dict],
    target_title: str,
    player_federation: str,
    player_name: str | None = None,
) -> TournamentPerformance:
    """Builds TournamentPerformance from chess-results matches and user input."""

    return TournamentPerformance(
        player_federation=player_federation,
        target_title=target_title,
        games=map_chess_results_to_games(matches),
        player_name=player_name,
    )

