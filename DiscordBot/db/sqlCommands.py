# ---- CREATE TABLES ----

sql_create_users_table = """CREATE TABLE IF NOT EXISTS players (
                                id INTEGER PRIMARY KEY,
                                status INTEGER,
                                place TEXT,
                                intown BOOLEAN
                        ); """

sql_create_inventory_table = """CREATE TABLE IF NOT EXISTS inventory (
                                id INTEGER PRIMARY KEY,
                                health INTEGER,
                                gold INTEGER,
                                gun INTEGER,
                                booze INTEGER,
                                hat INTEGER,
                                horse INTEGER,
                                lasso INTEGER,
                                pickaxe INTEGER
                        );"""

sql_insert_player = """INSERT INTO players(id, status, place, intown)
                        VALUES(?, ?, ?, ?) """

sql_insert_inventory = """INSERT INTO inventory(id, health, gold, gun, booze, hat, horse, lasso, pickaxe)
                        VALUES(?, ?, ?, ?, ?, ? ,? ,?, ?) """

# ---- SELECT STATEMENTS ----
sql_select_player_exists = """SELECT 1 
                            FROM players
                            WHERE id=?"""

sql_select_player_status = """SELECT status
                                FROM players
                                WHERE id=?"""

sql_select_active_player = """SELECT 1
                            FROM players
                            WHERE status=1
                            AND id=?"""

sql_select_player_place = """SELECT place
                            FROM players
                            WHERE id=?"""

sql_select_player_intown = """SELECT intown
                            FROM players
                            WHERE id=?"""

sql_select_all_inventory = """SELECT * 
                            FROM inventory
                            WHERE id=?
                            """

sql_select_gold = """SELECT gold 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_health = """SELECT health 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_gun = """SELECT gun 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_booze = """SELECT booze 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_hat = """SELECT hat 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_horse = """SELECT horse 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_lasso = """SELECT lasso 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_pickaxe = """SELECT pickaxe 
                    FROM inventory
                    WHERE id=?
                    """

sql_select_option = """SELECT ?
					FROM inventory
					WHERE id=?"""

# ---- UPDATE STATEMENTS ----

sql_update_all_player_status = """UPDATE players
                                SET status=0;"""

sql_update_player_status = """UPDATE players
                            SET status=?
                            WHERE id=?"""

sql_update_player_place = """UPDATE players
                            SET place=?
                            WHERE id=?"""

sql_update_player_intown = """UPDATE players
                            SET intown=?
                            WHERE id=?"""

sql_update_health = """UPDATE inventory
                        SET health=?
                        WHERE id=?"""

sql_update_gold = """UPDATE inventory
                        SET gold=?
                        WHERE id=?"""

sql_update_gun = """UPDATE inventory
                        SET gun=?
                        WHERE id=?"""

sql_update_booze = """UPDATE inventory
                        SET booze=?
                        WHERE id=?"""

sql_update_hat = """UPDATE inventory
                        SET hat=?
                        WHERE id=?"""

sql_update_horse = """UPDATE inventory
                        SET horse=?
                        WHERE id=?"""

sql_update_lasso = """UPDATE inventory
                        SET lasso=?
                        WHERE id=?"""

sql_update_pickaxe = """UPDATE inventory
                        SET pickaxe=?
                        WHERE id=?"""
