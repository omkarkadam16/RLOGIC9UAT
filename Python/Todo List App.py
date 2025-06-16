from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Temporary task list (resets every time you restart the server)
tasks = []

# HTML template in a string (you can also use separate .html files)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Todo List</title>
</head>
<body>
    <h1>📝 Todo List</h1>

    <form method="POST" action="/add">
        <input type="text" name="task" placeholder="Enter a new task" required>
        <button type="submit">Add Task</button>
    </form>

    <ul>
        {% for task in tasks %}
            <li>
                {{ loop.index }}. {{ task['name'] }} 
                [{{ "✅" if task['done'] else "❌" }}]
                <a href="/done/{{ loop.index0 }}">Mark Done</a> |
                <a href="/delete/{{ loop.index0 }}">Delete</a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    task_name = request.form["task"]
    tasks.append({"name": task_name, "done": False})
    return redirect("/")


@app.route("/done/<int:task_id>")
def mark_done(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
