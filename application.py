import os
import webbrowser
import csv
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

links = {"Math":"math", "Science":"science", "History":"history", "English":"english", "Current Events":"cur_events", "Computer Science":"cs", "Logging in Sessions":"forms"}
creators = {"Math":"Jacob Chen", "Science":"Jack Tsai", "History":"Sabrina Cohen", "English":"Grace Beecher", "Current Events":"Yahel Tamir", "Computer Science":"Aiden Taghinia", "Logging in Sessions":"Yahel & Maxwell"}

Fmath = {"Curriculum":"https://docs.google.com/document/d/1s000raW-xUc1hL9LWiJ1ynI_nMFpOSJi/edit?usp=sharing&ouid=104361955554049195573&rtpof=true&sd=true"}
Fscience = {"Curriculum":"https://docs.google.com/document/d/1679uLXhH-4ZdC4DJ48RnbYsg01eyCl3sGYw4FWT80to/edit?usp=sharing"}
Fenglish = {"Curriculum":"https://docs.google.com/document/d/154eoWTXXEuoMfpLqBBXBs6eJ1DwFpO7RX_lruCDzExE/edit?usp=sharing"}
Fhistory = {"Curriculum":"https://docs.google.com/document/d/1_4F63-2QQf7C0jTqzi2oMcaxIMeRauM7/edit?usp=sharing&ouid=104361955554049195573&rtpof=true&sd=true"}
Fcur_events = {"Curriculum":"https://docs.google.com/document/d/1lbHgTiamPL74ks6uIz0uajkNmrSInRyiAnzucoEEqzw/edit?usp=sharing"}
Fcs = {"Python Curriculum":"https://docs.google.com/document/d/1KYXnl22QtDne1C4Eb8JM7M6lFfbUdE-FwBJn-QwNjVU/edit?usp=sharing"}
Fforms = {"Math":"https://docs.google.com/forms/d/e/1FAIpQLSe_4cS2JbNnRiKf4OiZ7drSTsa9J0Fj_5GvZzgmefxjnKlnlg/viewform", "Science":"https://docs.google.com/forms/d/e/1FAIpQLSd0m1gzv7pOVkzbzUGVnodolVSOHPwDCZScUY3WQpiLmmRbpg/viewform", "History":"https://docs.google.com/forms/d/e/1FAIpQLSezk0oY_5DZYKCRFc_jZl5hfafZcCDwZVO1SpohiJhJLbsaHw/viewform", "English":"https://docs.google.com/forms/d/e/1FAIpQLSfrleN1z_oXtGXLMbLaoSUuWfp1uxr-NoL2BGvXuE-4cm2lQA/viewform"}


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    """Resources"""    
    return render_template("index.html", links=links, creators=creators)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("login.html", error=True, errormsg="Enter a Password")

        pwd = request.form.get("password")
        if str(pwd) != "keepclimbing2":
          return render_template("login.html", error=True, errormsg="Invalid Password")
        session["user_id"] = 2022

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", error=False)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    
  
@app.route("/math")
@login_required
def math():
    """Math"""
    return render_template("math.html", folder=Fmath)
    
    
@app.route("/science")
@login_required
def science():
    """Science"""
    return render_template("science.html", folder=Fscience)
    

@app.route("/english")
@login_required
def english():
    """English"""
    return render_template("english.html", folder=Fenglish)
    
    
@app.route("/history")
@login_required
def history():
    """History"""
    return render_template("history.html", folder=Fhistory)


@app.route("/cur_events")
@login_required
def cur_events():
    """Current Events"""
    return render_template("cur_events.html", folder=Fcur_events)
    

@app.route("/cs")
@login_required
def cs():
    """Computer Science"""
    return render_template("cs.html", folder=Fcs)
    

@app.route("/forms")
@login_required
def forms():
    """Past Tutoring Session Forms"""
    return render_template("forms.html", folder=Fforms)
    

def error(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)
    
    
# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)