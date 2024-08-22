import os
import hashlib

def checkenviron() -> bool:
    """
    To check if the required environment variables are defined.
    """
    flag = True
    vars = ["DBNAME", "SALT"]
    for var in vars:
        if var not in os.environ:
            flag = False
    return flag

def hashtxt(plaintext: str) -> str:
    """
    To generated a hashed representation from plain text values. This function
    is intended to protect password when they are stored in a database.
    """
    m = hashlib.sha256()
    m.update(plaintext.encode() + os.environ["SALT"].encode())
    return m.hexdigest()
