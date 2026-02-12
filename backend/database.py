import sqlite3


conn = sqlite3.connect("alerts.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    time TEXT,
    severity TEXT,
    score REAL
)
""")
conn.commit()




def save_alert(alert):
    cursor.execute(
        "INSERT INTO alerts VALUES (?, ?, ?)",
        (alert['time'], alert['severity'], alert['score'])
    )
    conn.commit()