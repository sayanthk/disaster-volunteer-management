from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        location = request.form["location"]
        skills = request.form["skills"]
        experience = request.form["experience"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO volunteers
            (name, email, phone, location, skills, experience, trained, level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, location, skills, experience, 0, 1))

        conn.commit()
        conn.close()

        return "Registration Successful"

    return render_template("register.html")


@app.route("/volunteers")
def volunteers():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM volunteers")
    data = cursor.fetchall()

    conn.close()
    return str(data)


@app.route("/training", methods=["GET", "POST"])
def training():
    if request.method == "POST":
        volunteer_id = request.form["volunteer_id"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE volunteers
            SET trained = 1,
                level = level + 1
            WHERE id = ?
        """, (volunteer_id,))

        conn.commit()
        conn.close()

        return "Training completed successfully"

    return render_template("training.html")


@app.route("/assign", methods=["GET", "POST"])
def assign():
    if request.method == "POST":
        volunteer_id = request.form["volunteer_id"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT trained, level FROM volunteers WHERE id = ?",
            (volunteer_id,)
        )
        result = cursor.fetchone()
        conn.close()

        if result is None:
            return "Volunteer not found"

        trained, level = result

        if trained == 0:
            return "Assignment blocked: Volunteer is NOT trained"

        return f"Volunteer assigned successfully (Level {level})"

    return render_template("assign.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    volunteer = None

    if request.method == "POST":
        volunteer_id = request.form["volunteer_id"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, experience, trained, level
            FROM volunteers
            WHERE id = ?
        """, (volunteer_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            volunteer = {
                "name": row[0],
                "experience": row[1],
                "trained": row[2],
                "level": row[3]
            }

    return render_template("dashboard.html", volunteer=volunteer)

@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, experience, trained, level
        FROM volunteers
    """)
    rows = cursor.fetchall()
    conn.close()

    volunteers = []
    for r in rows:
        volunteers.append({
            "id": r[0],
            "name": r[1],
            "experience": r[2],
            "trained": r[3],
            "level": r[4]
        })

    return render_template("admin.html", volunteers=volunteers)


if __name__ == "__main__":
    app.run(debug=True)
