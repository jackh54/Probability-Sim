from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__, template_folder='templates')

experiments = {}

def calculate_statistics(experiment_name):
    flip_history = experiments.get(experiment_name, [])
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
    experiment_name = request.args.get("experiment", "default")
    if experiment_name not in experiments:
        experiments[experiment_name] = []
    
    result = "Heads" if random.random() < 0.5 else "Tails"
    experiments[experiment_name].append(result)
    stats = calculate_statistics(experiment_name)
    return jsonify({
        "experiment": experiment_name,
        "flip_result": result,
        "total_flips": stats["total_flips"],
        "heads_count": stats["heads_count"],
        "tails_count": stats["tails_count"],
        "heads_probability": stats["heads_probability"],
        "tails_probability": stats["tails_probability"],
        "last_flip": stats["last_flip"]
    })

@app.route("/stats", methods=["GET"])
def get_stats():
    experiment_name = request.args.get("experiment", "default")
    return jsonify(calculate_statistics(experiment_name))

@app.route("/reset", methods=["POST"])
def reset_flips():
    experiment_name = request.args.get("experiment", "default")
    experiments[experiment_name] = []
    return jsonify({"message": f"Flip history reset for experiment '{experiment_name}'", "total_flips": 0})

if __name__ == "__main__":
    app.run(debug=True)
