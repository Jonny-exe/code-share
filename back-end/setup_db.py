# setup_db
import mariadb
import sys

try:
    conn = mariadb.connect(
        user="code-share",
        password="password",
        host="127.0.0.1",
        port=3306,
        database="code_share",
        autocommit=True,
    )
    print("Database set up")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


def create_db():
    cur.execute("CREATE DATABASE IF NOT EXISTS code_share")


def create_table():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS messages \
        (id int auto_increment PRIMARY KEY,\
         text longtext, likes int(11), quality int(1))"
    )


create_db()
create_table()
