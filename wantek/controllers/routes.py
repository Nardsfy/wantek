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
    organized_menu = {}
    if (current_user.is_authenticated):
        hasil_get_list_akses_menu   = get_list_akses_menu(current_user.role)
        if (hasil_get_list_akses_menu["status"] == "F"):
            message     = hasil_get_list_akses_menu["message"]
            flash_type  = "error"
            flash(message, flash_type)
        list_akses_menu     = hasil_get_list_akses_menu["result"] 
        # Set children dari menu
        grandparent = list_akses_menu[0]["m_id"]
        for menu in list_akses_menu:
            menu_id, menu_desc, menu_parent, menu_link, menu_level = menu.values()            
            if (menu_level < 1):
                grandparent = menu_id
                organized_menu[menu_id] = {"desc": menu_desc, "link": menu_link, "level": menu_level, "children": []}
            else:
                if (menu_parent in organized_menu):
                    organized_menu[menu_parent]["children"].append({"id": menu_id, "desc": menu_desc, "link": menu_link, "grandchildren": []})
                # Set grandchildren
                else:       
                    for child in organized_menu[grandparent]["children"]:
                        if (child["id"] == menu_parent):
                            child["grandchildren"].append({"id": menu_id, "desc": menu_desc, "link": menu_link})        

    return dict(
        APP_NAME    = app.config["APP_NAME"],
        APP_INITIAL = app.config["APP_INITIAL"],
        COPYRIGHT   = app.config["COPYRIGHT"],
        VERSION     = app.config["VERSION"],
        AKSES_MENU  = organized_menu
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
