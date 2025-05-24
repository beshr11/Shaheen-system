from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "shaheen_secret"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="بيانات الدخول غير صحيحة")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "role" not in session:
        return redirect("/")
    if session["role"] == "admin":
        return render_template("admin.html", username=session["username"])
    elif session["role"] == "delegate":
        return render_template("delegate.html", username=session["username"])
    elif session["role"] == "director":
        return render_template("director.html", username=session["username"])
    return "صلاحية غير معروفة"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

