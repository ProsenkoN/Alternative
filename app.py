from flask import Flask,render_template, request, jsonify, session
from tinydb import TinyDB, Query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geslo123'

db=TinyDB('db.json')
notes_table=db.table('notes')

@app.route('/')
def zapiski():
    if "user" not in session:
        #redirect("/index.html")
        return redirect("/login")
    user = users.get(User.username == session["user"])
    note=user.get('note'," ")
    #return render_templates("register.html")
    return render_template('index.html',notes=notes, note=note, uporabnik=session["user"])
#return render_template('index.html',notes=notes)

@app.route("/nekej",methods=["POST"])
def nekej():
    note = request.form[note]
    print(note)
    users.update(["note" : note], User.username == session["user"])
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        user = users_table.get((User.username == username) & (User.password == password))
        print(user)
        if user and user["password"] == username:
            session["user"] = username

        if user:
            session['username'] = username
            return redirect('/')
        else:
            return "Napačno uporabniško ime ali geslo!"

    return render_template('login.html')

@app.route('/register',methods=["GET","POST"])

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

app.run(debug=True)