from flask import Flask, jsonify, request, render_template, session
import random

app = Flask(__name__, template_folder='templates', static_folder='static')

def get_experiment_data(experiment_name):
    """Retrieve the session-stored experiment data"""
    if "experiments" not in session:
        session["experiments"] = {}
    return session["experiments"].get(experiment_name, [])

def save_experiment_data(experiment_name, data):
    """Save experiment data to the session"""
    if "experiments" not in session:
        session["experiments"] = {}
    session["experiments"][experiment_name] = data
    session.modified = True

def calculate_statistics(experiment_name):
    """Calculate stats"""
    flip_history = get_experiment_data(experiment_name)
    total_flips = len(flip_history)
    heads_count = flip_history.count("Heads")
    tails_count = flip_history.count("Tails")

    heads_probability = (heads_count / total_flips) * 100 if total_flips > 0 else 0
    tails_probability = (tails_count / total_flips) * 100 if total_flips > 0 else 0

    return {
        "experiment": experiment_name,
        "total_flips": total_flips,
        "heads_count": heads_count,
        "tails_count": tails_count,
        "heads_probability": heads_probability,
        "tails_probability": tails_probability,
        "last_flip": flip_history[-1] if total_flips > 0 else None
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/experiments/<experiment_name>")
def experiment_page(experiment_name):
    return render_template(f"experiments/{experiment_name}.html", experiment_name=experiment_name)

@app.route("/flip", methods=["GET"])
def flip_coin():
    """Handles flipping the coin and storing results per session"""
    experiment_name = request.args.get("experiment", "default")
    flip_history = get_experiment_data(experiment_name)
    result = "Heads" if random.random() < 0.5 else "Tails"
    flip_history.append(result)
    save_experiment_data(experiment_name, flip_history)
    print(f"[DEBUG] Experiment: {experiment_name} - Flip Result: {result}")
    stats = calculate_statistics(experiment_name)
    return jsonify({
        "experiment": experiment_name,
        "flip_result": result,
        "total_flips": stats["total_flips"],
        "heads_count": stats["heads_count"],
        "tails_count": stats["tails_count"],
        "heads_probability": stats["heads_probability"],
        "tails_probability": stats["tails_probability"]
    })


@app.route("/stats", methods=["GET"])
def get_stats():
    """Fetches experiment statistics"""
    experiment_name = request.args.get("experiment", "default")
    return jsonify(calculate_statistics(experiment_name))

@app.route("/reset", methods=["POST"])
def reset_flips():
    """Resets an experiment for the current session"""
    experiment_name = request.args.get("experiment", "default")
    save_experiment_data(experiment_name, [])
    return jsonify({"message": f"Flip history reset for experiment '{experiment_name}'", "total_flips": 0})

if __name__ == "__main__":
    app.run(debug=True)
