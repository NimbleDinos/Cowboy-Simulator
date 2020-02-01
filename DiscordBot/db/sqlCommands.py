sql_create_users_table = """CREATE TABLE IF NOT EXISTS players (
                                id INTEGER PRIMARY KEY
                        ); """

sql_insert_player = """INSERT INTO players(id)
                        VALUES(?) """

sql_select_player = """SELECT 1 
                        FROM players
                        WHERE id=?"""