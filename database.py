# -*- coding: utf-8 -*-

import sqlite3 as sql

#general class for database creation
class Database(object):
    def __init__(self, name):
        self.conn = sql.connect(name)
        self.database_instence = self.conn.cursor()

    def create_table(self, columns_dictionary, table_name):
        self.database_instence.execute("create table " + table_name + " (" + columns_dictionary + " );")
        self.conn.commit()

    def insert_data(self, table, columns, data):
        self.database_instence.execute("INSERT INTO " + table + " (" + columns + ") VALUES (" + data + " );")
        self.conn.commit()

    def delete_by_column(self, table, column, column_value):
        self.database_instence.execute("DELETE FROM " + table + " WHERE " + column + " == " + column_value + ";")
        self.conn.commit()

    def Display_all(self, table):
        self.database_instence.execute("SELECT * FROM " + table)
        data = self.database_instence.fetchone()
        return data

#example
d = Database("TAL")
d.create_table("name string, marvel fan string, anime string", "Itzhaky")
d.insert_data("Itzhaky", "name, marvel, anime", "'shon', 'dudu faruk', 'robert'")
print d.Display_all("Itzhaky")