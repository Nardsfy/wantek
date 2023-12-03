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
                                u_id,
                                u_username,
                                u_role
                            FROM 
                                users
                            WHERE
                                u_id = %(id)s
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


def validate_user_login(p_username, p_password):
    """ Validate user log in """
    conn    = None
    try:
        cursor  = None        
        conn    = connectionDB()
        try:
            cursor  = conn.cursor()
            query   =   """
                            SELECT 
                                u_id,
                                u_username,
                                u_password,
                                u_role,
                                u_status
                            FROM 
                                users
                            WHERE
                                u_username      = %(username)s
                                AND u_password  = %(password)s
                        """
            params  = {
                "username"  : p_username,
                "password"  : p_password
            }

            cursor.execute(query, params)
            data    = rows_to_dict_list(cursor)
            print(data)
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