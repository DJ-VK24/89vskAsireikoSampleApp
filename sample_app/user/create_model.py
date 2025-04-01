import sys, datetime

sys.path.append('C:\\sample_app')
import sqlite3
from app import settings

def create():
    try:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY NOT NULL,
                    email VARCHAR(256) UNIQUE NOT NULL,
                    name VARCHAR(25) NOT NULL,
                    surname VARCHAR(25) NOT NULL,
                    password VARCHAR(256) NOT NULL,
                    role TEXT CHECK(role IN ('user', 'admin')) NOT NULL DEFAULT 'user',
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
