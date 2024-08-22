import os
import sqlite3
import utils

def unsafe_authenticate(username, password) -> bool:
    con = sqlite3.connect(os.environ["DBNAME"])
    cur = con.cursor()
    stmt = """
        SELECT COUNT(*)
            FROM users
            WHERE username='{}' AND password='{}'
    """.format(username, utils.hashtxt(password))
    # print(stmt)
    res = cur.execute(stmt)
    return res.fetchone()[0] > 0

def safer_authenticate(username, password) -> bool:
    flag = True
    invalid_chars = ["'"]
    for ch in invalid_chars:
        if ch in username or ch in password:
            flag = False
    return unsafe_authenticate(username, password) if flag else False

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    if unsafe_authenticate(username, password):
        print("Login accepted. Welcome!")
    else:
        print("Invalid username or password. Try again.")
