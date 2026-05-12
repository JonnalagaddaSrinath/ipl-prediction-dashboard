from data.responses import get_match_range


def normalize_team(value):
    """
    Normalize team code safely.
    """
    if value is None:
        return None

    return str(value).strip().lower()


def score_prediction(guess, actual):
    """
    Returns True if prediction matches actual winner.
    """
    guess = normalize_team(guess)
    actual = normalize_team(actual)

    if not guess or not actual:
        return False

    return guess == actual


def calculate_accuracy(score, attempted):
    """
    Accuracy percentage.
    """
    if attempted == 0:
        return 0.0

    return round((score / attempted) * 100, 2)


def assign_shared_ranks(leaderboard):
    """
    Competition ranking:
    scores: 8,8,7,7,6
    ranks : 1,1,3,3,5
    """
    if not leaderboard:
        return leaderboard

    current_rank = 1
    previous_score = None

    for index, participant in enumerate(leaderboard):
        if previous_score is None:
            participant["rank"] = current_rank
        elif participant["score"] == previous_score:
            participant["rank"] = current_rank
        else:
            current_rank = index + 1
            participant["rank"] = current_rank

        previous_score = participant["score"]

    return leaderboard


def build_leaderboard(responses, actual_results):
    """
    Returns:
    [
        {
            "rank": 1,
            "name": "Srinath",
            "score": 5,
            "attempted": 6,
            "accuracy": 83.33
        }
    ]
    """
    leaderboard = []
    match_range = get_match_range()

    for participant in responses:
        name = participant["name"]

        score = 0
        attempted = 0
        correct_matches = []
        wrong_matches = []

        for match_no in match_range:
            match_key = str(match_no)

            if match_no not in actual_results:
                continue

            actual = actual_results[match_no]
            guess = participant.get(match_key)

            if not guess:
                continue

            attempted += 1

            if score_prediction(guess, actual):
                score += 1
                correct_matches.append(match_no)
            else:
                wrong_matches.append(match_no)

        leaderboard.append({
            "name": name,
            "score": score,
            "attempted": attempted,
            "accuracy": calculate_accuracy(score, attempted),
            "correct_matches": correct_matches,
            "wrong_matches": wrong_matches
        })

    leaderboard.sort(
        key=lambda x: (
            -x["score"],
            -x["accuracy"],
            x["name"].lower()
        )
    )

    leaderboard = assign_shared_ranks(leaderboard)

    return leaderboard


def build_match_breakdown(responses, actual_results, metadata):
    """
    Match-centric view.
    """
    breakdown = []
    match_range = get_match_range()

    for match_no in match_range:
        if match_no not in actual_results:
            continue

        actual = actual_results[match_no]
        match_meta = metadata.get(match_no, {})

        predictions = []

        for participant in responses:
            name = participant["name"]
            guess = normalize_team(participant.get(str(match_no)))

            if not guess:
                continue

            predictions.append({
                "name": name,
                "guess": guess,
                "correct": score_prediction(guess, actual)
            })

        breakdown.append({
            "match": match_no,
            "winner": actual,
            "teams": match_meta.get("teams", []),
            "venue": match_meta.get("venue", "Unknown"),
            "title": match_meta.get("title", f"Match {match_no}"),
            "predictions": predictions
        })

    breakdown.sort(key=lambda x: x["match"])

    return breakdown


def build_participant_breakdown(responses, actual_results):
    """
    Participant-centric view.
    """
    participants = {}
    match_range = get_match_range()

    for participant in responses:
        name = participant["name"]
        entries = []

        for match_no in match_range:
            if match_no not in actual_results:
                continue

            actual = actual_results[match_no]
            guess = normalize_team(participant.get(str(match_no)))

            if not guess:
                continue

            entries.append({
                "match": match_no,
                "guess": guess,
                "actual": actual,
                "correct": score_prediction(guess, actual)
            })

        participants[name] = entries

    return participants