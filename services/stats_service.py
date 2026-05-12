from collections import Counter
from data.responses import get_match_range


def get_leaders(leaderboard):
    """
    Return all joint leaders with shared top rank.
    """
    if not leaderboard:
        return []

    top_rank = leaderboard[0]["rank"]
    return [player for player in leaderboard if player["rank"] == top_rank]


def get_team_popularity(responses):
    """
    Count total prediction frequency per team.
    """
    counts = Counter()
    match_range = get_match_range()

    for participant in responses:
        for match_no in match_range:
            guess = participant.get(str(match_no))

            if guess:
                counts[str(guess).strip().lower()] += 1

    return dict(counts)


def get_match_consensus(match_breakdown):
    """
    Per match prediction distribution.
    """
    consensus = []

    for match in match_breakdown:
        distribution = Counter()

        for prediction in match["predictions"]:
            distribution[prediction["guess"]] += 1

        consensus.append({
            "match": match["match"],
            "winner": match["winner"],
            "distribution": dict(distribution)
        })

    return consensus


def get_longest_streak(participant_breakdown):
    """
    Tie-aware longest streak detection.
    """
    streak_map = {}

    for name, entries in participant_breakdown.items():
        current = 0
        longest = 0

        ordered_entries = sorted(entries, key=lambda x: x["match"])

        for item in ordered_entries:
            if item["correct"]:
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        streak_map[name] = longest

    if not streak_map:
        return None

    best_streak = max(streak_map.values())

    if best_streak == 0:
        return None

    leaders = [
        name for name, streak in streak_map.items()
        if streak == best_streak
    ]

    return {
        "leaders": leaders,
        "streak": best_streak
    }


def get_pending_matches(actual_results):
    """
    Matches not yet completed.
    """
    match_range = get_match_range()

    return [
        match_no
        for match_no in match_range
        if match_no not in actual_results
    ]


def get_completed_matches(actual_results):
    """
    Matches already completed.
    """
    match_range = get_match_range()

    return [
        match_no
        for match_no in match_range
        if match_no in actual_results
    ]


def get_prediction_summary(match_breakdown):
    """
    Total correct / wrong.
    """
    total_correct = 0
    total_wrong = 0

    for match in match_breakdown:
        for prediction in match["predictions"]:
            if prediction["correct"]:
                total_correct += 1
            else:
                total_wrong += 1

    return {
        "total_correct": total_correct,
        "total_wrong": total_wrong
    }


def get_biggest_upset(match_consensus):
    """
    Winner picked by fewest people.
    """
    biggest = None
    fewest = None

    for match in match_consensus:
        winner = match["winner"]
        distribution = match["distribution"]

        winner_votes = distribution.get(winner, 0)

        if fewest is None or winner_votes < fewest:
            fewest = winner_votes
            biggest = {
                "match": match["match"],
                "winner": winner,
                "votes": winner_votes
            }

    return biggest


def build_dashboard_stats(
    responses,
    leaderboard,
    match_breakdown,
    participant_breakdown,
    actual_results
):
    """
    Master stats aggregator.
    """
    completed_matches = get_completed_matches(actual_results)
    pending_matches = get_pending_matches(actual_results)
    team_popularity = get_team_popularity(responses)
    match_consensus = get_match_consensus(match_breakdown)
    leaders = get_leaders(leaderboard)
    longest_streak = get_longest_streak(participant_breakdown)
    prediction_summary = get_prediction_summary(match_breakdown)
    biggest_upset = get_biggest_upset(match_consensus)

    return {
        "completed_matches": completed_matches,
        "pending_matches": pending_matches,
        "completed_count": len(completed_matches),
        "pending_count": len(pending_matches),
        "team_popularity": team_popularity,
        "match_consensus": match_consensus,
        "leaders": leaders,
        "longest_streak": longest_streak,
        "prediction_summary": prediction_summary,
        "biggest_upset": biggest_upset
    }