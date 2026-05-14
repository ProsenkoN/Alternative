from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB, Query
import os

app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)

app.config["SECRET_KEY"] = "zabaracarak"

UPLOAD_FOLDER = "static2/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    print("Napaka: static2/uploads obstaja, ampak ni mapa.")
else:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

db = TinyDB("db2.json")
users = db.table("users")
User = Query()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def zapiski():
    if "user" not in session:
        return redirect("/login")

    trenutni_user = users.get(User.username == session["user"])

    if not trenutni_user:
        session.clear()
        return redirect("/login")

    moje_notes = trenutni_user.get("notes", {})
    image_url = trenutni_user.get("profile_picture", "")

    vse_objave = []

    for user in users.all():
        username = user.get("username")
        notes = user.get("notes", {})
        profile_picture = user.get("profile_picture", "")

        for ime, vsebina in notes.items():
            vse_objave.append({
                "uporabnik": username,
                "vsebina": vsebina,
                "slika": profile_picture
            })

    return render_template(
        "index.html",
        notes=moje_notes,
        vse_objave=vse_objave,
        uporabnik=session["user"],
        image_url=image_url
    )


@app.route("/dodajZapisek", methods=["POST"])
def dodaj_zapisek():
    if "user" not in session:
        return redirect("/login")

    note = request.form["note"]

    user = users.get(User.username == session["user"])
    notes = user.get("notes", {})

    notes[f"note{len(notes) + 1}"] = note

    users.update({"notes": notes}, User.username == session["user"])

    return redirect("/")


@app.route("/dodajSLIKO", methods=["POST"])
def dodaj_sliko():
    if "user" not in session:
        return redirect("/login")

    if "slika" not in request.files:
        return redirect("/")

    file = request.files["slika"]

    if file.filename == "":
        return redirect("/")

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        image_url = "/" + filepath.replace("\\", "/")

        users.update(
            {"profile_picture": image_url},
            User.username == session["user"]
        )

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get((User.username == username) & (User.password == password))

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Napačno uporabniško ime ali geslo!"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ze_obstaja = users.get(User.username == username)

        if ze_obstaja:
            return "Uporabnik že obstaja!"

        users.insert({
            "username": username,
            "password": password,
            "notes": {},
            "profile_picture": ""
        })

        return redirect("/login")

    return render_template("register.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)

