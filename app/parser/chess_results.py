import httpx
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

def get_tournament_players(url: str) -> list[dict]:
    """Function to get the list of players from a tournament."""

    response = httpx.get(url, follow_redirects=True) 
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="CRs1")
    if not table:
        raise ValueError("Did not find players")

    players = []
    rows = table.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        if not cells:
            continue

        sno = int(cells[1].get_text(strip=True))
        name = cells[3].get_text(strip=True)
        raw_rating = cells[5].get_text(strip=True)
        rating = int(raw_rating) if raw_rating.isdigit() else 0

        players.append({"snr": sno, "name": name, "rating": rating})
    players.sort(key=lambda p: p["snr"])

    return players

def build_player_url(tournament_url: str, snr: int) -> str:
    """Builds the direct URL for a player's card (art=9) given their starting number."""

    parsed = urlparse(tournament_url)
    params = parse_qs(parsed.query)

    params["art"] = ["9"]
    params["snr"] = [str(snr)]

    new_query = urlencode(params, doseq=True)

    return urlunparse(parsed._replace(query=new_query))

    