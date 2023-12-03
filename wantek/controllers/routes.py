from flask import render_template
from flask_login import login_required
from wantek import app

@app.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", menu="Home")

@app.context_processor
def global_var():
    # Function global var for Jinja2    
    return dict(
        APP_NAME    = app.config["APP_NAME"],
        APP_INITIAL = app.config["APP_INITIAL"],
        COPYRIGHT   = app.config["COPYRIGHT"],
        VERSION     = app.config["VERSION"]
    )