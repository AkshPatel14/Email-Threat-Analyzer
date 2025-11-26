# app.py
import os
import joblib
import math
from flask import Flask, render_template, request, redirect, url_for, flash

# ---------- Config ----------
MODELS_DIR = "models"
SECRET_KEY = "change_this_to_a_random_secret_in_prod"
THRESHOLD = 0.5  # final threshold for marking SPAM (tweakable)
# ---------------------------

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Load TF-IDF + Naive Bayes model at startup
load_error = None
tfidf = None
nb_model = None

try:
    tfidf = joblib.load(os.path.join(MODELS_DIR, "tfidf.pkl"))
    nb_model = joblib.load(os.path.join(MODELS_DIR, "nb_model.pkl"))
except Exception as e:
    load_error = str(e)
    tfidf = nb_model = None

# ---------- Heuristic functions ----------
SPAM_KEYWORDS = [
    "urgent", "verify", "verification", "account locked", "account has been",
    "immediate attention", "click", "claim", "congratulations", "winner",
    "won", "free", "prize", "limited offer", "bank account", "update your information",
    "verify your", "verify now", "reset", "secure your account", "payment overdue",
    "loan approval", "final notice"
]

def keyword_score(text: str):
    matches = []
    t = text.lower()
    for k in SPAM_KEYWORDS:
        if k in t:
            matches.append(k)
    score = min(1.0, len(matches) / 4.0)  # 4 matches -> full score (tunable)
    return score, matches

def uppercase_score(original: str):
    words = original.split()
    if not words:
        return 0.0
    all_caps = sum(1 for w in words if w.isalpha() and w.upper() == w and len(w) >= 2)
    return min(1.0, all_caps / 3.0)  # 3 ALL-CAPS words => full signal

def sigmoid(x: float) -> float:
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

# ---------- Prediction with heuristic ----------
def predict_with_heuristic(message: str):
    """Return detailed prediction info using MultinomialNB + heuristic boosting."""
    if tfidf is None or nb_model is None:
        return {"error": "Model not loaded"}

    vec = tfidf.transform([message])
    raw_prob = None
    try:
        # MultinomialNB has predict_proba
        raw_prob = float(nb_model.predict_proba(vec)[0][1])
    except Exception as e:
        return {"error": f"Model scoring error: {e}"}

    # heuristic signals
    k_score, matched = keyword_score(message)
    up_score = uppercase_score(message)

    # combine boost
    boost = 0.5 * k_score + 0.3 * up_score
    adjusted_prob = min(1.0, raw_prob + boost)

    final_label = "SPAM" if adjusted_prob >= THRESHOLD else "SAFE"

    return {
        "raw_prob": round(raw_prob, 4),
        "keyword_score": round(k_score, 4),
        "matched_keywords": matched,
        "uppercase_score": round(up_score, 4),
        "boost": round(boost, 4),
        "adjusted_prob": round(adjusted_prob, 4),
        "final_label": final_label
    }

# ---------- Flask routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if load_error:
        flash("Model loading error: " + load_error, "danger")

    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if not message:
            flash("Please paste an email/message to classify.", "warning")
            return redirect(url_for("index"))

        info = predict_with_heuristic(message)
        if "error" in info:
            flash(info["error"], "danger")
            return redirect(url_for("index"))

        # pass the full info to the template
        return render_template("index.html", message=message, info=info)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
