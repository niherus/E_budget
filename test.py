import sqlite3
#print(sqlite3.apilevel)
#print(sqlite3.sqlite_version)


def creat(name = "mydatabase"):
    conn = sqlite3.connect(name + ".db")
    table_name = "user"
    column0 = "id_user"
    column1 = "email"
    column2 = "passw"
    #conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS user (name, pass) ;
    SELECT name FROM sqlite_master
    WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%'
    UNION ALL
    SELECT name FROM sqlite_temp_master
    WHERE type IN ('table','view')
    ORDER BY 1;
    """
    try:
        cursor.executescript(sql)
    except sqlite3.DatabaseError as err:
        print(err)
        conn.close()
        return 0
    print("Сreated")
    cursor.close()
    conn.close()
    return 0
def add_user(name,user_name,passw):
    table_name = "user"
    column1 = "name"
    column2 = "pass"
    conn = sqlite3.connect(name + ".db")
    cursor = conn.cursor()
    sql =  """\
        INSERT INTO %s (%s,%s)
        VALUES ('%s','%s')
    """ % (table_name,column1,column2,user_name,passw)
    print(sql)
    try:
        cursor.executescript(sql)
    except sqlite3.DatabaseError as err:
        print(err)
        cursor.close()
        conn.close()
        return 0
    conn.commit()
    print("Success")
    cursor.close()
    conn.close()
    return 0
def del_user(name):
    table_name = "user"
    column1 = "name"
    column2 = "pass"
    conn = sqlite3.connect(name + ".db")
    cursor = conn.cursor()
    sql = """\
    """
def check_info(name):
    table_name = "user"
    conn = sqlite3.connect(name + ".db")
    cursor = conn.cursor()
    sql = "PRAGMA table_info(%s)" % (table_name)
    cursor.executescript(sql)
creat("hope")
flag = (input("Add new user? ") == 'Y')
while flag:
    add_user("hope",input("Username: "),input("Password: "))
    flag = (input("Add new user? ") == 'Y')
check_info("hope")


