from cricdata import CricinfoClient
import re


IPL_SERIES_ID = "ipl-2026-1510719"

client = CricinfoClient()


def fetch_series_matches():
    """
    Fetch raw IPL matches.
    Handles cricdata response variations safely.
    """
    payload = client.series_fixtures(IPL_SERIES_ID)

    if isinstance(payload, dict):
        if "content" in payload and "matches" in payload["content"]:
            return payload["content"]["matches"]

        if "matches" in payload:
            return payload["matches"]

    return []


def extract_match_number(match):
    """
    Extract numeric match number from title.
    Example:
    '56th Match' -> 56
    """
    title = match.get("title", "")
    found = re.search(r"(\d+)", title)

    if not found:
        return None

    return int(found.group(1))


def extract_winner(match):
    """
    Winner extraction using winnerTeamId.
    """
    winner_team_id = match.get("winnerTeamId")

    if not winner_team_id:
        return None

    teams = match.get("teams", [])

    for team_entry in teams:
        team = team_entry.get("team", {})

        if team.get("id") == winner_team_id:
            abbr = team.get("abbreviation")

            if abbr:
                return abbr.lower()

    return None


def is_completed_match(match):
    """
    RESULT only.
    """
    return match.get("status") == "RESULT"


def get_completed_match_results():
    matches = fetch_series_matches()
    results = {}

    for match in matches:
        if not is_completed_match(match):
            continue

        match_no = extract_match_number(match)
        winner = extract_winner(match)

        if match_no is None:
            continue

        if winner is None:
            continue

        results[match_no] = winner

    return results


def get_match_metadata():
    matches = fetch_series_matches()
    metadata = {}

    for match in matches:
        match_no = extract_match_number(match)

        if match_no is None:
            continue

        teams = []

        for team_entry in match.get("teams", []):
            team = team_entry.get("team", {})
            abbr = team.get("abbreviation")

            if abbr:
                teams.append(abbr.lower())

        ground = match.get("ground", {})
        venue = ground.get("smallName") or ground.get("name") or "Unknown"

        metadata[match_no] = {
            "match": match_no,
            "title": match.get("title"),
            "status": match.get("status"),
            "winner": extract_winner(match),
            "teams": teams,
            "venue": venue
        }

    return metadata