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
    def remove_table(self, table_name = 'new_table'):
        sql = "DROP TABLE %s" % table_name
        try:
            self.cur.executescript(sql)
        except sqlite3.DatabaseError as err:
            print(err)
    def get_tables_list(self):
        sql = """\
        SELECT name FROM sqlite_master
        WHERE TYPE IN ('table','view') AND name not like 'sqlite_%'
        UNION ALL
        SELECT name FROM sqlite_temp_master
        WHERE type IN ('table','view')
        ORDER BY 1;
        """
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        tab_list = self.cur.fetchall()
        ret_tab = []
        for i in tab_list:
            ret_tab.append(i[0])
        return ret_tab
    def get_raw_number(self, table_name):
        sql = "SELECT COUNT(*) FROM %s" % table_name
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        return self.cur.fetchall()[0][0]
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
        if self.get_column_number(table_name)-1 == len(raw_data):
            sql = """
            INSERT INTO %s (%s)
            VALUES (%s);
            """ % (table_name,str(self.get_colomn_names(table_name)[1:len(self.get_colomn_names(table_name))]).
                   strip('[]').replace('\'',''),str(raw_data).strip('[]'))
            try:
                self.cur.execute(sql)
            except sqlite3.DatabaseError as err:
                print(err)
        else:
            print("Mismatch of raw length and fields number!")
    def edit_raw(self,table_name,raw_num, raw_data):
        if self.get_column_number(table_name) - 1 == len(raw_data):
            fields = self.get_colomn_names(table_name)
            new_data = ''
            for i in range(len(raw_data)):
                new_data = new_data + fields[i+1] + '=\''+ raw_data[i] + '\','
            new_data = new_data[0:len(new_data)-1]
            sql = """
            UPDATE OR ABORT %s
            SET %s
            WHERE %s=%s
            """ % (table_name,new_data,fields[0],raw_num)
            try:
                self.cur.execute(sql)
            except sqlite3.DatabaseError as err:
                print(err)
        else:
            print("Mismatch of raw length and fields number!")
    def remove_raw(self,table_name,raw_num):
        sql = """
        DELETE FROM %s
        WHERE %s=%s
        """ % (table_name,self.get_colomn_name(table_name),raw_num)
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
    def edit_cell(self,table_name,new_data,raw_num,column_name):
        sql = """
        UPDATE OR ABORT %s
        SET %s = %s
        WHERE %s = %s
        """% (table_name,column_name,new_data,self.get_colomn_name(),raw_num)
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
    def edit_column_name(self,table_name,column_name,new_column_name):
        sql = """
        ALTER TABLE %s RENAME COLUMN %s TO %s;
        """ % (table_name,column_name,new_column_name)
        print(sql)
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
    def add_column(self,table_name,new_column_name):
        sql = """
        ALTER TABLE %s ADD COLUMN \'%s\' TEXT DEFAULT \'---\'
        """ % (table_name,new_column_name)
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
    def index_correction(self,table_name):
        for i in self.get_raw_number(table_name):
            if self.get_data(table_name)[i][0] != i:
                self.edit_cell(table_name,i,self.get_data(table_name)[i][0],self.get_colomn_name(table_name))

    def edit_column(self,table_name,column_name,column_data):
        if self.get_raw_number(table_name) == len(column_data):
            interator = 1
            for inserted_data in column_data:
                self.edit_cell(table_name,inserted_data,interator,column_name)
                interator = interator+1

    def remove_cloumn(self,table_name,column_name):
        sql = """
        ALTER TABLE %s DROP COLUMN %s
        """ % (table_name,column_name)
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
    def commite_changes(self):
        self.base.commit()
    def get_data(self,table_name):
        sql = "SELECT * FROM %s" % (table_name)
        try:
            self.cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(err)
        return self.cur.fetchall()
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
    base1.create_table("user2", ['Name', 'pass', 'email'], ['TEXT', "INTEGER", "TEXT"])
    base1.add_raw("user",['Max','2311k','tnb6@yandex.ru'])
    base1.add_raw("user", ['Max', '231', 'tnb6@yandex.ru'])
    base1.add_raw("user", ['Max2', '2313', 'tnb6@yandex.ru3'])
    print(base1.get_tables_list())
    print((base1.get_tables_list()))
    print(base1.get_colomn_name("user"))
    print(base1.get_colomn_names("user"))
    print(base1.get_raw_number("user"))
    print(base1.get_column_number("user"))
    base1.commite_changes()
    print(base1.get_data("user")[0])
    base1.edit_raw("user",5,['Nikita','625893','niherus@gmail.com'])
    print(base1.get_data("user")[4])
    base1.remove_raw("user",10)
    base1.commite_changes()
    base1.commite_changes()
    #base1.remove_table(base1.get_tables_list()[0])
    print(base1.get_tables_list())
    del base1