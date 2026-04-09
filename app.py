from flask import Flask, request, jsonify, session, redirect, render_template
from flask_cors import CORS
from challenges import get_challenge, CHALLENGES, ROUNDS, ANSWERS, HINTS, ANSWER_KEYWORDS
import json, os, re

app = Flask(__name__)
CORS(app)
app.secret_key = "blackbox_secret_2024"
app.config["SESSION_PERMANENT"] = False
# One-time token issued after POST login, consumed on first GET — forces re-auth on every reload
_admin_tokens = set()

ADMIN_PASSWORD = "anveshan2025"
DATA_FILE = "sessions.json"

# ── LOAD & SAVE ───────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"teams": {}, "current_round": 1, "round_ended": False,
            "frozen": False, "broadcast": ""}

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

data = load_data()
if "frozen"    not in data: data["frozen"]    = False
if "broadcast" not in data: data["broadcast"] = ""

# ── TEAM ──────────────────────────────────────────────────────────────────────
def get_team(team):
    if team not in data["teams"]:
        data["teams"][team] = {
            "queries": 0, "history": [], "hypotheses": {},
            "scores":        {"1": 0, "2": 0, "3": 0},
            "correct":       {"1": 0, "2": 0, "3": 0},
            "eliminated":    False,
            "round_queries": {"1": 0, "2": 0, "3": 0}
        }
    return data["teams"][team]

# ── KEYWORD ANSWER CHECK ──────────────────────────────────────────────────────
def normalize(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def check_answer(chal_id, submitted):
    cleaned = normalize(submitted)
    for group in ANSWER_KEYWORDS.get(int(chal_id), []):
        if all(kw.lower() in cleaned for kw in group):
            return True
    return False

# ── PAGES ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    import secrets as _secrets
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            # Issue a one-time token, store in session
            tok = _secrets.token_hex(16)
            _admin_tokens.add(tok)
            session["admin_tok"] = tok
            return redirect("/admin")
        return render_template("login.html", error=True)

    # GET: consume the token — valid only once per login POST
    tok = session.pop("admin_tok", None)
    if tok and tok in _admin_tokens:
        _admin_tokens.discard(tok)
        # Issue a fresh page-lifetime token stored only for API calls this session
        session["admin"] = True
        return render_template("admin.html")

    # Any reload hits here — session["admin"] is gone, must re-login
    session.clear()
    return render_template("login.html", error=False)

@app.route("/admin-logout")
def logout():
    session.clear()
    return redirect("/admin")

# ── QUERY ─────────────────────────────────────────────────────────────────────
@app.route("/query", methods=["POST"])
def query():
    body    = request.json
    team    = body.get("team", "").strip()
    chal_id = int(body.get("challenge_id", 1))
    raw     = body.get("input", "")
    if not team:
        return jsonify({"error": "No team name"}), 400

    t   = get_team(team)
    rnd = data["current_round"]

    if t["eliminated"]:      return jsonify({"error": "Team eliminated"}), 403
    if data.get("frozen"):   return jsonify({"error": "Submissions frozen by coordinator"}), 403

    fn = get_challenge(chal_id)
    if fn is None: return jsonify({"error": "Invalid challenge"}), 400

    try:
        result = fn(raw)
        t["queries"] += 1
        t["round_queries"][str(rnd)] = t["round_queries"].get(str(rnd), 0) + 1
        t["history"].append({"input": raw, "output": str(result), "challenge": chal_id, "round": rnd})
        save_data(data)
        return jsonify({"output": result, "queries_used": t["queries"],
                        "round_queries": t["round_queries"].get(str(rnd), 0)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ── SUBMIT ────────────────────────────────────────────────────────────────────
@app.route("/submit", methods=["POST"])
def submit():
    body    = request.json
    team    = body.get("team", "").strip()
    chal_id = str(body.get("challenge_id"))
    formula = body.get("formula", "").strip().lower()
    t       = get_team(team)
    rnd     = data["current_round"]

    if t["eliminated"]:    return jsonify({"error": "Team eliminated"}), 403
    if data.get("frozen"): return jsonify({"error": "Submissions frozen by coordinator"}), 403

    is_correct  = check_answer(chal_id, formula)
    rnd_queries = t["round_queries"].get(str(rnd), 0)
    score       = (100 if is_correct else 0) - (rnd_queries * 3)

    t["hypotheses"][chal_id] = {"formula": formula, "correct": is_correct, "score": score}

    total, correct_count = 0, 0
    for c in ROUNDS.get(rnd, []):
        h = t["hypotheses"].get(str(c))
        if h:
            total += h["score"]
            if h["correct"]: correct_count += 1

    t["scores"][str(rnd)]  = total
    t["correct"][str(rnd)] = correct_count
    save_data(data)

    return jsonify({"correct": is_correct, "score": score, "round_score": total,
                    "correct_count": correct_count, "expected": ANSWERS.get(int(chal_id))})

# ── ROUND STATUS (also returns broadcast + frozen) ────────────────────────────
@app.route("/api/round")
def get_round():
    return jsonify({"round": data["current_round"], "round_ended": data.get("round_ended", False),
                    "frozen": data.get("frozen", False), "broadcast": data.get("broadcast", "")})

# ── ADMIN: END ROUND ──────────────────────────────────────────────────────────
@app.route("/api/end-round", methods=["POST"])
def end_round():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    data["round_ended"] = True
    save_data(data)
    return jsonify({"round_ended": True})

# ── ADMIN: NEXT ROUND ─────────────────────────────────────────────────────────
@app.route("/api/next-round", methods=["POST"])
def next_round():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    if not data.get("round_ended"): return jsonify({"error": "End the current round first"}), 403
    if data["current_round"] < 3:
        data["current_round"] += 1
        data["round_ended"] = False
        save_data(data)
    return jsonify({"round": data["current_round"]})

# ── ADMIN: STANDINGS ──────────────────────────────────────────────────────────
@app.route("/api/standings")
def standings():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    rnd = data["current_round"]
    teams = []
    for name, t in data["teams"].items():
        # cumulative score across all rounds
        cumulative = sum(t["scores"].get(str(r), 0) for r in [1,2,3])
        teams.append({
            "team":       name,
            "round_score": t["scores"].get(str(rnd), 0),
            "cumulative":  cumulative,
            "correct":     t["correct"].get(str(rnd), 0),
            "queries":     t["round_queries"].get(str(rnd), 0),
            "eliminated":  t["eliminated"]
        })
    teams.sort(key=lambda x: (-x["round_score"], x["queries"]))
    return jsonify({"round": rnd, "round_ended": data.get("round_ended", False),
                    "frozen": data.get("frozen", False), "teams": teams})

# ── ADMIN: ELIMINATE ──────────────────────────────────────────────────────────
@app.route("/api/eliminate", methods=["POST"])
def eliminate():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    n   = int(request.json.get("bottom_n", 1))
    rnd = data["current_round"]
    teams = [(name, t["scores"].get(str(rnd), 0), t["round_queries"].get(str(rnd), 0))
             for name, t in data["teams"].items() if not t["eliminated"]]
    teams.sort(key=lambda x: (x[1], -x[2]))
    eliminated = []
    for name, _, _ in teams[:n]:
        data["teams"][name]["eliminated"] = True
        eliminated.append(name)
    save_data(data)
    return jsonify({"eliminated": eliminated})

# ── ADMIN: FREEZE TOGGLE ──────────────────────────────────────────────────────
@app.route("/api/freeze", methods=["POST"])
def freeze():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    data["frozen"] = not data.get("frozen", False)
    save_data(data)
    return jsonify({"frozen": data["frozen"]})

# ── ADMIN: BROADCAST ──────────────────────────────────────────────────────────
@app.route("/api/broadcast", methods=["POST"])
def broadcast():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    data["broadcast"] = request.json.get("message", "")
    save_data(data)
    return jsonify({"broadcast": data["broadcast"]})

# ── ADMIN: RESET TEAM ─────────────────────────────────────────────────────────
@app.route("/api/reset-team", methods=["POST"])
def reset_team():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    name = request.json.get("team", "")
    if name in data["teams"]:
        data["teams"][name] = {
            "queries": 0, "history": [], "hypotheses": {},
            "scores": {"1":0,"2":0,"3":0}, "correct": {"1":0,"2":0,"3":0},
            "eliminated": False, "round_queries": {"1":0,"2":0,"3":0}
        }
        save_data(data)
    return jsonify({"reset": name})

# ── ADMIN: CSV EXPORT ─────────────────────────────────────────────────────────
@app.route("/api/export-csv")
def export_csv():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    lines = ["team,r1_score,r2_score,r3_score,cumulative,eliminated"]
    for name, t in data["teams"].items():
        r1 = t["scores"].get("1", 0)
        r2 = t["scores"].get("2", 0)
        r3 = t["scores"].get("3", 0)
        lines.append(f"{name},{r1},{r2},{r3},{r1+r2+r3},{t['eliminated']}")
    from flask import Response
    return Response("\n".join(lines), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=blackbox_results.csv"})

# ── ADMIN: ALL SESSIONS ───────────────────────────────────────────────────────
@app.route("/all-sessions")
def all_sessions():
    if not session.get("admin"): return jsonify({"error": "Unauthorized"}), 401
    return jsonify(data)

# ── HINT ──────────────────────────────────────────────────────────────────────
@app.route("/hint/<int:chal_id>")
def hint(chal_id):
    return jsonify({"hint": HINTS.get(chal_id, "no hint available")})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)