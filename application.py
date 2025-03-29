import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///notes.db")

def is_provided(field):
    if not request.form.get(field):
        return apology(f"must provide {field}", 403)

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        result_checks = is_provided("username") or is_provided("password") or is_provided("confirmation")
        if result_checks != None:
            return result_checks
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match",400)
        try:
            prim_key= db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                    username=request.form.get("username"),
                    hash= generate_password_hash(request.form.get("password")))
        except:
            return apology("username already exists",400)
            if prim_key is None:
                return apology("registration error",400)
            session["user_id"] = prim_key
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username and password was submitted
        result_checks = is_provided("username") or is_provided("password")

        if result_checks is not None:
            return result_checks

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
@login_required
def index():
    notes = db.execute("SELECT * FROM notes WHERE user_id=:user_id",user_id=session["user_id"])
    return render_template("index.html",notes=notes)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        result_checks = is_provided("title") or is_provided("content")
        if result_checks is not None:
            return result_checks
        title = request.form.get("title")
        content = request.form.get("content")
        db.execute("""
            INSERT INTO notes (user_id,title,content)
            VALUES(:user_id, :title, :content)
        """,user_id=session["user_id"],
            title=request.form.get("title"),
            content = request.form.get("content"))

        flash("Added!")
        return redirect("/")

    else:
        return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        result_checks = is_provided("title") or is_provided("titleEdited") or is_provided("content")
        if result_checks is not None:
            return result_checks
        db.execute("""
            UPDATE notes
            SET title=:titleEdited, content=:content
            WHERE title=:title
            """,titleEdited=request.form.get("titleEdited"),
            content=request.form.get("content"),
            title=request.form.get("title"))

        flash("Edited!")
        return redirect("/")
    else:
        return render_template("edit.html")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove notes"""
    if request.method == "POST":
        result_check= is_provided("title")
        if result_check is not None:
            return result_check
        db.execute("delete from notes where title=:title",title=request.form.get("title"))

        flash("Removed!")
        return redirect("/")
    else:
        return render_template("remove.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
