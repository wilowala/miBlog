from flask import Flask, render_template, Blueprint

app = Blueprint("app", __name__, url_prefix="/")

@app.route("/")
def home():

    return render_template("index.html")