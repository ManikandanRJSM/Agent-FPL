import requests
import json
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "fpl-agent-secret"

API_BASE = "http://127.0.0.1:8000"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/players", methods=["GET", "POST"])
def players():
    if request.method == "GET":
        session.clear()
        return redirect(url_for("index"))
    manager_id = request.form.get("manager_id")
    auth_token = request.form.get("auth_token")

    session["manager_id"] = manager_id
    session["auth_token"] = auth_token

    response = requests.get(
        f"{API_BASE}/get_manger_players/{manager_id}",
        headers={"Authorization": auth_token}
    )

    if response.status_code != 200 or response.json().get("status") != "SUCCESS":
        error = response.json().get("data", "Failed to fetch players.")
        return render_template("index.html", error=error)

    response_data = response.json().get("data", {})
    players = response_data.get("player_data", [])
    manager_data = response_data.get("manager_data", {})
    return render_template("players.html", players=players, manager_id=manager_id, manager_data=manager_data)


@app.route("/transfer", methods=["POST"])
def transfer():
    manager_id = session.get("manager_id")
    player = request.get_json()

    if not player or not manager_id:
        return {"status": "FAILED", "data": "Missing data"}, 400

    response = requests.post(
        f"{API_BASE}/get_player_suggestion/{manager_id}",
        json=player
    )

    return response.json() if response.status_code == 200 else ({"status": "FAILED"}, 500)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
