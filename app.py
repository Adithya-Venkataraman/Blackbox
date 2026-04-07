from flask import Flask, request, jsonify, send_file, session, redirect
from flask_cors import CORS
from challenges import get_challenge, CHALLENGES, ROUNDS, ANSWERS, HINTS
import json, os, re

app = Flask(__name__)
CORS(app)
app.secret_key = "blackbox_secret_2024"

ADMIN_PASSWORD = "anveshan2025"
DATA_FILE = "sessions.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "teams": {},
        "current_round": 1,
        "round_ended": False
    }

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

data = load_data()

def get_team(team):
    if team not in data["teams"]:
        data["teams"][team] = {
            "queries": 0,
            "history": [],
            "hypotheses": {},
            "scores":       {"1": 0, "2": 0, "3": 0},
            "correct":      {"1": 0, "2": 0, "3": 0},
            "eliminated":   False,
            "round_queries":{"1": 0, "2": 0, "3": 0}
        }
    return data["teams"][team]

def normalize(s):
    s = s.lower().strip()
    s = re.sub(r'\s+', '', s)
    s = s.replace('f(x)=', '')
    s = s.replace('f(x)', '')
    s = s.replace('y=', '')
    s = s.replace('*', '')
    s = s.replace('^', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace('=', '')
    s = s.replace('-', '')
    s = s.replace('_', '')
    return s

# ── PAGES ──
@app.route("/")
def index():
    return send_file("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        return send_file("login.html"), 401
    if not session.get("admin"):
        return send_file("login.html")
    return send_file("admin.html")

@app.route("/admin-logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")

# ── QUERY ──
@app.route("/query", methods=["POST"])
def query():
    body    = request.json
    team    = body.get("team")
    chal_id = int(body.get("challenge_id", 1))
    raw     = body.get("input", "")
    t       = get_team(team)
    rnd     = data["current_round"]

    if t["eliminated"]:
        return jsonify({"error": "Team eliminated"}), 403

    fn = get_challenge(chal_id)
    if fn is None:
        return jsonify({"error": "Invalid challenge"}), 400

    try:
        result = fn(raw)
        t["queries"] += 1
        t["round_queries"][str(rnd)] = t["round_queries"].get(str(rnd), 0) + 1
        t["history"].append({
            "input":     raw,
            "output":    str(result),
            "challenge": chal_id,
            "round":     rnd
        })
        save_data(data)
        return jsonify({
            "output":       result,
            "queries_used": t["queries"],
            "round_queries":t["round_queries"].get(str(rnd), 0)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ── SUBMIT HYPOTHESIS ──
@app.route("/submit", methods=["POST"])
def submit():
    body    = request.json
    team    = body.get("team")
    chal_id = str(body.get("challenge_id"))
    formula = body.get("formula", "").strip().lower()
    t       = get_team(team)
    rnd     = data["current_round"]

    if t["eliminated"]:
        return jsonify({"error": "Team eliminated"}), 403

    correct_ans = ANSWERS.get(int(chal_id), "")
    is_correct  = normalize(formula) == normalize(correct_ans)

    print(f"INPUT:    '{normalize(formula)}'")
    print(f"EXPECTED: '{normalize(correct_ans)}'")
    print(f"MATCH:     {is_correct}")

    rnd_queries = t["round_queries"].get(str(rnd), 0)
    score       = (100 if is_correct else 0) - (rnd_queries * 3)

    t["hypotheses"][chal_id] = {
        "formula":  formula,
        "correct":  is_correct,
        "score":    score
    }

    round_challenges = ROUNDS.get(rnd, [])
    total = 0
    correct_count = 0
    for c in round_challenges:
        h = t["hypotheses"].get(str(c))
        if h:
            total += h["score"]
            if h["correct"]:
                correct_count += 1

    t["scores"][str(rnd)]  = total
    t["correct"][str(rnd)] = correct_count
    save_data(data)

    return jsonify({
        "correct":       is_correct,
        "score":         score,
        "round_score":   total,
        "correct_count": correct_count,
        "expected":      ANSWERS.get(int(chal_id))
    })

# ── ROUND STATUS (for frontend to poll) ──
@app.route("/api/round")
def get_round():
    return jsonify({
        "round":       data["current_round"],
        "round_ended": data.get("round_ended", False)
    })

# ── ADMIN: END ROUND ──
@app.route("/api/end-round", methods=["POST"])
def end_round():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401
    data["round_ended"] = True
    save_data(data)
    return jsonify({"round_ended": True})

# ── ADMIN: NEXT ROUND ──
@app.route("/api/next-round", methods=["POST"])
def next_round():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401
    if not data.get("round_ended"):
        return jsonify({"error": "End the current round first"}), 403
    if data["current_round"] < 3:
        data["current_round"] += 1
        data["round_ended"] = False
        save_data(data)
    return jsonify({"round": data["current_round"]})

# ── ADMIN: STANDINGS ──
@app.route("/api/standings")
def standings():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401
    rnd   = data["current_round"]
    teams = []
    for name, t in data["teams"].items():
        teams.append({
            "team":        name,
            "round_score": t["scores"].get(str(rnd), 0),
            "correct":     t["correct"].get(str(rnd), 0),
            "queries":     t["round_queries"].get(str(rnd), 0),
            "eliminated":  t["eliminated"]
        })
    teams.sort(key=lambda x: (-x["round_score"], x["queries"]))
    return jsonify({
        "round":       rnd,
        "round_ended": data.get("round_ended", False),
        "teams":       teams
    })

# ── ADMIN: ELIMINATE ──
@app.route("/api/eliminate", methods=["POST"])
def eliminate():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401
    body  = request.json
    n     = int(body.get("bottom_n", 1))
    rnd   = data["current_round"]
    teams = [
        (name, t["scores"].get(str(rnd), 0), t["round_queries"].get(str(rnd), 0))
        for name, t in data["teams"].items()
        if not t["eliminated"]
    ]
    teams.sort(key=lambda x: (x[1], -x[2]))
    eliminated = []
    for name, _, _ in teams[:n]:
        data["teams"][name]["eliminated"] = True
        eliminated.append(name)
    save_data(data)
    return jsonify({"eliminated": eliminated})

# ── ADMIN: ALL SESSIONS ──
@app.route("/all-sessions")
def all_sessions():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(data)

# ── HINTS (optional, for participants) ──
@app.route("/hint/<int:chal_id>")
def hint(chal_id):
    return jsonify({"hint": HINTS.get(chal_id, "No hint available")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)