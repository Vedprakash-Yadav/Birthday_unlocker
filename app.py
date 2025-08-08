from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Fake user data for now
users = [
    {"username": "alice", "password": "123", "name": "Alice Johnson", "photo": "alice.jpg"},
    {"username": "bob", "password": "123", "name": "Bob Smith", "photo": "bob.jpg"},
    {"username": "charlie", "password": "123", "name": "Charlie Brown", "photo": "charlie.jpg"}
]

# ---------- PUBLIC ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        name = request.form.get("name").strip()
        photo = request.form.get("photo").strip()  # filename for now

        if any(u["username"] == username for u in users):
            return render_template("register.html", error="Username already exists")

        users.append({"username": username, "password": password, "name": name, "photo": photo})
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user_data = next((u for u in users if u["username"] == username and u["password"] == password), None)
        if user_data:
            session["user"] = user_data["username"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# ---------- PROTECTED ROUTES ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/profile/<username>")
def profile(username):
    if "user" not in session:
        return redirect(url_for("login"))

    user_data = next((u for u in users if u["username"] == username), None)
    if not user_data:
        return "User not found", 404

    return render_template("profile.html", profile=user_data)

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name").strip().lower()
        user_data = next((u for u in users if name in u["name"].lower()), None)
        if user_data:
            return redirect(url_for("view_profile", username=user_data["username"]))
        return render_template("search.html", not_found=True)

    return render_template("search.html", not_found=False)

@app.route("/explore")
def explore():
    if "user" not in session:
        return redirect(url_for("login"))

    random_user = random.choice([u for u in users if u["username"] != session["user"]])
    return redirect(url_for("view_profile", username=random_user["username"]))

@app.route("/view/<username>")
def view_profile(username):
    if "user" not in session:
        return redirect(url_for("login"))

    profile_user = next((u for u in users if u["username"] == username), None)
    if not profile_user:
        return "User not found", 404

    return render_template("view_profile.html", profile=profile_user)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
