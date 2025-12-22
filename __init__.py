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

c.execute("CREATE TABLE IF NOT EXISTS cats(id TEXT, img TEXT, cost INT);")

def create_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM user_base")
    list = [username[0] for username in c.fetchall()]
    if not username in list:
        # creates user in table
        pfp = random.choice(pfps)
        c.execute("INSERT INTO user_base VALUES(?, ?, ?, 'temp', '', 3000, 0)", (username, password, pfp))

        # set path
        c.execute("SELECT rowid FROM user_base WHERE username=?", (username,))
        rowid = c.fetchall()[0][0]
        c.execute("UPDATE user_base SET path = ? WHERE username=?", (f'/profile/{rowid}', username))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False


pfps = ['https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdo.lolwot.com%2Fwp-content%2Fuploads%2F2015%2F06%2F20-of-the-most-evil-cats-youll-ever-see-11.jpg&f=1&nofb=1&ipt=7b4168f197edce4122be7002d6d0ee88e9e9e73d0fd2ae603a2fcf147e98f723',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2F236x%2F40%2F09%2Ff1%2F4009f1324d775dd5c1f566282e3cc71c.jpg%3Fnii%3Dt&f=1&nofb=1&ipt=5cce8cff0671f80be2eb8c2ebf3bb21c956c71eeb29bba238ce238d6036b8046',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.tenor.com%2Fg7-y0PzwFYUAAAAM%2Fdevious-evil-cat.gif&f=1&nofb=1&ipt=01a19b982824a2f0cbe49a02788a77a0da89145dc962cee67e38295894a0c205',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2F736x%2F7a%2F22%2F88%2F7a22882b3f70fa099068f71716f32994.jpg&f=1&nofb=1&ipt=1232fbbb73aed544069044f0850d988d179abe20b7f4f443d256fe4244ff5f7b',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Ffe%2F55%2F84%2Ffe55842fb719c1deed66398848b35c5c.jpg&f=1&nofb=1&ipt=8e7d7dd916eaf4f92ef8df464e751805a153e95c1c69e79638186ff4c1ab0ffd',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.boredpanda.com%2Fblog%2Fwp-content%2Fuploads%2F2017%2F03%2FEvil-Cats-Demons-Summoning-Satan-102-58d0d5127832f__700.jpg&f=1&nofb=1&ipt=926a872dff64013519cef2372f2c0b86e25c72d035d90d74a8866f523607baae']

#ensures that leaderboard works bc there are enough accounts
create_user('ashley', 'ashley')
create_user('nataliee', 'natalie')
create_user('bogdan', 'bogdan')
create_user('haowen', 'haowen')


db.commit()
db.close()

# HTML PAGES
# LANDING PAGE
@app.route('/')
def homepage():
    if not 'u_rowid' in session:
        return redirect("/login")
    else:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        user_data = fetch("user_base", "ROWID=?", "cash", (session['u_rowid'][0],))
        if not user_data:
            session.pop("u_rowid", None)
            return redirect('/login')
        cash = user_data[0][0]
        c.execute("DELETE FROM user_base WHERE cash < 0;")
        if (cash <= 0):
            session.pop("u_rowid", None)
            db.commit()
            db.close()
            return redirect('/login')
        query = "SELECT * FROM user_base ORDER BY wins DESC LIMIT 5;"
        c.execute(query)
        leaderboard = []
        data = c.fetchall()
        db.commit()
        db.close()
        print(data)
        if (len(data) > 4):
            leaderboard = [[1, data[0][2], data[0][0], data[0][6], data[0][3]],
                                [2, data[1][2], data[1][0], data[1][6], data[1][3]],
                                [3, data[2][2], data[2][0], data[2][6], data[2][3]],
                                [4, data[3][2], data[3][0], data[3][6], data[3][3]],
                                [5, data[4][2], data[4][0], data[4][6], data[4][3]]]
            print(data[0][3])
        if request.args.get('error') == 'storefail':
            return render_template("home.html", leaderboard=leaderboard, user = fetch("user_base", "ROWID=?", "username", (session['u_rowid'][0],))[0][0], tuna = fetch("user_base", "ROWID=?", "cash", (session['u_rowid'][0],))[0][0], wins = fetch("user_base", "ROWID=?", "wins", (session['u_rowid'][0],))[0][0], error='Store could not be loaded.')
        return render_template("home.html", leaderboard=leaderboard, user = fetch("user_base", "ROWID=?", "username", (session['u_rowid'][0],))[0][0], tuna = fetch("user_base", "ROWID=?", "cash", (session['u_rowid'][0],))[0][0], wins = fetch("user_base", "ROWID=?", "wins", (session['u_rowid'][0],))[0][0])

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
                                "username = ?",
                                "password", (request.form['username'],))[0][0]:
                return render_template("login.html",
                    error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>",
                    normal=True)
        else:
            session["u_rowid"] = fetch("user_base",
                                "username = ?",
                                "rowid", (request.form['username'],))[0]
    if 'u_rowid' in session:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        db.commit()
        db.close()
        return redirect("/")
    return render_template("login.html", normal=True)

@app.route('/store', methods=["GET", "POST"])
def store():
    if request.method == 'POST':

        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = "SELECT cash FROM user_base WHERE rowid=?;"
        c.execute(query, (session['u_rowid'][0],))
        cash = c.fetchall()[0][0]
        if (int(cash) > 50):
            query = "UPDATE user_base SET cash = cash - 50 WHERE rowid=?"
            c.execute(query, (session['u_rowid'][0],))
        else:
            db.close()
            return redirect('/store')
        db.commit()
        db.close()
    try:
        with urllib.request.urlopen('https://api.thecatapi.com/v1/images/search?limit=3') as resp:
            with urllib.request.urlopen('https://random-words-api.kushcreates.com/api?words=3') as resp2:
                resp = resp.read().decode()
                cats = []
                json_obj = json.loads(resp)

                db = sqlite3.connect(DB_FILE)
                c = db.cursor()
                query = "SELECT cash FROM user_base WHERE rowid=?;"
                c.execute(query, (session['u_rowid'][0],))
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
    except urllib.error.URLError as e:
        print(e.reason)
        return redirect('/?error=storefail')

@app.route('/buy', methods=["GET", "POST"]) #takes in cat image and name like /buy?id=XXimage=XX&cost=XX
def buy():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = "SELECT inv FROM user_base WHERE rowid=?;"
        id = request.args['id']
        query = "UPDATE user_base SET inv = inv || ' ' || ? WHERE rowid=?;" #adds cat name to inventory
        c.execute(query, (id, session['u_rowid'][0]))
        query = "INSERT INTO cats VALUES(?, ?, ?);" #adds cat with name and link to db to be accessed later
        c.execute(query, (request.args['id'], request.args['img'], request.args['cost']))
        query = "SELECT cash FROM user_base WHERE rowid=?;"
        c.execute(query, (session['u_rowid'][0],))
        cash = c.fetchall()[0][0]
        query = "UPDATE user_base SET cash = cash - ?;" #takes money
        c.execute(query, (request.args['cost'],))
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
                   "ROWID=?",
                   'username, pfp', (u_rowid,))[0]
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
    inv_list = fetch("user_base", "ROWID=?", "inv", (u_rowid,))
    inv_list = inv_list[0][0].split()
    cat_list = []
    for cat in inv_list:
        query = "SELECT * FROM cats WHERE id=?;"
        c.execute(query, (cat,))
        cats = c.fetchall()
        if not (len(cats) == 0):
                cat_list.append(list(cats[0]))

    # renders page
    return render_template("profile.html",
        username=u_data[0],
        own_profile=profcheck,
        pfp=u_data[1],
        pfps=pfps,
        edit=edit,
        balance=fetch("user_base", "ROWID=?", "cash", (u_rowid,))[0][0],
        wins=fetch("user_base", "ROWID=?", "wins", (u_rowid,))[0][0],
        inventory = cat_list)

@app.route('/poker', methods=['GET', 'POST'])
def poker():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = "SELECT cash FROM user_base WHERE rowid=?;"
        c.execute(query, (session['u_rowid'][0],))
        cash = c.fetchall()[0][0]
        if (int(cash) >= int(request.form['theBet'])):
            query = "UPDATE user_base SET cash = cash - ? WHERE rowid=?"
            c.execute(query, (request.form['theBet'], session['u_rowid'][0]))
        else:
            db.close()
            return redirect('/poker')
        db.commit()
        db.close()
        return render_template('poker.html', bet=request.form['theBet'], dealButton="<br><button id = 'start-btn' class='btn btn-success btn-lg' onclick='Setup()'>Deal</button>")
    return render_template('poker.html', dealButton="")

@app.route('/blj', methods=['GET', 'POST'])
def blj():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = "SELECT cash FROM user_base WHERE rowid=?;"
    c.execute(query, (session['u_rowid'][0],))
    cash = c.fetchall()[0][0]
    if request.method == 'POST':
        if (int(cash) >= int(request.form['theBet'])):
            query = "UPDATE user_base SET cash = cash - ? WHERE rowid=?"
            c.execute(query, (request.form['theBet'], session['u_rowid'][0]))
        else:
            db.close()
            return redirect('/blj')
        db.commit()
        db.close()
        return render_template('blj.html', won=cash-int(request.form['theBet']), bet=request.form['theBet'], dealButton="<button id = 'start-btn' class='btn btn-success btn-lg' onclick='startGame()'>Start New Game</button> <button id = 'hit-btn' class='btn btn-warning btn-lg' onclick='hit()'>Hit</button> <button id = 'stand-btn' class='btn btn-danger btn-lg' onclick='stand()'>Stand</button>")
    db.commit()
    db.close()
    return render_template('blj.html', dealButton="", won=cash)

@app.route('/slots')
def slots():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = "SELECT cash FROM user_base WHERE rowid=?"
    c.execute(query, (session['u_rowid'][0],))
    data = c.fetchall()
    db.commit()
    db.close()
    return render_template('slots.html', won=data[0][0])

@app.route('/rl', methods=["GET", "POST"])
def rl():
    if not 'u_rowid' in session:
        return redirect("/login")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = "SELECT cash FROM user_base WHERE rowid=?"
    c.execute(query, (session['u_rowid'][0],))
    data = c.fetchall()
    db.commit()
    db.close()
    return render_template('rl.html', won=data[0][0])
    
@app.route('/addtuna', methods=['POST'])
def addtuna():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    tuna = request.args.get('num')
    won = request.args.get('win')
    cash = fetch("user_base", "ROWID=?", "cash", (session['u_rowid'][0],))[0][0]
    if (cash < -(int(tuna))):
        print('a')
        user = fetch("user_base", "ROWID=?", "username", (session['u_rowid'][0],))[0][0]
        check_ban(user, '/addtuna?num=num&win=false')
    if won == 'true':
        query = "UPDATE user_base SET wins = wins + 1 where rowid = ?"
        c.execute(query, (session['u_rowid'][0],))
    query = "UPDATE user_base SET cash = cash + ? where rowid = ?"
    c.execute(query, (tuna, session['u_rowid'][0]))
    query = "SELECT cash FROM user_base WHERE rowid=?"
    c.execute(query, (session['u_rowid'][0],))
    data = c.fetchall()
    db.commit()
    db.close()
    return data


@app.route('/sound')
def sound():
    return send_file('cha-ching.mp3')

# HELPER FUNCTIONS
def fetch(table, criteria, data, params=()):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria};"
    print(query)
    c.execute(query, params)
    data = c.fetchall()
    db.commit()
    db.close()
    return data



def update_pfp(pfp, u_rowid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE user_base SET pfp = ? WHERE ROWID=?", (pfp, u_rowid))
    db.commit()
    db.close()

def update_password(pw, username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE user_base SET password = ? WHERE username=?", (pw, username))
    db.commit()
    db.close()

def update_inv(user, cashUpdt, newCash, invUpdt, newItem):
#cashUpdt and invUpdt are -1, 0, or 1
#-1 indicates subtraction of cash or an item
#0 indicates no change
#1 indicates addition of cash or item
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    curCash = fetch("user_base", "ROWID=?", "cash", (user,))[0][0]+newCash*cashUpdt
    curInv = fetch("user_base", "ROWID=?", "inv", (user,))[0][0]
    if (invUpdt==1):
        curInv += f", {newItem}"
    elif (invUpdt==-1):
        curInv = curInv.replace(f"{newItem}, ", "")
    c.execute("UPDATE user_base SET cash = ? WHERE username=?", (curCash, user))
    c.execute("UPDATE user_base SET inv = ? WHERE username=?", (curInv, user))
    db.commit()
    db.close()

def check_ban(username, original_link):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    curCash = fetch("user_base", "username=?", "cash", (username,))[0][0]
    if (curCash <= 0):
        c.execute("DELETE FROM user_base WHERE username=?;", (username,))
        db.commit()
        db.close()
        return redirect('/login')
    db.commit()
    db.close()
    return redirect(original_link)

# Flask
if __name__=='__main__':
    app.debug = True
    app.run()
