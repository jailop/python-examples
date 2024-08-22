import os
import sqlite3
import utils

def createdb():
    """
    To create a demostrative user table in SQLite.
    If the table already exists, it is dropped and created again.
    """
    con = sqlite3.connect(os.environ["DBNAME"])
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (username text, password text)")
    con.commit()

def populatedb():
    """
    Insert synthetic data into the users database, to be used as examples.
    """
    con = sqlite3.connect(os.environ["DBNAME"])
    cur = con.cursor()
    examples = [
        {"username": "adam", "password": "1234"},
        {"username": "rosie", "password": "mypasswd"},
        {"username": "jane", "password": "secret"},
    ]
    for example in examples:
        cur.execute("INSERT INTO users VALUES ('{}', '{}')".format(
            example["username"],
            utils.hashtxt(example["password"])
        ))
    con.commit()

if __name__ == "__main__":
    if not utils.checkenviron():
        raise Exception("No required environment variables has been defined")
    createdb()
    populatedb()
