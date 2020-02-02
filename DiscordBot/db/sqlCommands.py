sql_create_users_table = """CREATE TABLE IF NOT EXISTS players (
                                id INTEGER PRIMARY KEY,
                                status INTEGER
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

sql_insert_player = """INSERT INTO players(id, status)
                        VALUES(?, ?) """

sql_select_player_exists = """SELECT 1 
                            FROM players
                            WHERE id=?"""

sql_select_player_status = """SELECT status
                                FROM players
                                WHERE id=?"""

sql_update_player_status = """UPDATE players
                            SET status=?
                            WHERE id=?"""

sql_select_active_player = """SELECT 1
                            FROM players
                            WHERE status=1
                            AND id=?"""

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