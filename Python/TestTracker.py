from flask import Flask, render_template_string, request, redirect, flash, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "testtracker123"

# Simulated database
tasks = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🧪 Advanced Testing Task Tracker</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f9f9f9; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
        th { background-color: #eee; }
        .status-passed { color: green; font-weight: bold; }
        .status-failed { color: red; font-weight: bold; }
        .status-pending { color: orange; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🧪 Advanced Testing Task Tracker</h1>

    <form method="POST" action="/add">
        <input type="text" name="name" placeholder="Test Case Title" required>
        <input type="text" name="description" placeholder="Test Description" required>
        <select name="status">
            <option value="Pending">Pending</option>
            <option value="Passed">Passed</option>
            <option value="Failed">Failed</option>
        </select>
        <button type="submit">Add Test</button>
    </form>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <table>
        <tr>
            <th>#</th>
            <th>Test Case</th>
            <th>Description</th>
            <th>Status</th>
            <th>Created At</th>
            <th>Actions</th>
        </tr>
        {% for task in tasks %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ task['name'] }}</td>
            <td>{{ task['description'] }}</td>
            <td class="status-{{ task['status']|lower }}">{{ task['status'] }}</td>
            <td>{{ task['timestamp'] }}</td>
            <td>
                <a href="/edit/{{ loop.index0 }}">Edit</a> |
                <a href="/delete/{{ loop.index0 }}" onclick="return confirm('Are you sure?');">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    description = request.form["description"]
    status = request.form["status"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.append(
        {
            "name": name,
            "description": description,
            "status": status,
            "timestamp": timestamp,
        }
    )
    flash("Test case added successfully!")
    return redirect(url_for("home"))


@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(tasks):
        del tasks[index]
        flash("Test case deleted.")
    return redirect(url_for("home"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    if request.method == "POST":
        tasks[index]["name"] = request.form["name"]
        tasks[index]["description"] = request.form["description"]
        tasks[index]["status"] = request.form["status"]
        flash("Test case updated!")
        return redirect(url_for("home"))

    task = tasks[index]
    edit_form = f"""
    <h2>Edit Test Case</h2>
    <form method="POST">
        <input type="text" name="name" value="{task['name']}" required>
        <input type="text" name="description" value="{task['description']}" required>
        <select name="status">
            <option value="Pending" {'selected' if task['status']=='Pending' else ''}>Pending</option>
            <option value="Passed" {'selected' if task['status']=='Passed' else ''}>Passed</option>
            <option value="Failed" {'selected' if task['status']=='Failed' else ''}>Failed</option>
        </select>
        <button type="submit">Update</button>
    </form>
    <a href="/">Back to Home</a>
    """
    return render_template_string(edit_form)


if __name__ == "__main__":
    app.run(debug=True)
