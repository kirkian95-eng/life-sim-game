from flask import Flask, jsonify, request
from simulation.engine import Ecosystem

app = Flask(__name__)
ecosystem = Ecosystem()


@app.route("/api/simulation", methods=["POST"])
def create_simulation():
    """Reset and create a fresh simulation."""
    global ecosystem
    ecosystem = Ecosystem()
    return jsonify(ecosystem.get_state()), 201


@app.route("/api/simulation/tick", methods=["POST"])
def advance_tick():
    """Advance the simulation by N ticks (default 1)."""
    n = request.json.get("ticks", 1) if request.is_json else 1
    n = max(1, min(n, 1000))
    for _ in range(n):
        state = ecosystem.tick()
    return jsonify(state)


@app.route("/api/simulation/state", methods=["GET"])
def get_state():
    """Get current simulation state."""
    return jsonify(ecosystem.get_state())


@app.route("/api/simulation/history", methods=["GET"])
def get_history():
    """Get population history over all ticks."""
    return jsonify({
        "tick_count": ecosystem.tick_count,
        "history": ecosystem.history,
    })


@app.route("/api/simulation/reset", methods=["POST"])
def reset_simulation():
    """Reset to initial conditions."""
    ecosystem.reset()
    return jsonify(ecosystem.get_state())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
