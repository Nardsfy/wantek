from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from hashlib import md5
from wantek import app, login_manager
from wantek.models.userModel import User
from wantek.controllers.validate import login_not_allowed
from wantek.dao.userDao import get_data_user_loader, validate_user_login

@login_manager.user_loader
def load_user(user_id):
    """ Load session user """
    v_get_data_user_loader = get_data_user_loader(user_id)
    # If user not exists or error return None
    if (v_get_data_user_loader["status"] == "F" or not v_get_data_user_loader["result"]): return None

    # Set session user
    user_id     = v_get_data_user_loader["result"][0]["u_id"]
    username    = v_get_data_user_loader["result"][0]["u_username"]
    user_role   = v_get_data_user_loader["result"][0]["u_role"]
    return User(user_id, username, user_role)

@app.route("/login", methods=["GET", "POST"])
@login_not_allowed
def login():
    # Load login page
    if request.method == "GET":                          
        # For highlight invalid form
        validate    = request.args.getlist("validate")

        return render_template("login.html", menu="Login", validate=validate)
    
    # Process log in
    elif request.method == "POST":
        username    = request.form.get("username", None)
        password    = request.form.get("password", None)

        # Validate input data
        validate    = []
        if (username in [None, ""]):
            validate.append("username")            
        if (password in [None, ""]):
            validate.append("password")            
        if (validate):
            message     = f"{', '.join(validate)} must not be empty."
            flash_type  = "danger"
            flash(message, flash_type)
            return redirect(url_for("login", validate=validate))
        
        # Hash password with md5
        password    = md5(password.encode()).hexdigest()

        # Validate user login
        v_validate_user_login   = validate_user_login(username, password)
        if (v_validate_user_login["status"] == "F"):
            message     = v_validate_user_login["message"]
            flash_type  = "danger"
            flash(message, flash_type)
            return redirect(url_for("login"))
        elif (not v_validate_user_login["result"]):
            message     = "Username and password not match."
            flash_type  = "danger"
            flash(message, flash_type)
            return redirect(url_for("login"))
        
        # Set user data
        v_id            = v_validate_user_login["result"][0]["u_id"] 
        v_username      = v_validate_user_login["result"][0]["u_username"] 
        v_role          = v_validate_user_login["result"][0]["u_role"]
        v_status_user   = v_validate_user_login["result"][0]["u_status"]

        # Check status user active or inactive 
        if (v_status_user == "F"):
            message     = "Account deactivated."
            flash_type  = "danger"
            flash(message, flash_type)
            return redirect(url_for("login"))
        
        # Set session user loader
        user    = User(v_id, v_username, v_role)        
        login_user(user)
        return redirect(url_for("home"))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
