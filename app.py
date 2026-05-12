from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from data.responses import get_responses
from services.cricket_service import (
    get_completed_match_results,
    get_match_metadata
)
from services.scoring_service import (
    build_leaderboard,
    build_match_breakdown,
    build_participant_breakdown
)
from services.stats_service import build_dashboard_stats


app = FastAPI(
    title="IPL Prediction League",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def assemble_dashboard_payload():
    """
    Master orchestration layer.
    """
    responses = get_responses()

    actual_results = get_completed_match_results()
    metadata = get_match_metadata()

    leaderboard = build_leaderboard(
        responses=responses,
        actual_results=actual_results
    )

    match_breakdown = build_match_breakdown(
        responses=responses,
        actual_results=actual_results,
        metadata=metadata
    )

    participant_breakdown = build_participant_breakdown(
        responses=responses,
        actual_results=actual_results
    )

    stats = build_dashboard_stats(
        responses=responses,
        leaderboard=leaderboard,
        match_breakdown=match_breakdown,
        participant_breakdown=participant_breakdown,
        actual_results=actual_results
    )

    return {
        "leaderboard": leaderboard,
        "matches": match_breakdown,
        "participants": participant_breakdown,
        "stats": stats
    }


@app.get("/")
def home(request: Request):
    """
    Dashboard shell page.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": "IPL Prediction League"
        }
    )


@app.get("/api/dashboard")
def api_dashboard():
    """
    Full dashboard payload.
    """
    try:
        payload = assemble_dashboard_payload()
        return JSONResponse(payload)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to build dashboard",
                "details": str(e)
            }
        )


@app.get("/api/leaderboard")
def api_leaderboard():
    """
    Leaderboard only.
    """
    try:
        payload = assemble_dashboard_payload()
        return JSONResponse(payload["leaderboard"])

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to build leaderboard",
                "details": str(e)
            }
        )


@app.get("/api/matches")
def api_matches():
    """
    Match breakdown only.
    """
    try:
        payload = assemble_dashboard_payload()
        return JSONResponse(payload["matches"])

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to build match breakdown",
                "details": str(e)
            }
        )


@app.get("/api/stats")
def api_stats():
    """
    Stats only.
    """
    try:
        payload = assemble_dashboard_payload()
        return JSONResponse(payload["stats"])

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to build stats",
                "details": str(e)
            }
        )


@app.get("/health")
def health():
    """
    Health endpoint for deployment checks.
    """
    return {
        "status": "ok",
        "service": "ipl-prediction-league"
    }