"""

    import sqlite3 as sq3` is importing the `sqlite3` module and assigning it the alias `sq3`. This
    allows us to use the functionality provided by the `sqlite3` module by referencing it as `sq3`
    in our code.

"""
import sqlite3 as sq3

connection = sq3.connect("database.db")

with open ('schema.sql', encoding='utf-8') as db:
    connection.executescript(db.read())
cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?,?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?,?)",
            ('Second Post', 'Content for the second post')
            )
connection.commit()
connection.close()
