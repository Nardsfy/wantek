import psycopg2
from wantek import connectionDB
from wantek.others.format import rows_to_dict_list, responseJSON

def get_data_role():
    """ Get data role """    
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT        
                                r_id,
                                r_desc
                            FROM 
                                roles                            
                        """
            params  = {}

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)            

            message = "Sukses get data master role."            
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

def get_data_user(p_username, p_status, p_role, p_offset, p_limit):
    """ Get data master user  """
    def count_data_user(cursor):
        try:
            query   =   """
                            SELECT        
                                COUNT(1) count
                            FROM 
                                users u                            
                        """
            params  = {}
            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Sukses get count master user."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, [])
    # End count_data_user

    result  = {"total": 0, "data": []}    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT        
                                ROW_NUMBER() OVER(ORDER BY u_status DESC, u_username) index,                         
                                u_username,
                                u_password,
                                u_role,
                                r.r_desc role_desc,
                                u_status,
                                TO_CHAR(u_ins_date, 'dd Mon yyyy HH24:MI:SS') u_ins_date,
                                u_ins_user,
                                COALESCE(TO_CHAR(u_upd_date, 'dd Mon yyyy HH24:MI:SS'), '') u_upd_date,
                                COALESCE(u_upd_user, '') u_upd_user
                            FROM 
                                users u
                            LEFT JOIN roles r ON (
                                u.u_role = r.r_id
                            )
                            WHERE
                                (LOWER (u_username) LIKE '%%'||LOWER (%(username)s)||'%%' OR %(username)s IS NULL OR %(username)s = '')
                                AND (u_role = %(role)s OR %(role)s IS NULL OR %(role)s = '')
                                AND (u_status = %(status)s OR %(status)s IS NULL OR %(status)s = '')
                            ORDER BY u_status DESC, u_username
                            OFFSET %(offset)s
                            LIMIT %(limit)s
                        """
            params  = {
                "username"  : p_username,
                "role"      : p_role,
                "status"    : p_status,
                "offset"    : p_offset,
                "limit"     : p_limit
            }
                                    
            cursor.execute(query, params)                       
            data    = rows_to_dict_list(cursor)

            # Get total data
            hasil_count_data_user   = count_data_user(cursor)
            if (hasil_count_data_user["status"] == "F"):
                return hasil_count_data_user
            total   = hasil_count_data_user["result"][0]["count"]

            result["data"]  = data
            result["total"] = total

            message = "Sukses get data master user."            
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

def add_data_user(p_username, p_password, p_role, p_status, p_user_login):
    """ Insert data user """  
    def cek_user(cursor, username): 
        try:
            query   =   """
                            SELECT EXISTS (
                                SELECT
                                    1
                                FROM
                                    users
                                WHERE
                                    u_username = %(username)s
                            )              
                        """
            params  = {
                "username"  : username
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Sukses cek user."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, []) 
    # End of cek_user

    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor      = conn.cursor()      

            # Cek user sudah ada
            hasil_cek_user  = cek_user(cursor, p_username)
            if (hasil_cek_user["status"] == "F"):
                return hasil_cek_user
            is_user_exists  = hasil_cek_user["result"][0]["exists"]
            if (is_user_exists):
                message = f"User <strong>{p_username}</strong> sudah ada."            
                return responseJSON(400, "I", message, [])

            # Insert user
            query       =   """
                                INSERT INTO users (
                                    u_username,
                                    u_password,
                                    u_role,
                                    u_status,
                                    u_ins_user
                                ) VALUES (
                                    LOWER (%(username)s),
                                    %(password)s,
                                    %(role)s,
                                    %(status)s,
                                    %(user_login)s
                                )                          
                        """
            params      = {
                "username"      : p_username,
                "password"      : p_password,
                "role"          : p_role,
                "status"        : p_status,
                "user_login"    : p_user_login
            }

            cursor.execute(query, params)
            conn.commit()                      

            message = f"User <strong>{p_username}</strong> berhasil ditambahkan."            
            return responseJSON(200, "T", message, [])
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

def edit_data_user(p_username, p_role, p_status, p_user_login):
    """ Update data user """  
    def get_data_user_cek(cursor, username): 
        try:
            query   =   """
                            SELECT
                                u_role,
                                u_status
                            FROM
                                users
                            WHERE
                                u_username = %(username)s              
                        """
            params  = {
                "username"  : username
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Sukses get data user untuk cek."            
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            message = f"Error query: {str(e)}"
            return responseJSON(400, "F", message, []) 
    # End of cek_data_user
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()

            # Cek tidak ada data yang diupdate
            hasil_get_data_user_cek = get_data_user_cek(cursor, p_username)
            if (hasil_get_data_user_cek["status"] == "F"):
                return hasil_get_data_user_cek
            if (not hasil_get_data_user_cek["result"]):
                return responseJSON(400, "F", f"User <strong>{p_username}</strong> tidak ditemukan.", [])            
            cek_role    = hasil_get_data_user_cek["result"][0]["u_role"]
            cek_status  = hasil_get_data_user_cek["result"][0]["u_status"]            
            if (cek_role == p_role and cek_status == p_status):
                message = f"Tidak ada data yang diubah untuk user <strong>{p_username}</strong>."
                return responseJSON(400, "I", message, [])
            
            # Update user
            query   =   """
                            UPDATE users 
                            SET                                
                                u_role      = %(role)s,
                                u_status    = %(status)s,
                                u_upd_date  = CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta',
                                u_upd_user  = %(user_login)s                                                                          
                            WHERE 
                                u_username  = %(username)s
                        """
            params  = {
                "username"      : p_username,                
                "role"          : p_role,
                "status"        : p_status,
                "user_login"    : p_user_login
            }

            cursor.execute(query, params)
            conn.commit()                      

            message = f"User <strong>{p_username}</strong> berhasil diubah."            
            return responseJSON(200, "T", message, [])
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


