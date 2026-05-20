# Embedded IPL prediction responses
# Source: user's Excel export
# Match range: 56–70

RESPONSES = [
    {
        "name": "Half ticket",
        "56": "gt",
        "57": "kkr",
        "58": "pbks",
        "59": "csk",
        "60": "kkr",
        "61": "pbks",
        "62": "rr",
        "63": "csk",
        "64": "rr",
        "65": "kkr",
        "66": "csk",
        "67": "srh",
        "68": "pbks",
        "69": "mi",
        "70": "kkr"
    },
    {
        "name": "Meghana S Nair",
        "56": "gt",
        "57": "rcb",
        "58": "pbks",
        "59": "csk",
        "60": "kkr",
        "61": "pbks",
        "62": "rr",
        "63": "csk",
        "64": "rr",
        "65": "kkr",
        "66": "csk",
        "67": "rcb",
        "68": "pbks",
        "69": "rr",
        "70": "kkr"
    },
    {
        "name": "Srinath",
        "56": "srh",
        "57": "kkr",
        "58": "pbks",
        "59": "csk",
        "60": "kkr",
        "61": "pbks",
        "62": "dc",
        "63": "srh",
        "64": "rr",
        "65": "kkr",
        "66": "csk",
        "67": "srh",
        "68": "pbks",
        "69": "mi",
        "70": "dc"
    },
    {
        "name": "Shrihari",
        "56": "srh",
        "57": "rcb",
        "58": "pbks",
        "59": "csk",
        "60": "kkr",
        "61": "rcb",
        "62": "rr",
        "63": "csk",
        "64": "rr",
        "65": "mi",
        "66": "csk",
        "67": "rcb",
        "68": "pbks",
        "69": "mi",
        "70": "kkr"
    },
    {
        "name": "Sreevarsh William J",
        "56": "gt",
        "57": "rcb",
        "58": "mi",
        "59": "csk",
        "60": "gt",
        "61": "rcb",
        "62": "rr",
        "63": "srh",
        "64": "rr",
        "65": "kkr",
        "66": "csk",
        "67": "rcb",
        "68": "pbks",
        "69": "rr",
        "70": "dc"
    }
]


MATCH_RANGE = list(range(56, 71))


TEAM_FULL_NAMES = {
    "csk": "Chennai Super Kings",
    "dc": "Delhi Capitals",
    "gt": "Gujarat Titans",
    "kkr": "Kolkata Knight Riders",
    "lsg": "Lucknow Super Giants",
    "mi": "Mumbai Indians",
    "pbks": "Punjab Kings",
    "rr": "Rajasthan Royals",
    "rcb": "Royal Challengers Bengaluru",
    "srh": "Sunrisers Hyderabad"
}


TEAM_COLORS = {
    "csk": "#facc15",
    "dc": "#2563eb",
    "gt": "#1e293b",
    "kkr": "#7c3aed",
    "lsg": "#06b6d4",
    "mi": "#1d4ed8",
    "pbks": "#dc2626",
    "rr": "#ec4899",
    "rcb": "#ef4444",
    "srh": "#f97316"
}


def get_responses():
    return RESPONSES


def get_match_range():
    return MATCH_RANGE


def get_team_name(team_code: str):
    return TEAM_FULL_NAMES.get(team_code.lower(), team_code.upper())


def get_team_colors():
    return TEAM_COLORS