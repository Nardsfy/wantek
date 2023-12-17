import psycopg2
from wantek import connectionDB
from wantek.others.format import rows_to_dict_list, responseJSON

def get_data_role(p_role, p_offset, p_limit):
    """ Get data master user  """
    def count_data_role(cursor):
        try:
            query   =   """
                            SELECT        
                                COUNT(1) count
                            FROM 
                                roles 
                            WHERE
                                (LOWER (r_desc) LIKE '%%'||LOWER (%(role)s)||'%%' OR %(role)s IS NULL OR %(role)s = '')                          
                        """
            params  = {                
                "role"      : p_role
            }
            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Sukses get count master role."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, [])
    # End count_data_role

    result  = {"total": 0, "data": []}    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT        
                                ROW_NUMBER() OVER(ORDER BY r_status DESC, r_desc) index,                         
                                r_id,
                                r_desc,
                                r_status,                                
                                TO_CHAR(r_ins_date, 'dd Mon yyyy HH24:MI:SS') r_ins_date,
                                r_ins_user,
                                COALESCE(TO_CHAR(r_upd_date, 'dd Mon yyyy HH24:MI:SS'), '') r_upd_date,
                                COALESCE(r_upd_user, '') r_upd_user
                            FROM 
                                roles                            
                            WHERE
                                (LOWER (r_desc) LIKE '%%'||LOWER (%(role)s)||'%%' OR %(role)s IS NULL OR %(role)s = '')
                            ORDER BY r_status DESC, r_desc
                            OFFSET %(offset)s
                            LIMIT %(limit)s
                        """
            params  = {
                "role"      : p_role,
                "offset"    : p_offset,
                "limit"     : p_limit
            }
                                    
            cursor.execute(query, params)                       
            data    = rows_to_dict_list(cursor)

            # Get total data
            hasil_count_data_user   = count_data_role(cursor)
            if (hasil_count_data_user["status"] == "F"):
                return hasil_count_data_user
            total   = hasil_count_data_user["result"][0]["count"]

            result["data"]  = data
            result["total"] = total

            message = "Sukses get data master role."            
            return responseJSON(200, "T", message, result)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, result)
        finally:
            if (cursor):
                cursor.close()
    except psycopg2.Error as e:        
        message = f"Error connection: {str(e)}"
        return responseJSON(400, "F", message, result)
    finally:
        if (conn):            
            conn.close() 


def get_data_menu():
    """ Get data menu """    
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT        
                                m_id,
                                m_desc,                                                                                            
                                m_parent                                
                            FROM 
                                menus 
                            ORDER BY
                                m_id,
                                m_parent                          
                        """
            params  = {}

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)            

            message = "Sukses get data master menu."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, [])
        finally:
            if (cursor):
                cursor.close()
    except psycopg2.Error as e:        
        message = f"Error connection: {str(e)}"
        return responseJSON(400, "F", message, [])
    finally:
        if (conn):            
            conn.close() 

def add_data_role(p_role, p_status, p_access_menu, p_user_login):
    """ Insert data role """  
    def cek_role(cursor, role): 
        try:
            query   =   """
                            SELECT EXISTS (
                                SELECT
                                    1
                                FROM
                                    roles
                                WHERE
                                    LOWER(r_desc) = LOWER(%(role)s)
                            )              
                        """
            params  = {
                "role"  : role
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Sukses cek role."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, []) 
    # End of cek_role
    
    def get_id_role(cursor): 
        try:
            query   =   """
                            SELECT 
                                LPAD( (COALESCE(MAX(r_id::INT)+1, 0))::TEXT, 2, '0') r_id
                            FROM
                                roles                                       
                        """
            params  = {}

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Sukses get id role."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, []) 
    # End of get_id_role

    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor      = conn.cursor()      

            # Cek role sudah ada
            hasil_cek_role  = cek_role(cursor, p_role)
            if (hasil_cek_role["status"] == "F"):
                return hasil_cek_role
            is_user_exists  = hasil_cek_role["result"][0]["exists"]
            if (is_user_exists):
                message = f"Role <strong>{p_role.capitalize()}</strong> sudah ada."            
                return responseJSON(400, "I", message, [])
            
            hasil_get_id_role   = get_id_role(cursor)
            if (hasil_get_id_role["status"] == "F"):
                return hasil_get_id_role
            id_role     = hasil_get_id_role["result"][0]["r_id"]

            # Insert role
            query       =   """
                                INSERT INTO roles (
                                    r_id,
                                    r_desc,
                                    r_status,
                                    r_ins_user                                    
                                ) VALUES (
                                    %(id_role)s,
                                    %(role)s,
                                    %(status)s,
                                    %(user_login)s
                                )                          
                        """
            params      = {          
                "id_role"       : id_role,      
                "role"          : p_role,                
                "status"        : p_status,
                "user_login"    : p_user_login
            }
            cursor.execute(query, params)

            # Insert access menu
            for access_menu in p_access_menu:                                    
                query       =   """
                                    INSERT INTO access_menu (
                                        am_r_id,
                                        am_m_id,
                                        am_upd_user                                   
                                    ) VALUES (
                                        %(id_role)s,                                        
                                        %(access_menu)s,
                                        %(user_login)s
                                    ) ON CONFLICT ON CONSTRAINT access_menu_pk
                                        DO NOTHING
                            """
                params      = {   
                    "id_role"       : id_role,                                                 
                    "access_menu"   : access_menu,
                    "user_login"    : p_user_login
                }
                cursor.execute(query, params)

                menu_parent = access_menu
                while menu_parent is not None:                    
                    # Cek apakah menu memiliki parent
                    query   =   """
                                    SELECT        
                                        m_id,                                                                                                                               
                                        m_parent                                
                                    FROM 
                                        menus
                                    WHERE 
                                        m_id = %(access_menu)s                         
                                """
                    params  = {
                        "access_menu"   : menu_parent
                    }
                    cursor.execute(query, params)
                    data    = rows_to_dict_list(cursor)
                    menu_parent     = data[0]["m_parent"]                
                    menu_has_parent = menu_parent is not None    

                    # Jika menu memiliki parent, maka insert menu_parent 
                    if (menu_has_parent):
                        query       =   """
                                            INSERT INTO access_menu (
                                                am_r_id,
                                                am_m_id,
                                                am_upd_user                                   
                                            ) VALUES (
                                                %(id_role)s,                                                
                                                %(access_menu)s,
                                                %(user_login)s
                                            ) ON CONFLICT ON CONSTRAINT access_menu_pk
                                                DO NOTHING
                                    """
                        params      = {                
                            "id_role"       : id_role,                
                            "access_menu"   : menu_parent,
                            "user_login"    : p_user_login
                        }
                        cursor.execute(query, params)                        

            conn.commit()                      

            message = f"Role <strong>{p_role}</strong> berhasil ditambahkan."            
            return responseJSON(200, "T", message, [])
        except psycopg2.Error as e:
            if (conn):
                conn.rollback()
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, [])
        finally:
            if (cursor):
                cursor.close()
    except psycopg2.Error as e:        
        if (conn):
            conn.rollback()
        message = f"Error connection: {str(e)}"
        return responseJSON(400, "F", message, [])
    finally:
        if (conn):                        
            conn.close() 

def get_access_menu(p_id_role):
    """ Get data access menu berdasarkan role  """    
        
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT        
                                am_r_id,
                                am_m_id
                            FROM 
                                access_menu                            
                            WHERE
                                am_r_id = %(id_role)s
                        """
            params  = {
                "id_role"   : p_id_role
            }
                                    
            cursor.execute(query, params)                       
            data    = rows_to_dict_list(cursor)           

            message = "Sukses get access menu dari role."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, [])
        finally:
            if (cursor):
                cursor.close()
    except psycopg2.Error as e:        
        message = f"Error connection: {str(e)}"
        return responseJSON(400, "F", message, [])
    finally:
        if (conn):            
            conn.close() 

def edit_data_role(p_id_role, p_role, p_access_menu, p_status, p_user_login):
    """ Update data role """  
    def get_data_role_cek(cursor, id_role): 
        try:
            query   =   """
                            SELECT
                                r_id,
                                r_desc,
                                r_status,
                                am.am_m_id
                            FROM
                                roles r
                            LEFT JOIN
                                access_menu am ON (
                                    r.r_id = am.am_r_id
                                )
                            WHERE
                                r_id = %(id_role)s
                        """
            params  = {
                "id_role"   : id_role
            }            

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Sukses get data role untuk cek."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, []) 
    # End of get_data_role_cek
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()

            # Cek tidak ada data yang diupdate
            hasil_get_data_role_cek = get_data_role_cek(cursor, p_id_role)
            if (hasil_get_data_role_cek["status"] == "F"):
                return hasil_get_data_role_cek
            if (not hasil_get_data_role_cek["result"]):
                return responseJSON(400, "F", f"Role <strong>{p_role.capitalize()}</strong> tidak ditemukan.", [])
            
            # Cek apakah ada data yang diupdate atau tidak
            access_menu_is_updated  = False
            for cek_data_role in hasil_get_data_role_cek["result"]:     
                if (cek_data_role["am_m_id"] is None):
                    if (p_access_menu):
                        access_menu_is_updated  = True
                        break
                    else:
                        access_menu_is_updated  = False
                else:
                    access_menu_is_updated  = cek_data_role["am_m_id"] not in p_access_menu
                if (access_menu_is_updated is True):
                    break
            cek_role        = hasil_get_data_role_cek["result"][0]["r_desc"]
            cek_status      = hasil_get_data_role_cek["result"][0]["r_status"]            
            
            if (cek_role == p_role and cek_status == p_status and access_menu_is_updated is False):
                message = f"Tidak ada data yang diubah untuk role <strong>{p_role.capitalize()}</strong>."
                return responseJSON(400, "I", message, [])
            
            # Update data role
            query   =   """
                            UPDATE roles
                            SET
                                r_desc      = %(role)s,
                                r_status    = %(status)s, 
                                r_upd_date  = CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta',
                                r_upd_user  = %(user_login)s
                            WHERE
                                r_id        = %(id_role)s
                        """
            params  = {
                "id_role"       : p_id_role,
                "role"          : p_role,
                "status"        : p_status,
                "user_login"    : p_user_login
            }
            cursor.execute(query, params)
            
            # Delete access menu dari role sebelum insert
            query   =   """
                            DELETE FROM access_menu
                            WHERE
                                am_r_id = %(id_role)s
                        """
            params  = {
                "id_role"   : p_id_role
            }
            cursor.execute(query, params)

            # Insert access menu
            for menu in p_access_menu:                
                query   =   """
                                INSERT INTO access_menu (
                                    am_r_id,
                                    am_m_id,
                                    am_upd_user                                
                                ) VALUES (
                                    %(id_role)s,
                                    %(menu)s,
                                    %(user_login)s
                                )
                            """
                params  = {
                    "id_role"       : p_id_role,
                    "menu"          : menu,
                    "user_login"    : p_user_login
                }
                cursor.execute(query, params)

            conn.commit()                      

            message = f"Role <strong>{p_role}</strong> berhasil diubah."            
            return responseJSON(200, "T", message, [])
        except psycopg2.Error as e:
            if (conn):
                conn.rollback()
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, [])
        finally:
            if (cursor):
                cursor.close()
    except psycopg2.Error as e: 
        if (conn):
            conn.rollback()       
        message = f"Error connection: {str(e)}"
        return responseJSON(400, "F", message, [])
    finally:
        if (conn):            
            conn.close() 

