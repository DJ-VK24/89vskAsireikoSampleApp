import sys, datetime

sys.path.append('C:\\sample_app')
import sqlite3
from app import settings

def create():
    try:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY NOT NULL,
                    text TEXT NOT NULL,
                    user_id INT NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT '{}'
                )
            """.format(datetime.datetime.now())
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS shared_notes (
                    user_id INT NOT NULL,
                    note_id INT NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT '{}',
                    PRIMARY KEY (user_id, note_id)
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
