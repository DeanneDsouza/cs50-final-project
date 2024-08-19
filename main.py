from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import apology, login_required 
import sqlite3
from flask_session import Session
# create table for storing shares


# Configure application
main = Flask(__name__)

# to creat a database 
connection = sqlite3.connect('user.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, hash TEXT)''')


# Configure session to use filesystem (instead of signed cookies)
main.config["SESSION_PERMANENT"] = False
main.config["SESSION_TYPE"] = "filesystem"
Session(main)

@main.route('/')
@login_required
def home():
    user_id = session["user_id"]
    cursor.execute("SELECT event, date, status FROM events WHERE id = (?) ORDER BY status DESC", (user_id,))
    combined = cursor.fetchall()
    return render_template('home.html', combined = combined)

@main.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')



@main.route('/register', methods=["GET", "POST"])
def register():
    """register user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must provide cpassword", 400)
        elif not password == confirmation:
            return apology("confirm password incorrect", 400)
        try:
            hashpassword = generate_password_hash(password)
            print("Username:", username)
            print("Hashed Password:", hashpassword)
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashpassword))
            connection.commit()
            cursor.execute("SELECT id FROM users WHERE username = (?)", (username,))
            rows= cursor.fetchall()
            user_id = rows[0][0]  # Access the first column of the first row
            session["user_id"] = user_id
            return home()
        except ValueError:
            return apology("error")
    else:
        return render_template('register.html')
    
@main.route("/add", methods = ["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        # Ensure username was submitted
        Event = request.form.get("event_name")
        date = request.form.get("event_date")
        status = request.form.get("status") or "can be done later"
        id = session["user_id"]
        if not Event:
            return apology("must provide the Event", 400)
        # Ensure password was submitted
        elif not date:
            return apology("must provide the day", 400)
        

        cursor.execute("INSERT INTO events (id, event, date, status) VALUES (?, ?, ?, ?)", (id, Event, date, status))
        connection.commit()
        return redirect('/')
    else :
        return render_template('add.html')
    
@main.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@main.route("/CPassword", methods=["GET", "POST"])
def password():
    if request.method == "POST":
        new_password = request.form.get("password")
        if not new_password:
            return apology("Not entered the field", 403)

        confirm_password = request.form.get("confirmation")
        if not confirm_password:
            return apology("Not entered the field", 403)

        user_id = session["user_id"]
        cursor.execute("SELECT hash FROM users WHERE id = (?)", (user_id,))
        passwords  = cursor.fetchall()
        if new_password in passwords:
            return apology("Password already taken, please tyr again", 403)
        
        elif check_password_hash(passwords[0][0], new_password):
            return apology("New password cannot be the same as the old password", 403)
        
        elif (new_password == confirm_password):
            hash_password = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET hash = (?) WHERE id = (?)", (hash_password, user_id))
            connection.commit()
            return redirect('/')
        else:
            return apology("password does not match with the confirmed password try again")
        

    else:
        return render_template("password.html")
    
@main.route('/delete/<id>', methods=['POST'])
def delete(id):
    cursor.execute('DELETE FROM events WHERE event = ?', (id,))
    connection.commit()
    return redirect('/')


if __name__ == "__main__" :
    main.run(debug=True)
