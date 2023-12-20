from flask import flash, render_template
from flask_login import current_user, login_required
from wantek import app
from wantek.dao.userDao import get_list_akses_menu

@app.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", menu="Home")

@app.context_processor
def global_var():
    # Function global var for Jinja2

    # Set akses menu untuk navbar    
    list_akses_menu = []
    if (current_user.is_authenticated):
        hasil_get_list_akses_menu   = get_list_akses_menu(current_user.role)
        if (hasil_get_list_akses_menu["status"] == "F"):
            message     = hasil_get_list_akses_menu["message"]
            flash_type  = "error"
            flash(message, flash_type)
        list_akses_menu     = hasil_get_list_akses_menu["result"]         

    return dict(
        APP_NAME    = app.config["APP_NAME"],
        APP_INITIAL = app.config["APP_INITIAL"],
        COPYRIGHT   = app.config["COPYRIGHT"],
        VERSION     = app.config["VERSION"],        
        AKSES_MENU  = list_akses_menu
    )

@app.errorhandler(403)
def handle_forbidden(e):
    return render_template("errors/403.html")

@app.errorhandler(404)
def handle_bad_request(e):
    return render_template("errors/404.html")

@app.errorhandler(405)
def handle_method_not_allowed(e):
    return render_template("errors/405.html")
