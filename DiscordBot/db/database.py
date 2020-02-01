import sqlite3
from sqlite3 import Error
import db.sqlCommands


class Database:
    def __init__(self, db_location):
        self.conn = self.create_connection(db_location)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_player_table(self):
        if self.conn is not None:
            self.create_table(db.sqlCommands.sql_create_users_table)
        else:
            print("Error: Could not establish connection to database")

    def add_player(self, player):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_insert_player, player)
        self.conn.commit()
        return cur.lastrowid

    def select_player_exists(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_exists, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_player_status(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_status, (player_id,))
        rows = cur.fetchall()
        return rows

    def update_player_status(self, player_id, status):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_player_status, (status, player_id))
        self.conn.commit()
