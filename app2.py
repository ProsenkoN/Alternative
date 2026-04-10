from flask import Flask,render_template, request, jsonify, session, redirect
from tinydb import TinyDB, Query
import os
app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)

app.config['SECRET_KEY'] = 'žabaracarak'

db=TinyDB('db2.json')
notes_table=db.table('notes')
users = db.table('users')
slike = db.table('slika')
User = Query()

@app.route('/')
def zapiski():
    print("zapiski")
    if "user" not in session:
        #redirect("/index.html")
        return redirect("/login")
        
    print(session)
    user = users.get(User.username == session["user"])
    note=user.get('note'," ")
    notes = user.get("notes", {})
    #return render_templates("register.html")
    #return render_template('index.html',notes=notes, note=note, uporabnik=session["user"])
    return render_template('index.html',notes=notes, uporabnik=session["user"],slika=slike)
    #return redirect("/logout")
#return render_template('index.html',notes=notes)

@app.route("/dodajZapisek",methods=["POST"])
def nekej():
    note = request.form["note"]
    user = users.get(User.username == session["user"])
    notes = user.get("notes", {})
    notes[f"note{len(notes) + 1}"] = note
    users.update({"notes": notes}, User.username == session["user"])
    return redirect('/')
    #users.update(["note" : note], User.username == session["user"])
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        user = users.get((User.username == username) & (User.password == password))
        print(user)
        if user and user["password"] == password:
            session["user"] = username
            return redirect('/')
        else:
            return "Napačno uporabniško ime ali geslo!"

    return render_template('login.html')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        ze_obstaja = users.get(User.username == username)
        if ze_obstaja:
            return "Uporabnik že obstaja!"
        users.insert({
            "username": username,
            "password": password,
            "notes": {},
            "slike":slika
        })

        return redirect("/login")

    return render_template('register.html')
    
    #return render_template('register.html')
@app.route('/dodajSLIKO', methods=["POST"])
def dodajSLIKO():
    if 'slika' not in request.files:
        return redirect('/index.html')
    file = request.files['slika']

    if file.filename == '':
        return redirect('/index.html')

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        user = users.get(User.username == session["user"])
        user["profile_picture"] = filename
        users.update(user, User.username == session["user"])
        #return redirect('/index.html)
        #slika[f"slike{len(slika) + 1}"] = slike
        #slika je vrednost, slike so mapa
        return redirect('/')
    #note = request.form["note"]
    #user = users.get(User.username == session["user"])
    #notes = user.get("notes", {})
    #notes[f"note{len(notes) + 1}"] = note
    #users.update({"notes": notes}, User.username == session["user"])
    #return redirect('/')
    #users.update(["note" : note], User.username == session["user"])
@app.route('/logout',methods = ["POST"])
def logout():
    session.clear()
    return redirect("/login")

app.run(debug=True)