from flask import Flask,render_template, request, jsonify, session
from tinydb import TinyDB, Query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geslo123'

db=TinyDB('db.json')
notes_table=db.table('notes')

@app.route('/')
def zapiski():
    if "user" in session:
        redirect("/index.html")
    return redirect("/login")
return render_template("register.html")
       
#return render_template('index.html',notes=notes)


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

@app.route('/logout',methods=["GET","POST"])
def logout():
    session.clear()


app.run(debug=True)