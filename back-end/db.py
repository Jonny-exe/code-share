# db.py
import sys
import mariadb

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="code-share",
        password="password",
        host="127.0.0.1",
        port=3306,
        database="code_share",
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


def get_current_likes(id):
    cur.execute("select likes from messages where id=?", (id,))
    return cur.fetchone()[0]


def get_messages():
    cur.execute("select text, likes, id from messages order by id desc limit 30")
    return cur.fetchall()


def add_like(id, newLikes):
    cur.execute("update messages set likes=? where id=?", (newLikes, id))


def get_current_files(id):
    cur.execute("select likes from messages where id=?", (id))
    return cur.fetchone()[0]


def insert_message(text):
    cur.execute("insert into messages(text,likes) values(?,?)", (text, 0))
    conn.commit()
