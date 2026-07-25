from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

# In-memory "database" for demo purposes
tasks = [
    {"id": 1, "title": "Learn Docker", "done": False},
    {"id": 2, "title": "Set up CI/CD", "done": False},
]


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint used by monitoring / container orchestration."""
    return jsonify({"status": "ok"}), HTTPStatus.OK


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), HTTPStatus.OK


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), HTTPStatus.NOT_FOUND
    return jsonify(task), HTTPStatus.OK


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), HTTPStatus.BAD_REQUEST

    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": data["title"], "done": False}
    tasks.append(new_task)
    return jsonify(new_task), HTTPStatus.CREATED


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), HTTPStatus.NOT_FOUND
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"}), HTTPStatus.OK


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
