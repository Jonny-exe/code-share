# db.py
import sys
import mariadb
import setup_db

# Connect to MariaDB Platform

# Get Cursor
cur = setup_db.cur
setup_db.create_db()
setup_db.create_table()
print("HELLO")


def get_current_likes(id):
    cur.execute("select likes from messages where id=?", (id,))
    return cur.fetchone()[0]


def get_messages():
    cur.execute("select text, likes, id from messages order by quality desc limit 30")
    return cur.fetchall()


def add_like(new_likes, id):
    print(new_likes, id)
    query = f"update messages set likes={new_likes} where id={id}"
    print(query)
    cur.execute(query)
    # conn.commit()


def get_current_files(id):
    cur.execute("select likes from messages where id=?", (id))
    return cur.fetchone()[0]


def insert_message(message, quality):
    print(type(quality))
    cur.execute(
        "insert into messages(text,likes,quality) values(?, ?, ?)",
        (
            message["text"],
            0,
            quality,
        ),
    )


def get_message(id):
    cur.execute("select text, likes from messages where id = ?", (id,))
    return cur.fetchone()


def update_prediction(new_quality, id):
    cur.execute(
        "update messages set quality = ? where id = ?",
        (
            new_quality,
            id,
        ),
    )
