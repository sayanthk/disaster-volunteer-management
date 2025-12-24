from flask import Flask, render_template, request

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

        print("New Volunteer Registered:")
        print(name, email, phone, location, skills, experience)

        return "Registration Successful"

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
