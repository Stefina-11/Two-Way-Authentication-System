import json
from pathlib import Path
import bcrypt  # for secure password hashing

USER_DB = Path("core/data/users.json")
USER_DB.parent.mkdir(exist_ok=True, parents=True)
if not USER_DB.exists():
    USER_DB.write_text("{}")

def register_user(username: str, password: str):
    users = json.loads(USER_DB.read_text())
    if username in users:
        return False
    pwd_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = pwd_hash
    USER_DB.write_text(json.dumps(users))
    return True


def authenticate_user(username: str, password: str):
    users = json.loads(USER_DB.read_text())
    hashed = users.get(username)
    if not hashed:
        return False
    return bcrypt.checkpw(password.encode(), hashed.encode())
