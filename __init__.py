import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect

# Flask
app = Flask(__name__)
app.secret_key = 'supersecre'

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS user_base(username TEXT, password TEXT, pfp TEXT, path TEXT, inv TEXT, cash INTEGER, wins INTEGER);")

db.commit()
db.close()

pfps = ['https://cdn2.thecatapi.com/images/a20.jpg']

# HTML PAGES
# LANDING PAGE
@app.route('/')
def homepage():
    if not 'u_rowid' in session:
        return redirect("/login")
    return render_template("home.html")

# USER INTERACTIONS
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        usernames = [row[0] for row in fetch("user_base", "TRUE", "username")]
        # SIGNING IN
        if not request.form['username'] in usernames:
            return render_template("login.html",
                error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>",
                normal=True)
        elif request.form['password'] != fetch("user_base",
                                f"username = \"{request.form['username']}\"",
                                "password")[0][0]:
                return render_template("login.html",
                    error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>",
                    normal=True)
        else:
            session["u_rowid"] = fetch("user_base",
                                f"username = \"{request.form['username']}\"",
                                "rowid")[0]
    if 'u_rowid' in session:
        return redirect("/")
    return render_template("login.html", normal=True)

@app.route('/store', methods=["GET", "POST"])
def store():
    if request.method == 'POST':
        return render_template("store.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("u_rowid", None)
    return redirect("/login")

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'u_rowid' in session:
        return redirect("/")
    if request.method == "POST":
        if not request.form['password'] == request.form['confirm']:
            return render_template("register.html",
                                   error="Passwords do not match, please try again! <br><br>")
        if not create_user(request.form['username'], request.form['password']):
            return render_template("register.html",
                                   error="Username already taken, please try again! <br><br>")
        else:
            return redirect("/login")
    return render_template("register.html")

@app.route('/profile', methods=["GET", "POST"])
def profileDefault():
    print("inprofile")
    if not 'u_rowid' in session:
        return redirect("/login")
    return redirect(f"/profile/{session['u_rowid'][0]}")

@app.route('/profile/<u_rowid>', methods=["GET", "POST"]) # makes u_rowid a variable that is passed to the function
def profile(u_rowid):
    # session.clear()
    if not 'u_rowid' in session and session['u_rowid'] == u_rowid:
        return redirect("/login")

    u_data = fetch('user_base',
                   f"ROWID={u_rowid}",
                   'username, pfp')[0]
    # pfp editing
    if request.method=='POST':
        if 'pfp' in request.form:
            update_pfp(request.form['pfp'], u_rowid)
            return redirect(f"/profile/{u_rowid}")
        else:
            edit = f"<form method='POST' action={u_rowid} id='PFPform'>"
            for pfp in pfps:
                edit += f"""<button type='submit' name='pfp' class='ibutton' value={pfp}>
                <img src={pfp} alt='profile choice' class='image'>
                </button>"""
            edit += "</form>"
    else:
        edit = f"""<form method='POST' action={u_rowid}>
        <input type='Image' src='/static/edit.png' name='Change PFP'>
        </form>"""

    # renders page
    return render_template("profile.html",
        username=u_data[0],
        pfp=u_data[1],
        pfps=pfps,
        edit=edit,
        balance=fetch("user_base", f"ROWID={u_rowid}", "cash")[0][0],
        wins=fetch("user_base", f"ROWID={u_rowid}", "wins")[0][0])

@app.route('/slots')
def slots():
    return render_template('slots.html')

# HELPER FUNCTIONS
def fetch(table, criteria, data):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria};"
    c.execute(query)
    data = c.fetchall()
    db.commit()
    db.close()
    return data

def create_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM user_base")
    list = [username[0] for username in c.fetchall()]
    if not username in list:
        # creates user in table
        pfp = random.choice(pfps)
        c.execute(f"INSERT INTO user_base VALUES(\'{username}\', \'{password}\', \'{pfp}\', 'temp', '', 1000, 0)")

        # set path
        c.execute(f"SELECT rowid FROM user_base WHERE username=\'{username}\'")
        c.execute(f"UPDATE user_base SET path = '/profile/{c.fetchall()[0][0]}' WHERE username=\'{username}\'")
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def update_pfp(pfp, u_rowid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(f"UPDATE user_base SET pfp = \'{pfp}\' WHERE ROWID=\'{u_rowid}\'")
    db.commit()
    db.close()

def update_password(pw, username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(f"UPDATE user_base SET password = \'{pw}\' WHERE username=\'{username}\'")
    db.commit()
    db.close()

def update_inv(user, cashUpdt, newCash, invUpdt, newItem):
#cashUpdt and invUpdt are -1, 0, or 1
#-1 indicates subtraction of cash or an item
#0 indicates no change
#1 indicates addition of cash or item
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()


# Flask
if __name__=='__main__':
    app.debug = True
    app.run()
