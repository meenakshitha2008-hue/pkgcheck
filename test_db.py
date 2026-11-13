from db import init_db, log_prediction, get_conn

init_db()
print("new row id:", log_prediction("testpkg", "SAFE", 0.1, ["test"]))

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT id, name, verdict FROM predictions")
print(cur.fetchall())
conn.close()