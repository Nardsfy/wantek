import psycopg2
from wantek import connectionDB
from wantek.others.format import rows_to_dict_list, responseJSON

def get_data_user_loader(p_id):
    """ Get data user for user_loader """
    conn    = None
    try:
        cursor  = None
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT                                                                 
                                u_role,
                                u_cabang
                            FROM 
                                users
                            WHERE
                                u_username = %(id)s
                        """
            params  = {
                "id"    : p_id
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)
            message = "Success get data user laoder."
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


def get_list_akses_menu(p_role):
    """ Get data menu untuk navbar """    
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT        
                                m.m_id,
                                m.m_desc,                                                                                            
                                m.m_parent,
                                m.m_link                             
                            FROM 
                                menus m
                            JOIN access_menu am ON (am.am_m_id = m.m_id)
                            WHERE
                                am.am_r_id = %(role)s
                            ORDER BY
                                m_id,
                                m_parent                          
                        """
            params  = {
                "role"  : p_role
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)            

            message = "Sukses get data master menu sesuai role."            
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


def validate_user_login(p_username, p_password, p_cabang):
    """ Validate user log in """
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT                                 
                                u_username,
                                u_password,
                                u_role,
                                u_status,
                                u_cabang
                            FROM 
                                users
                            WHERE
                                LOWER (u_username)  = LOWER (%(username)s)
                                AND u_password      = %(password)s
                                AND u_cabang        = %(cabang)s
                        """
            params  = {
                "username"  : p_username,
                "password"  : p_password,
                "cabang"    : p_cabang
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)

            message = "Success validate user login."            
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


def get_list_cabang():
    """ Get data cabang untuk form login """    
    
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT        
                                c_id,
                                INITCAP(c_desc) c_desc
                            FROM
                                cabang
                            WHERE
                                c_status = 'T'
                            ORDER BY
                                c_desc                          
                        """
            params  = {                
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)            

            message = "Sukses get data cabang."            
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

