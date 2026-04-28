# db_model.py
# eita database connection establish korar jonno use kora hocche
# puro app er backend data communication eita handle kore

import mysql.connector

class DB:
    def __init__(self):
        # eita MySQL server er sathe connection create kore
        # ekhane credentials diye database access kora hocche
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="swastha"
        )
        # cursor use kora hocche SQL query run korar jonno
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        # eita SQL query execute korar main function
        # params use kora hoy SQL injection prevent korar jonno
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetchall(self, query, params=None):
        # eita data retrieve korar jonno use kora hocche
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()