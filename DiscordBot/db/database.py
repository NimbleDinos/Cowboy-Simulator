import sqlite3
from sqlite3 import Error
import db.sqlCommands


class Database:
    def __init__(self, db_location):
        self.conn = self.create_connection(db_location)

    @staticmethod
    def create_connection(db_file):
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
            self.create_table(db.sqlCommands.sql_create_player_table)
        else:
            print("Error: Could not establish connection to database")

    def create_inventory_table(self):
        if self.conn is not None:
            self.create_table(db.sqlCommands.sql_create_inventory_table)
        else:
            print("Error: Could not establish connection to database")

    def create_skills_table(self):
        if self.conn is not None:
            self.create_table(db.sqlCommands.sql_create_skills_table)
        else:
            print("Error: Could not establish connection to database")

    def add_player(self, player):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_insert_player, player)
        self.conn.commit()
        return cur.lastrowid

    def add_inventory(self, inventory):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_insert_inventory, inventory)
        self.conn.commit()
        return cur.lastrowid

    def add_skills(self, skills):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_insert_skill, skills)
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

    def select_player_place(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_place, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_player_intown(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_intown, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_player_name(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_name, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_player_inventory(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_all_inventory, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_player_item(self, item, player_id):
        cur = self.conn.cursor()
        cur.execute("SELECT {0} FROM inventory WHERE id={1}".format(item, player_id))
        rows = cur.fetchall()
        return rows

    def select_player_skill(self, player_id, skill):
        cur = self.conn.cursor()
        cur.execute("SELECT {0} FROM skills WHERE id={1}".format(skill, player_id))
        rows = cur.fetchall()
        return rows

    def select_player_skills(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_skills, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_all_skills(self):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_all_skills)
        rows = cur.fetchall()
        return rows

    def update_all_player_status(self):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_all_player_status, ())
        self.conn.commit()

    def update_player_status(self, player_id, status):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_player_status, (status, player_id))
        self.conn.commit()

    def update_player_place(self, player_id, place):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_player_place, (place, player_id))
        self.conn.commit()

    def update_player_intown(self, player_id, in_town):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_player_intown, (in_town, player_id))
        self.conn.commit()

    def update_player_item(self, item, amount, player_id):
        cur = self.conn.cursor()
        cur.execute("UPDATE inventory SET {0} = {1} WHERE id={2}".format(item, amount, player_id))
        self.conn.commit()

    def update_player_skill(self, skill, amount, player_id):
        cur = self.conn.cursor()
        cur.execute("UPDATE skills SET {0} = {1} WHERE id={2}".format(skill, amount, player_id))
        self.conn.commit()
