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

pfps = ['https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdo.lolwot.com%2Fwp-content%2Fuploads%2F2015%2F06%2F20-of-the-most-evil-cats-youll-ever-see-11.jpg&f=1&nofb=1&ipt=7b4168f197edce4122be7002d6d0ee88e9e9e73d0fd2ae603a2fcf147e98f723',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2F236x%2F40%2F09%2Ff1%2F4009f1324d775dd5c1f566282e3cc71c.jpg%3Fnii%3Dt&f=1&nofb=1&ipt=5cce8cff0671f80be2eb8c2ebf3bb21c956c71eeb29bba238ce238d6036b8046',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.tenor.com%2Fg7-y0PzwFYUAAAAM%2Fdevious-evil-cat.gif&f=1&nofb=1&ipt=01a19b982824a2f0cbe49a02788a77a0da89145dc962cee67e38295894a0c205',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2F736x%2F7a%2F22%2F88%2F7a22882b3f70fa099068f71716f32994.jpg&f=1&nofb=1&ipt=1232fbbb73aed544069044f0850d988d179abe20b7f4f443d256fe4244ff5f7b',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Ffe%2F55%2F84%2Ffe55842fb719c1deed66398848b35c5c.jpg&f=1&nofb=1&ipt=8e7d7dd916eaf4f92ef8df464e751805a153e95c1c69e79638186ff4c1ab0ffd',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.boredpanda.com%2Fblog%2Fwp-content%2Fuploads%2F2017%2F03%2FEvil-Cats-Demons-Summoning-Satan-102-58d0d5127832f__700.jpg&f=1&nofb=1&ipt=926a872dff64013519cef2372f2c0b86e25c72d035d90d74a8866f523607baae']

# HTML PAGES
# LANDING PAGE
@app.route('/')
def homepage():
    if not 'u_rowid' in session:
        return redirect("/login")
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = f"SELECT * FROM user_base ORDER BY wins DESC LIMIT 5;"
        c.execute(query)
        data = c.fetchall()
        leaderboard = [[1, data[0][2], data[0][0], data[0][6]],
                            [2, data[1][2], data[1][0], data[1][6]],
                            [3, data[2][2], data[2][0], data[2][6]],
                            [4, data[3][2], data[3][0], data[3][6]],
                            [5, data[4][2], data[4][0], data[4][6]],]
        print(data[0][6])
        return render_template("home.html", leaderboard=leaderboard, user = fetch("user_base", f"ROWID={session['u_rowid'][0]}", "username")[0][0], tuna = fetch("user_base", f"ROWID={session['u_rowid'][0]}", "cash")[0][0], wins = fetch("user_base", f"ROWID={session['u_rowid'][0]}", "wins")[0][0])

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
            nums = [random.randrange(500, 3000), random.randrange(500, 3000), random.randrange(500, 3000)]
            resp2 = resp2.read().decode()
            json_obj2 = json.loads(resp2)
            print(json_obj2)

            if (nums[0] > data):
                cats.append([json_obj2[0]['word'].split()[0], json_obj[0]['url'], nums[0], 'disabled'])
            else:
                cats.append([json_obj2[0]['word'].split()[0], json_obj[0]['url'], nums[0], ''])
            if (nums[1] > data):
                cats.append([json_obj2[1]['word'].split()[0], json_obj[1]['url'], nums[1], 'disabled'])
            else:
                cats.append([json_obj2[1]['word'].split()[0], json_obj[1]['url'], nums[1], ''])
            if (nums[2] > data):
                cats.append([json_obj2[2]['word'].split()[0], json_obj[2]['url'], nums[2], 'disabled'])
            else:
                cats.append([json_obj2[2]['word'].split()[0], json_obj[2]['url'], nums[2], ''])

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
    profcheck = False

    if int(u_rowid) == int(session['u_rowid'][0]):
        profcheck = True

    if request.method=='POST':
        if 'pfp' in request.form:
            update_pfp(request.form['pfp'], u_rowid)
            return redirect(f"/profile/{u_rowid}")
        else:
            edit = f"<form method='POST' action={u_rowid} id='PFPform' class='btn-dark' >"
            for pfp in pfps:
                edit += f"""<button type='submit' name='pfp' class='btn-dark' value={pfp}>
                <img src={pfp} alt='profile choice' class='image' style='height:120px;'>
                </button>"""
            edit += "</form>"

    else:
        edit = f"""<form method='POST' action={u_rowid}  class='btn-dark'>
        <input type='Image' name='Change PFP' value='Change PFP'>
        </form>"""

    #get cat list
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    inv_list = fetch("user_base", f"ROWID={u_rowid}", "inv")
    inv_list = inv_list[0][0].split()
    cat_list = []
    print(inv_list)
    for cat in inv_list:
        query = f"SELECT * FROM cats WHERE id=\'{cat}\';"
        c.execute(query)
        cats = c.fetchall()
        if not (len(cats) == 0):
                print("Cats: " + str(cats))
                cat_list.append(list(cats[0]))

    # renders page
    return render_template("profile.html",
        username=u_data[0],
        own_profile=profcheck,
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
            query = f"UPDATE user_base SET cash = cash - {request.form['theBet']} WHERE rowid={session['u_rowid'][0]}"
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
    won = request.args.get('win')
    if won == 'true':
        query = f"UPDATE user_base SET wins = wins + 1 where rowid = {session['u_rowid'][0]}"
        c.execute(query)
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
