import urllib.request
import json
from flask import Flask, render_template

app = Flask(__name__)    #create Flask object

@app.route("/")
def main_page():
    return render_template('/templates/home.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
