import sqlite3

from app import settings


class DB:
    def __init__(self):
        self.conn = DB.connect()
        self.cursor = self.conn.cursor()

    def connect():
        try:
            with sqlite3.connect(settings.DB_NAME) as conn:
                return conn
        except sqlite3.OperationalError as err:
            return None

    def insert_user(self, table, values):
            try:
                query = """
                    INSERT INTO {0}(email,name,surname,password,created)
                    VALUES({1})
                """.format(table, values)
                return self.cursor.execute(query)
            except:
                return False

    def select(self, table, filter):
        try:
            query_filter = """
                SELECT * FROM {0}
                WHERE {1}
            """.format(table, filter)
            query_all = """
                SELECT * FROM {0}
            """.format(table)

            query = query_filter if filter != '' else query_all
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except:
            return None
        
    def insert_note(self, table, values):
        try:
            query = """
                INSERT INTO {0}(text,user_id,created)
                VALUES({1})
            """.format(table, values)
            self.cursor.execute(query)
            return True
        except:
            return False

    def insert_task(self, table, values):
        try:
            query = """
                INSERT INTO {0}(name,user_id,created)
                VALUES({1})
            """.format(table, values)
            self.cursor.execute(query)
            return True
        except:
            return False
        
    def insert_subtask(self, table, values):
        try:
            query = """
                INSERT INTO {0}(name,task_id,is_complete,created)
                VALUES({1})
            """.format(table, values)
            self.cursor.execute(query)
            return True
        except:
            return False
        
    def insert_shared_note(self, table, values):
        try:
            query = """
                INSERT INTO {0}(user_id,note_id,created)
                VALUES({1})
            """.format(table, values)
            self.cursor.execute(query)
            return True
        except:
            return False

    def delete(self, table, filter):
        try:
            query = """
                DELETE FROM {0}
                WHERE {1}
            """.format(table, filter)
            self.cursor.execute(query)
            return True
        except:
            return False
