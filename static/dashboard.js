let scoresChartInstance = null;
let teamChartInstance = null;


function showLoading() {
    document.getElementById("loading-state").classList.remove("hidden");
    document.getElementById("error-state").classList.add("hidden");
}

function hideLoading() {
    document.getElementById("loading-state").classList.add("hidden");
}

function showError(message) {
    hideLoading();
    document.getElementById("error-state").classList.remove("hidden");
    document.getElementById("error-message").textContent =
        message || "Unknown error";
}

function titleCaseTeam(code) {
    const teamMap = {
        csk: "Chennai Super Kings",
        dc: "Delhi Capitals",
        gt: "Gujarat Titans",
        kkr: "Kolkata Knight Riders",
        lsg: "Lucknow Super Giants",
        mi: "Mumbai Indians",
        pbks: "Punjab Kings",
        rr: "Rajasthan Royals",
        rcb: "Royal Challengers Bengaluru",
        srh: "Sunrisers Hyderabad"
    };

    return teamMap[code] || code.toUpperCase();
}

function getRankBadge(rank) {
    let cls = "rank-badge";

    if (rank === 1) cls += " rank-1";
    else if (rank === 2) cls += " rank-2";
    else if (rank === 3) cls += " rank-3";

    return `<span class="${cls}">#${rank}</span>`;
}

function formatLeaderText(leaders) {
    if (!leaders || leaders.length === 0) {
        return "--";
    }

    if (leaders.length === 1) {
        return `${leaders[0].name} (${leaders[0].score})`;
    }

    if (leaders.length <= 3) {
        const names = leaders.map(x => x.name).join(", ");
        return `Joint: ${names}`;
    }

    return `Joint Leaders (${leaders.length})`;
}

function formatStreakText(streakData) {
    if (!streakData) {
        return "--";
    }

    const leaders = streakData.leaders || [];
    const streak = streakData.streak;

    if (leaders.length === 1) {
        return `${leaders[0]} (${streak})`;
    }

    if (leaders.length <= 3) {
        return `${leaders.join(", ")} (${streak})`;
    }

    return `${leaders.length} tied (${streak})`;
}

function renderSummary(stats) {
    document.getElementById("completed-count").textContent =
        stats.completed_count;

    document.getElementById("pending-count").textContent =
        stats.pending_count;

    document.getElementById("top-performer").textContent =
        formatLeaderText(stats.leaders);

    document.getElementById("longest-streak").textContent =
        formatStreakText(stats.longest_streak);

    if (stats.biggest_upset) {
        document.getElementById("biggest-upset-match").textContent =
            `Match ${stats.biggest_upset.match}`;

        document.getElementById("biggest-upset-winner").textContent =
            titleCaseTeam(stats.biggest_upset.winner);

        document.getElementById("biggest-upset-votes").textContent =
            stats.biggest_upset.votes;
    } else {
        document.getElementById("biggest-upset-match").textContent = "--";
        document.getElementById("biggest-upset-winner").textContent = "--";
        document.getElementById("biggest-upset-votes").textContent = "--";
    }
}

function renderLeaderboard(leaderboard) {
    const tbody = document.getElementById("leaderboard-body");
    tbody.innerHTML = "";

    leaderboard.forEach(player => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${getRankBadge(player.rank)}</td>
            <td><strong>${player.name}</strong></td>
            <td>${player.score}</td>
            <td>${player.attempted}</td>
            <td>
                <span class="accuracy-pill">
                    ${player.accuracy}%
                </span>
            </td>
        `;

        tbody.appendChild(row);
    });
}

function renderMatchTimeline(matches) {
    const container = document.getElementById("match-timeline");
    container.innerHTML = "";

    if (!matches || matches.length === 0) {
        container.innerHTML = `
            <div class="match-card">
                <div class="match-title">No completed matches yet</div>
                <div class="match-meta">
                    Predictions will be scored once tracked matches finish.
                </div>
            </div>
        `;
        return;
    }

    matches.forEach(match => {
        const card = document.createElement("div");
        card.className = "match-card";

        const predictionsHTML = match.predictions
            .map(pred => `
                <div class="prediction-row">
                    <span class="prediction-name">${pred.name}</span>
                    <span class="prediction-result ${pred.correct ? "correct" : "wrong"}">
                        ${pred.guess.toUpperCase()} ${pred.correct ? "✅" : "❌"}
                    </span>
                </div>
            `)
            .join("");

        card.innerHTML = `
            <div class="match-title">${match.title}</div>
            <div class="match-meta">${match.venue}</div>
            <div class="winner-tag">
                Winner: ${titleCaseTeam(match.winner)}
            </div>

            <div class="prediction-list">
                ${predictionsHTML}
            </div>
        `;

        container.appendChild(card);
    });
}

function renderScoresChart(leaderboard) {
    const ctx = document.getElementById("scores-chart");

    if (scoresChartInstance) {
        scoresChartInstance.destroy();
    }

    scoresChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: leaderboard.map(x => x.name),
            datasets: [{
                label: "Score",
                data: leaderboard.map(x => x.score)
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#cbd5e1"
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#cbd5e1",
                        precision: 0
                    }
                }
            }
        }
    });
}

function renderTeamChart(stats) {
    const ctx = document.getElementById("team-chart");

    if (teamChartInstance) {
        teamChartInstance.destroy();
    }

    const popularity = stats.team_popularity || {};

    teamChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: Object.keys(popularity).map(titleCaseTeam),
            datasets: [{
                data: Object.values(popularity)
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                }
            }
        }
    });
}

async function loadDashboard() {
    showLoading();

    try {
        const response = await fetch("/api/dashboard");

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const payload = await response.json();

        renderSummary(payload.stats);
        renderLeaderboard(payload.leaderboard);
        renderMatchTimeline(payload.matches);
        renderScoresChart(payload.leaderboard);
        renderTeamChart(payload.stats);

        hideLoading();

    } catch (err) {
        console.error(err);
        showError(err.message);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});