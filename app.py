from flask import Flask, render_template, url_for, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from dotenv import load_dotenv
import joblib
import os
import pandas as pd

#activating the essentials
load_dotenv()
model = joblib.load("SalaryPredictorModel.pkl")
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

#activating all of the imp stuff for complete login again
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False, #makes session temporary
    SESSION_PERMANENT=False #makes session temporary
)

#database stuff will come here
db_host = os.getenv("DB_HOST")
db_username = os.getenv("DB_USERNAME")
db_name = os.getenv("DB_NAME")
db_pass = os.getenv("DB_PASSWORD")

#all of the routes
@app.route("/", methods=["POST", "GET"])
def login():
    session.permanent = False
    if request.method == "POST":
        email_login = request.form.get("email")
        password_login = request.form.get("password")
        connection = mysql.connector.connect(
            host=db_host,
            user=db_username,
            password=db_pass,
            database=db_name
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_logs WHERE gmail = %s", (email_login,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            connection.close()
            return render_template("index.html", error_login="No User Found, SignUp")
        elif not check_password_hash(user[3], password_login):
            cursor.close()
            connection.close()
            return render_template("index.html", error_login="Wrong Password")
        else:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["gmail"] = user[2]
            cursor.close()
            connection.close()
            return redirect(url_for("home"))
    return render_template("index.html", error_login=None)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    session.permanent = False
    if request.method == "POST":
        user_name = request.form.get('username')
        email_signup = request.form.get('email')
        password_signup = request.form.get('password')
        hashed_pass = generate_password_hash(password_signup ,method='pbkdf2:sha256', salt_length=10)
        connection = mysql.connector.connect(
            host=db_host,
            user=db_username,
            password=db_pass,
            database=db_name
        )
        cursor = connection.cursor()
        # check if user exists
        cursor.execute("SELECT id FROM user_logs WHERE gmail = %s", (email_signup,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return render_template("signup.html", error_signup="User is already registered, Login")
        
        # insert new user
        cursor.execute(
            "INSERT INTO user_logs (username, gmail, password) VALUES (%s, %s, %s)",
            (user_name, email_signup, hashed_pass)
        )
        connection.commit() 
        cursor.close()
        connection.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout", methods=["POST","GET"])
def logout():
    if "user_id" not in session:   # check session
        return redirect(url_for("login"))
    else:
        session.clear()   # clears all session data
        return redirect(url_for('login'))

@app.route("/home", methods=["POST","GET"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    session.permanent = False
    if request.method == "POST":
        user_age = request.form.get("age")
        user_experience = request.form.get("experience")
        data = pd.DataFrame([[int(user_age), int(user_experience)]], columns=["Age", "Years of Experience"])
        prediction = model.predict(data)[0]
        prediction = round(prediction, 3)
        user_id = session.get("user_id")
        connection = mysql.connector.connect(
            host=db_host,
            user=db_username,
            password=db_pass,
            database=db_name
        )
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users_history 
            (user_id, age, exp_years, prediction) VALUES (%s, %s, %s, %s)""",
            (user_id, user_age, user_experience, prediction))
        connection.commit()
        cursor.close()
        connection.close()
        return render_template("home.html", prediction=prediction)
    return render_template("home.html")

@app.route("/about", methods=["GET"])
def about():
    if "user_id" not in session:
        return redirect(url_for("login"))
    session.permanent = False
    if request.method == "GET":
        return render_template("about.html")
    return render_template("about.html")

@app.route("/history", methods=["POST", "GET"])
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    session.permanent = False
    user_id = session.get("user_id")
    connection = mysql.connector.connect(
        host=db_host,
        user=db_username,
        password=db_pass,
        database=db_name
    )
    cursor = connection.cursor()
    cursor.execute("""
        SELECT age, exp_years, prediction, predicted_at 
        FROM users_history 
        WHERE user_id = %s 
        ORDER BY predicted_at DESC 
        LIMIT 5""", (user_id,))
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("history.html", history=history)

if __name__=="__main__":
    app.run(debug=True)