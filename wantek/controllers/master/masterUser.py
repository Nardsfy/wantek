from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_parameter
from hashlib import md5
from wantek import app
from wantek.dao.master.masterUserDao import get_data_role, get_data_cabang, get_data_user, add_data_user, edit_data_user

@app.route("/master/user", methods=["GET"])
@login_required
def master_user():      
    username    = request.args.get("username", "")    # Optional
    status      = request.args.get("status", "")      # Optional
    role        = request.args.get("role", "")        # Optional  
    cabang        = request.args.get("cabang", "")    # Optional  

    # Untuk set parameter pagination menggunakan flask_paginate
    page    = request.args.get(get_page_parameter(), type=int, default=1)
    limit   = app.config["LIMIT_DATA_MASTER"]
    offset  = (page-1) * limit

    # Untuk set form search
    v_search    = {
        "username"  : username,
        "status"    : status,
        "role"      : role,
        "cabang"    : cabang
    }
    
    # Untuk dropdown filter role
    hasil_get_data_role = get_data_role()    
    if (hasil_get_data_role["status"] == "F"):
        message     = hasil_get_data_role["message"]
        flash_type  = "error"
        flash(message, flash_type)
    v_role      = hasil_get_data_role["result"]

    hasil_get_data_cabang = get_data_cabang()    
    if (hasil_get_data_cabang["status"] == "F"):
        message     = hasil_get_data_cabang["message"]
        flash_type  = "error"
        flash(message, flash_type)
    v_cabang    = hasil_get_data_cabang["result"]
        
    hasil_get_data_user = get_data_user(username, status, role, cabang, offset, limit)
    if (hasil_get_data_user["status"] == "F"):
        message     = hasil_get_data_user["message"]
        flash_type  = "error"
        flash(message, flash_type)
    v_data  = hasil_get_data_user["result"]["data"]
    v_total = hasil_get_data_user["result"]["total"]

    # Declare pagination
    pagination  = Pagination(page=page, total=v_total, per_page=limit, alignment="right", css_framework="bootstrap5", link_size="sm")    

    return render_template("master/masterUser.html", menu="Master", roles=v_role, list_cabang=v_cabang, data=v_data, search=v_search, pagination=pagination)    

@app.route("/master/user/add", methods=["POST"])
@login_required
def master_user_add():
    username    = request.form.get("username", None)    # Mandatory
    password    = request.form.get("password", None)    # Mandatory
    role        = request.form.get("role", None)        # Mandatory
    cabang      = request.form.get("cabang", None)      # Mandatory
    status      = request.form.get("status", None)      # Mandatory

    # Validate input data
    validate    = []
    if (username in [None, ""]):
        validate.append("username")
    # Jika username tidak kosong, validasi username hanya boleh berupa alphanumeric
    else:
        if (not username.isalnum()):
            message     = f"<strong>{username}</strong> hanya boleh berupa karakter atau angka."
            flash_type  = "danger"
            flash(message, flash_type)
            return redirect(url_for("master_user"))
    if (password in [None, ""]):
        validate.append("password")            
    if (role in [None, ""]):
        validate.append("role")            
    if (cabang in [None, ""]):
        validate.append("cabang")            
    if (status in [None, ""]):
        validate.append("status")            
    if (validate):
        message     = f"Nilai <strong>{', '.join(validate)}</strong> tidak boleh kosong."
        flash_type  = "danger"
        flash(message, flash_type)
        return redirect(url_for("master_user"))
    
    # Hash password menggunakan md5
    hash_password   = md5(password.encode()).hexdigest()

    # Proses insert data user
    hasil_add_data_user = add_data_user(username, hash_password, role, cabang, status, current_user.username)        
    message     = hasil_add_data_user["message"]
    flash_type  = "success"
    if (hasil_add_data_user["status"] == "F"):
        flash_type  = "error"
    elif (hasil_add_data_user["status"] == "I"):
        flash_type  = "warning"            
    
    flash(message, flash_type)
    return redirect(url_for("master_user"))

@app.route("/master/user/edit", methods=["POST"])
@login_required
def master_user_edit():    
    username    = request.form.get("username", None)    # Mandatory    
    role        = request.form.get("role", None)        # Mandatory
    cabang      = request.form.get("cabang", None)      # Mandatory
    status      = request.form.get("status", None)      # Mandatory

    # Validate input data
    validate    = []
    if (username in [None, ""]):
        validate.append("username")            
    if (role in [None, ""]):
        validate.append("role")            
    if (cabang in [None, ""]):
        validate.append("cabang")            
    if (status in [None, ""]):
        validate.append("status")            
    if (validate):
        message     = f"Nilai <strong>{', '.join(validate)}</strong> tidak boleh kosong."
        flash_type  = "danger"
        flash(message, flash_type)
        return redirect(url_for("master_user"))
    
    hasil_edit_data_user    = edit_data_user(username, role, cabang, status, current_user.username)
    message     = hasil_edit_data_user["message"]
    flash_type  = "success"
    if (hasil_edit_data_user["status"] == "F"):
        flash_type  = "error"
    elif (hasil_edit_data_user["status"] == "I"):
        flash_type  = "warning"
    
    flash(message, flash_type)
    return redirect(url_for("master_user"))
