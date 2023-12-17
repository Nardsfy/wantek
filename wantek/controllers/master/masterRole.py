from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_parameter
from wantek import app
from wantek.dao.master.masterRoleDao import get_data_role, get_data_menu, add_data_role, get_access_menu, edit_data_role
from wantek.others.format import responseJSON

@app.route("/master/role", methods=["GET"])
@login_required
def master_role():
    role        = request.args.get("role", "")        # Optional

    # Untuk set parameter pagination menggunakan flask_paginate
    page    = request.args.get(get_page_parameter(), type=int, default=1)
    limit   = app.config["LIMIT_DATA_MASTER"]
    offset  = (page-1) * limit

    # Untuk set form search
    v_search    = {        
        "role"      : role
    }

    hasil_get_data_role = get_data_role(role, offset, limit)
    if (hasil_get_data_role["status"] == "F"):
        message     = hasil_get_data_role["message"]
        flash_type  = "error"
        flash(message, flash_type)    
    v_data  = hasil_get_data_role["result"]["data"]
    v_total = hasil_get_data_role["result"]["total"]

    # Declare pagination
    pagination  = Pagination(page=page, total=v_total, per_page=limit, alignment="right", css_framework="bootstrap5", link_size="sm")

    # Untuk menampilkan checkbox menu ketika add user
    hasil_data_menu = get_data_menu()
    if (hasil_data_menu["status"] == "F"):
        message     = hasil_data_menu["message"]        
        flash_type  = "error"        
        flash(message, flash_type) 

    v_access_menu   = hasil_data_menu["result"]        
    return render_template("master/masterRole.html", menu="Master", data=v_data, search=v_search, access_menu=v_access_menu, pagination=pagination)    
    
@app.route("/master/role/add", methods=["POST"])
@login_required
def master_role_add():
    role        = request.form.get("role", None)        # Mandatory
    status      = request.form.get("status", None)      # Mandatory
    access_menu = request.form.getlist("access_menu[]")
    
    # Validate input data
    validate    = []                  
    if (role in [None, ""]):
        validate.append("role")
    if (status in [None, ""]):
        validate.append("status")            
    if (validate):
        message     = f"Nilai <strong>{', '.join(validate)}</strong> tidak boleh kosong."
        flash_type  = "danger"
        flash(message, flash_type)
        return redirect(url_for("master_role"))
    
    # Proses insert data role
    hasil_add_data_role = add_data_role(role, status, access_menu, current_user.username)        
    message     = hasil_add_data_role["message"]
    flash_type  = "success"
    if (hasil_add_data_role["status"] == "F"):
        flash_type  = "error"
    elif (hasil_add_data_role["status"] == "I"):
        flash_type  = "warning"            
    
    flash(message, flash_type)
    return redirect(url_for("master_role"))

@app.route("/master/role/edit", methods=["POST"])
@login_required
def master_role_edit():     
    id_role     = request.form.get("id_role", None)     # Mandatory    
    role        = request.form.get("role", None)        # Mandatory    
    status      = request.form.get("status", None)      # Mandatory
    access_menu = request.form.getlist("access_menu[]")    

    # Validate input data
    validate    = []
    if (id_role in [None, ""]):
        validate.append("id role")            
    if (role in [None, ""]):
        validate.append("role")            
    if (status in [None, ""]):
        validate.append("status")                          
    if (validate):
        message     = f"Nilai <strong>{', '.join(validate)}</strong> tidak boleh kosong."
        flash_type  = "danger"
        flash(message, flash_type)
        return redirect(url_for("master_role"))

    hasil_edit_data_user    = edit_data_role(id_role, role, access_menu, status, current_user.username)
    message     = hasil_edit_data_user["message"]
    flash_type  = "success"
    if (hasil_edit_data_user["status"] == "F"):
        flash_type  = "error"
    elif (hasil_edit_data_user["status"] == "I"):
        flash_type  = "warning"
    
    flash(message, flash_type)
    return redirect(url_for("master_role"))

@app.route("/master/role/get-access-menu", methods=["GET"])
@login_required
def master_role_get_access_menu(): # Request by ajax
    id_role     = request.args.get("id_role", None) # Mandatory
    if (id_role in [None, ""]):
        message = f"Nilai <strong>ID Role</strong> tidak boleh kosong."
        return responseJSON(400, "F", message, []), 400
    
    hasil_get_access_menu   = get_access_menu(id_role)    
    if (hasil_get_access_menu["status"] == "F"):        
        return hasil_get_access_menu, 400

    return hasil_get_access_menu, 200
