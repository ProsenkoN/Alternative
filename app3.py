from flask import Flask, render_template, request, session, redirect
import random

app = Flask(
    __name__,
    template_folder="templates3",
#   static_folder="static3"
)

app.secret_key = "secret123"


@app.route("/")
def index():
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["tries"] = 0

    return render_template("index.html")


@app.route("/guess", methods=["POST"])
def guess():
    user_guess = int(request.form["guess"])
    number = session["number"]

    session["tries"] += 1

    if user_guess < number:
        message = "Večja številka"
    elif user_guess > number:
        message = "Manjša številka"
    else:
        message = "Pravilno! Število poskusov: " + str(session["tries"])
        session.pop("number")
        session.pop("tries")

    return render_template("index.html", message=message)


@app.route("/reset")
def reset():
    session.pop("number", None)
    session.pop("tries", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)