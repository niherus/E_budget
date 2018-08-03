import sqlite3
import os
class Db_control():
    def __init__(self,base_path = "temp.db",default = False):
        if default:
            self.base = sqlite3.connect(base_path)
        else:
            if not os.path.isfile(base_path):
                print(os.path.isfile(base_path))
                self.base = sqlite3.connect(base_path)
                print("Created new database %s" % base_path)
            else:
                answ = input("""
            Database %s has already exist
            1 - to connect to %s
            2 - replace new
            3 - cansel
            Answer: """ % (base_path,base_path))
                if answ == '1':
                    self.base = sqlite3.connect(base_path)
                elif answ == '2':
                    os.remove(base_path)
                    self.base = sqlite3.connect(base_path)
                else:
                    return None
        self.cur = self.base.cursor()
    def create_table(self, table_name = 'new_table',fields_list = [],type_list = []):
        if len(fields_list)!= len(type_list):
            print("""
            Error wrong list of fields or types.
            Please check your lists
            """)
            return None
        sql = """
        create table %s (
        id_%s integer primary key autoincrement,
        """ % (table_name, table_name)
        fields = ""
        if len(fields_list) > 0:
            for i in range(len(fields_list)):
                fields = fields + "\t\t"+str(fields_list[i]) + " " +str(type_list[i]) + ",\n"
        sql = sql + fields[2:len(fields)-2] + "\n);"
        try:
            self.cur.executescript(sql)
        except sqlite3.DatabaseError as err:
            print(err)
    def get_tables_list(self):
        sql = """SELECT name FROM sqlite_master
        WHERE TYPE IN ('table','view') AND name not like 'sqlite_%'
        UNION ALL
        SELECT name FROM sqlite_temp_master
        WHERE type IN ('table','view')
        ORDER BY 1;
        """
        try:
            self.cur.executescript(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        return self.cur.fetchall()
    def get_raw_number(self, table_name):
        sql = "SELECT COUNT(*) FROM %s" % table_name
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        return len(self.cur.fetchall())
    def get_column_number(self, table_name):
        sql = "PRAGMA TABLE_INFO(%s)" % table_name
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        return len(self.cur.fetchall())
    def get_colomn_names(self, table_name):
        sql = "PRAGMA TABLE_INFO(%s)" % table_name
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        names = [tup[1] for tup in self.cur.fetchall()]
        return names
    def get_colomn_name(self, table_name, col_num = 0):
        sql = "PRAGMA TABLE_INFO(%s)" % table_name
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        names = [tup[1] for tup in self.cur.fetchall()]
        return names[col_num]
    def add_raw(self, table_name, raw_data):
        if self.get_column_number(table_name) == len(raw_data):
            sql = "INSERT INTO"
        else:
            print("Warning! Mismatch of raw length and fields number!")
    def __del__(self):
        try:
            self.cur.close()
            self.base.close()
            print("Database disconnected")
        except AttributeError:
            print("No database to delete")
            return None





if __name__ == '__main__':
    base1 = Db_control("fin_base.db",default = True)
    base1.create_table("user", ['Name', 'pass','email'],['TEXT',"INTEGER","TEXT"])
    print(base1.get_colomn_name("user"))
    print(base1.get_raw_number("user"))
    print(base1.get_column_number("user"))
    del base1