import sys, datetime

sys.path.append('C:\\sample_app')
import sqlite3
from app import settings

def create():
    try:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name VARCHAR(256) NOT NULL,
                    user_id INT NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT '{}'
                )
            """.format(datetime.datetime.now())
        )
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS subtasks (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name VARCHAR(256) NOT NULL,
                    task_id INT NOT NULL,
                    is_complete BOOLEAN CHECK(is_complete IN ('0', '1')) NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT '{}'
                )
            """.format(datetime.datetime.now())
        )
    except sqlite3.OperationalError as err:
        print(err)

conn = sqlite3.connect(settings.DB_NAME)
cursor = conn.cursor()
create()
conn.commit()
conn.close()
