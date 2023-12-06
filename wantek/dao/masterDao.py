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
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor      = conn.cursor()      

            # Cek user sudah ada
            query_cek   =   """
                                SELECT EXISTS (
                                    SELECT
                                        1
                                    FROM
                                        users
                                    WHERE
                                        u_username = %(username)s
                                )              
                        """
            params_cek  = {
                "username"      : p_username
            }

            cursor.execute(query_cek, params_cek)
            data_cek        = rows_to_dict_list(cursor)
            is_user_exists  = data_cek[0]["exists"]
            if (is_user_exists):
                message = f"User <strong>{p_username}</strong> sudah ada."            
                return responseJSON(400, "I", message, [])

            query       =   """
                                INSERT INTO users (
                                    u_username,
                                    u_password,
                                    u_role,
                                    u_status,
                                    u_ins_user
                                ) VALUES (
                                    %(username)s,
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
    """ Insert data user """    
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
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


