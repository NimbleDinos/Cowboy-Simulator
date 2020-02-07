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
            self.create_table(db.sqlCommands.sql_create_users_table)
        else:
            print("Error: Could not establish connection to database")

    def create_inventory_table(self):
        if self.conn is not None:
            self.create_table(db.sqlCommands.sql_create_inventory_table)
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

    def select_active_players(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_active_player, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_player_place(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_place, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_player_intwon(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_player_intown, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_inventory(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_all_inventory, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_health(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_health, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_gold(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_gold, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_gun(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_gun, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_booze(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_booze, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_hat(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_hat, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_horse(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_horse, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_lasso(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_lasso, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_pickaxe(self, player_id):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_select_pickaxe, (player_id,))
        rows = cur.fetchall()
        return rows

    def select_user_item(self, item, player_id):
        cur = self.conn.cursor()
        cur.execute("SELECT {0} FROM inventory WHERE id={1}".format(item, player_id))
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

    def update_player_health(self, player_id, health):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_health, (health, player_id))
        self.conn.commit()

    def update_player_gold(self, player_id, gold):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_gold, (gold, player_id))
        self.conn.commit()

    def update_player_gun(self, player_id, gun):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_gun, (gun, player_id))
        self.conn.commit()

    def update_player_booze(self, player_id, booze):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_booze, (booze, player_id))
        self.conn.commit()

    def update_player_hat(self, player_id, hat):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_hat, (hat, player_id))
        self.conn.commit()

    def update_player_horse(self, player_id, horse):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_horse, (horse, player_id))
        self.conn.commit()

    def update_player_lasso(self, player_id, lasso):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_lasso, (lasso, player_id))
        self.conn.commit()

    def update_player_pickaxe(self, player_id, pickaxe):
        cur = self.conn.cursor()
        cur.execute(db.sqlCommands.sql_update_pickaxe, (pickaxe, player_id))
        self.conn.commit()

    def update_player_item(self, item, amount, player_id):
        cur = self.conn.cursor()
        cur.execute("UPDATE inventory SET {0} = {1} WHERE id={2}".format(item, amount, player_id))
        rows = cur.fetchall()
        return rows
