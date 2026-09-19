import httpx
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def fetch_html(url: str) -> str:
    """Fetches HTML content from a given URL."""

    response = httpx.get(url, follow_redirects=True)
    response.raise_for_status()

    return response.text


def build_player_url(tournament_url: str, snr: int) -> str:
    """Builds the direct URL for a player's card (art=9) given their starting number."""

    parsed = urlparse(tournament_url)
    params = parse_qs(parsed.query)

    params["art"] = ["9"]
    params["snr"] = [str(snr)]

    new_query = urlencode(params, doseq=True)

    return urlunparse(parsed._replace(query=new_query))


def parse_tournament_players(html: str) -> list[dict]:
    """Parses starting list from HTML string."""

    soup = BeautifulSoup(html, "html.parser")

    column_aliases: dict[str, list[str]] = {
        "snr": ["No.", "Nr", "SNo", "SNR", "Lp."],
        "name": ["Name", "Nom", "Player"],
        "rating": ["Rtg", "Rtgl", "Elo", "Rating", "FIDE"],
    }

    target_table = None
    header_indices: dict[str, int] = {}

    for table in soup.find_all("table", class_="CRs1"):
        header_row = table.find("tr")
        if not header_row:
            continue

        th_cells = header_row.find_all("th")
        raw_headers = []
        for th in th_cells:
            raw_headers.append(th.get_text(strip=True))

        is_candidate_table = False
        for alias in column_aliases["name"]:
            if alias in raw_headers:
                is_candidate_table = True
                break

        if is_candidate_table:
            target_table = table
            for field, aliases in column_aliases.items():
                for alias in aliases:
                    found = False
                    for idx, header_text in enumerate(raw_headers):
                        if header_text == alias:
                            header_indices[field] = idx
                            found = True
                            break
                    if found:
                        break
            break

    if not target_table:
        raise ValueError("Did not find players")

    missing_fields = []
    for field in column_aliases:
        if field not in header_indices:
            missing_fields.append(field)

    if missing_fields:
        raise KeyError(f"Missing columns: {missing_fields}")

    snr_idx = header_indices["snr"]
    name_idx = header_indices["name"]
    rtg_idx = header_indices["rating"]
    max_idx = max(snr_idx, name_idx, rtg_idx)

    players: list[dict] = []
    rows = target_table.find_all("tr", recursive=False)

    for row in rows[1:]:
        cells = row.find_all("td", recursive=False)
        if not cells or len(cells) <= max_idx:
            continue

        raw_snr = cells[snr_idx].get_text(strip=True)
        raw_name = cells[name_idx].get_text(strip=True)
        raw_rating = cells[rtg_idx].get_text(strip=True)

        snr = int(raw_snr) if raw_snr.isdigit() else 0
        rating = int(raw_rating) if raw_rating.isdigit() else 0

        players.append({
            "snr": snr,
            "name": raw_name,
            "rating": rating
        })

    players.sort(key=lambda p: p["snr"])

    return players


def parse_player_matches(html: str) -> list[dict]:
    """Parses player match history from HTML string."""

    soup = BeautifulSoup(html, "html.parser")

    column_aliases: dict[str, list[str]] = {
        "Rd.": ["Rd.", "Rnd", "Rnd.", "Round"],
        "Name": ["Name", "Nom", "Player"],
        "Rtg": ["Rtg", "Elo", "Rating", "FIDE"],
        "FED": ["FED", "Fed", "Fed.", "Country"],
        "Res.": ["Res.", "Result", "Pts"]
    }

    target_table = None
    header_indices: dict[str, int] = {}

    for table in soup.find_all("table", class_="CRs1"):
        header_row = table.find("tr")
        if not header_row:
            continue

        th_cells = header_row.find_all("th")
        raw_headers = []
        for th in th_cells:
            raw_headers.append(th.get_text(strip=True))

        is_candidate_table = False
        for alias in column_aliases["Rd."]:
            if alias in raw_headers:
                is_candidate_table = True
                break

        if is_candidate_table:
            target_table = table
            for field, aliases in column_aliases.items():
                for alias in aliases:
                    found = False
                    for idx, header_text in enumerate(raw_headers):
                        if header_text == alias:
                            header_indices[field] = idx
                            found = True
                            break
                    if found:
                        break
            break

    if not target_table:
        raise ValueError("Did not find matches table")

    missing_fields = []
    for field in column_aliases:
        if field not in header_indices:
            missing_fields.append(field)

    if missing_fields:
        raise KeyError(f"Missing columns: {missing_fields}")

    matches: list[dict] = []
    rows = target_table.find_all("tr", recursive=False)
    max_idx = max(header_indices.values())

    for row in rows[1:]:
        cells = row.find_all("td", recursive=False)
        if not cells or len(cells) <= max_idx:
            continue

        res_cell = cells[header_indices["Res."]]
        color = None
        if res_cell.find("div", class_="FarbewT"):
            color = "w"
        elif res_cell.find("div", class_="FarbesT"):
            color = "b"

        matches.append({
            "Rd.": cells[header_indices["Rd."]].get_text(strip=True),
            "Name": cells[header_indices["Name"]].get_text(strip=True),
            "Rtg": cells[header_indices["Rtg"]].get_text(strip=True),
            "FED": cells[header_indices["FED"]].get_text(strip=True),
            "Res.": cells[header_indices["Res."]].get_text(strip=True),
            "Color": color
        })

    return matches


def get_tournament_players(url: str) -> list[dict]:
    """Fetches and parses players from tournament starting list URL."""

    html = fetch_html(url)

    return parse_tournament_players(html)


def get_player_matches(url: str) -> list[dict]:
    """Fetches and parses matches from player URL."""

    html = fetch_html(url)

    return parse_player_matches(html)

