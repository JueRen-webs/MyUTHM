import sqlite3
from schemas.user import UserCreate, LogCreate

def get_user_by_id(db: sqlite3.Connection, user_id: str) -> dict | None:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE User_ID = ?", (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def create_user(db: sqlite3.Connection, user: UserCreate) -> dict:
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO Users (User_ID, Name, Email, Phone, Role, FCM_Token, Is_Active, Password_Hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user.User_ID, user.Name, user.Email, user.Phone, user.Role.value, user.FCM_Token, int(user.Is_Active), user.Password_Hash)
    )
    db.commit()
    return get_user_by_id(db, user.User_ID)

# 复杂的 JOIN 查询：获取部门时，连带查出办公地点（Locations）的名称和 URL


def write_system_log(db: sqlite3.Connection, log: LogCreate) -> bool:
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO Logs (User_ID, Time, Date, Details)
        VALUES (?, ?, ?, ?)
        """,
        (log.User_ID, log.Time.strftime("%H:%M:%S") if log.Time else None,
         log.Date.strftime("%Y-%m-%d") if log.Date else None, log.Details)
    )
    db.commit()
    return True