from typing import Optional
from pydantic import BaseModel


class Opponent(BaseModel):
    """Model for representing an opponent in the tournament."""

    name: str # name of the opponent
    federation: str # federation of the opponent
    fide_id: Optional[int] = None # FIDE ID of the opponent 
    rating: int = 1400 # default rating for the opponent (we can change when we name the opponent)
    title: Optional[str] = None # title of the opponent
    starting_rank: Optional[int] = None # starting rank of the opponent in the tournament
                                        # id of the opponent in the tournament 

class Game(BaseModel):
    """Model for representing a game in the tournament."""

    round_number: int # round number of the tournament
    opponent: Optional[Opponent] = None # opponent of the player in the game
    color: Optional[str] = None # color which the player played in the game (white or black)
    points: float # points scored in the game
    is_played: bool # flag indicating whether the game was played or not

class TournamentPerformance(BaseModel):
    """Model for representing the performance of a player in a tournament."""

    player_federation: str # federation of the player to calculate needed federations
    target_title: str # target title of the player to calculate norm
    games: list[Game] # list of games played in the tournament
    player_name: Optional[str] = None # name of the player