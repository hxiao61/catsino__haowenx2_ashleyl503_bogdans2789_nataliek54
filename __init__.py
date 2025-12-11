import sqlite3
import random
import urllib.request
import json
from flask import Flask, render_template, send_file
from flask import session, request, redirect

# Flask
app = Flask(__name__)
app.secret_key = 'supersecre'

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS user_base(username TEXT, password TEXT, pfp TEXT, path TEXT, inv TEXT, cash INTEGER, wins INTEGER);")
c.execute("INSERT INTO user_base VALUES('user', 'pass', 'pfp', '1', 'temp', 1000, 0);")

c.execute("CREATE TABLE IF NOT EXISTS cats(id TEXT, img TEXT, cost INT);")


db.commit()
db.close()

pfps = ['https://cdn2.thecatapi.com/images/a20.jpg']

# HTML PAGES
# LANDING PAGE
@app.route('/')
def homepage():
    if not 'u_rowid' in session:
        return redirect("/login")
    return render_template("home.html", user = fetch("user_base", f"ROWID={session['u_rowid'][0]}", "username")[0][0], tuna = fetch("user_base", f"ROWID={session['u_rowid'][0]}", "cash")[0][0], wins = fetch("user_base", f"ROWID={session['u_rowid'][0]}", "wins")[0][0])

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

        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = f"SELECT cash FROM user_base WHERE rowid={session['u_rowid'][0]};"
        c.execute(query)
        cash = c.fetchall()[0][0]
        if (int(cash) > 50):
            query = f"UPDATE user_base SET cash = cash - 50 WHERE rowid={session['u_rowid'][0]}"
            c.execute(query)
        else:
            return redirect('/store')
        db.commit()
        db.close()
    #key = open('keys/key_The-Cat-API.txt', 'r').read()
    with urllib.request.urlopen('https://api.thecatapi.com/v1/images/search?limit=3') as resp:
        with urllib.request.urlopen('https://random-words-api.kushcreates.com/api?words=3') as resp2:
            resp = resp.read().decode()
            cats = []
            json_obj = json.loads(resp)

            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            query = f"SELECT cash FROM user_base WHERE rowid={session['u_rowid'][0]};"
            c.execute(query)
            data = int(c.fetchall()[0][0])
            nums = [random.randrange(500, 1500), random.randrange(500, 1500), random.randrange(500, 1500)]
            resp2 = resp2.read().decode()
            json_obj2 = json.loads(resp2)

            if (nums[0] > data):
                cats.append([json_obj2[0]['word'], json_obj[0]['url'], nums[0], 'disabled'])
            else:
                cats.append([json_obj2[0]['word'], json_obj[0]['url'], nums[0], ''])
            if (nums[1] > data):
                cats.append([json_obj2[1]['word'], json_obj[1]['url'], nums[1], 'disabled'])
            else:
                cats.append([json_obj2[1]['word'], json_obj[1]['url'], nums[1], ''])
            if (nums[2] > data):
                cats.append([json_obj2[2]['word'], json_obj[2]['url'], nums[2], 'disabled'])
            else:
                cats.append([json_obj2[2]['word'], json_obj[2]['url'], nums[2], ''])

    print(data)
    db.commit()
    db.close()
    return render_template("store.html", cats=cats, tuna=data)

@app.route('/buy', methods=["GET", "POST"]) #takes in cat image and name like /buy?id=XXimage=XX&cost=XX
def buy():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = f"SELECT inv FROM user_base WHERE rowid={session['u_rowid'][0]};"
        id = request.args['id']
        query = f"UPDATE user_base SET inv = inv || ' ' || \'{id}\' WHERE rowid={session['u_rowid'][0]};" #adds cat name to inventory
        c.execute(query)
        query = f"INSERT INTO cats VALUES(\'{request.args['id']}\', \'{request.args['img']}\', {request.args['cost']});" #adds cat with name and link to db to be accessed later
        c.execute(query)
        query = f"SELECT cash FROM user_base WHERE rowid={session['u_rowid'][0]};"
        c.execute(query)
        cash = c.fetchall()[0][0]
        query = f"UPDATE user_base SET cash = cash - {request.args['cost']};" #takes money
        c.execute(query)
        db.commit()
        db.close()
    return redirect('/store')

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

    #get cat list
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    inv_list = fetch("user_base", f"ROWID={u_rowid}", "inv")
    inv_list = inv_list[0][0].split()
    print(inv_list)
    cat_list = []
    for cat in inv_list:
        query = f"SELECT * FROM cats WHERE id=\'{cat}\';"
        c.execute(query)
        cats = c.fetchall()
        cat_list.append(list(cats[0]))
    print(cat_list)
    # renders page
    return render_template("profile.html",
        username=u_data[0],
        pfp=u_data[1],
        pfps=pfps,
        edit=edit,
        balance=fetch("user_base", f"ROWID={u_rowid}", "cash")[0][0],
        wins=fetch("user_base", f"ROWID={u_rowid}", "wins")[0][0],
        inventory = cat_list)

@app.route('/blj')
def blackjack():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT cash FROM user_base WHERE rowid={session['u_rowid'][0]}"
    c.execute(query)
    data = c.fetchall()
    db.close()
    return render_template('blj.html', won=data[0][0])

@app.route('/poker', methods=['GET', 'POST'])
def poker():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = f"SELECT cash FROM user_base WHERE rowid={session['u_rowid'][0]};"
        c.execute(query)
        cash = c.fetchall()[0][0]
        if (int(cash) > 50):
            query = f"UPDATE user_base SET cash = cash - 50 WHERE rowid={session['u_rowid'][0]}"
            c.execute(query)
        else:
            return redirect('/poker')
        db.commit()
        db.close()
    return render_template('poker.html')

@app.route('/slots')
def slots():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT cash FROM user_base WHERE rowid={session['u_rowid'][0]}"
    c.execute(query)
    data = c.fetchall()
    db.commit()
    db.close()
    return render_template('slots.html', won=data[0][0])

@app.route('/addtuna', methods=['POST'])
def addtuna():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    tuna = request.args.get('num')
    query = f"UPDATE user_base SET cash = cash + {tuna} where rowid = {session['u_rowid'][0]}"
    c.execute(query)
    query = f"SELECT cash FROM user_base WHERE rowid={session['u_rowid'][0]}"
    c.execute(query)
    data = c.fetchall()
    db.commit()
    db.close()
    return data


@app.route('/sound')
def sound():
    return send_file('cha-ching.mp3')

# HELPER FUNCTIONS
def fetch(table, criteria, data):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria};"
    print(query)
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
    curCash = fetch("user_base", f"ROWID={user}", "cash")[0][0]+newCash*cashUpdt
    curInv = fetch("user_base", f"ROWID={user}", "inv")[0][0]
    if (invUpdt==1):
        curInv += f", {newItem}"
    elif (invUpdt==-1):
        curInv = curInv.replace(f"{newItem}, ", "")
    c.execute(f"UPDATE user_base SET cash = \'{curCash}\' WHERE username=\'{user}\'")
    c.execute(f"UPDATE user_base SET inv = \'{curInv}\' WHERE username=\'{user}\'")
    db.commit()
    db.close()

# Flask
if __name__=='__main__':
    app.debug = True
    app.run()
