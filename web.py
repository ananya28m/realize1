from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)
@app.route("/")
def hello_world():
    return '''ABC
    BCA 
    READ'''
@app.route("/signup")
def signup():
    return "<p>signup<p>"
@app.route("/signin", methods=["POST", "GET"])
def signin():
# if form is submitted
    if request.method == "POST":
        # record the user name
        session["username"] = request.form.get("name")
        # redirect to the main page
        return redirect("/")
    return render_template("signin.html")
