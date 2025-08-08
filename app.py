from flask import Flask, render_template, request, redirect, url_for, session, flash
import random

app = Flask(__name__)
app.secret_key = "secret123"

# Temporary "database" (in-memory)
users = {
    "john": {"name": "John Doe", "password": "123", "birthday": "2000-01-01", "photo": "https://via.placeholder.com/150"},
    "jane": {"name": "Jane Smith", "password": "456", "birthday": "1998-05-10", "photo": "https://via.placeholder.com/150"}
}

# -------------------- Public Routes --------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        if username in users:
            flash("Username already exists!", "error")
            return redirect(url_for("register"))

        # Add user
        users[username] = {
            "name": name,
            "password": password,
            "birthday": "",
            "photo": "https://via.placeholder.com/150"
        }
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

# -------------------- Logged-in Routes --------------------

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/profile/<username>")
def profile(username):
    if username in users:
        return render_template("profile.html", user=users[username], username=username)
    else:
        flash("User not found!", "error")
        return redirect(url_for("dashboard"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"].lower()
        for uname, details in users.items():
            if details["name"].lower() == name:
                return redirect(url_for("view_profile", username=uname))
        flash("No user found with that name!", "error")
        return redirect(url_for("search"))

    return render_template("search.html")

@app.route("/explore")
def explore():
    if "username" not in session:
        return redirect(url_for("login"))

    # Pick a random user (not the current one)
    other_users = [u for u in users.keys() if u != session["username"]]
    if not other_users:
        flash("No other users to explore!", "error")
        return redirect(url_for("dashboard"))

    random_user = random.choice(other_users)
    return redirect(url_for("view_profile", username=random_user))

@app.route("/view/<username>")
def view_profile(username):
    if "username" not in session:
        return redirect(url_for("login"))

    if username in users:
        return render_template("view_profile.html", user=users[username], username=username)
    else:
        flash("User not found!", "error")
        return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
