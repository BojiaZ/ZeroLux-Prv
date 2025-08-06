import os
import sqlite3

# 脚本位于 .../ZeroLux_Antivirus/db/add.py
base_dir = os.path.dirname(__file__)                # .../ZeroLux_Antivirus/db
root_dir = os.path.abspath(os.path.join(base_dir, '..'))  # .../ZeroLux_Antivirus
db_path  = os.path.join(root_dir, 'db', 'mal_hashes.db')

# EICAR 标准 MD5
eicar_md5 = '44d88612fea8a8f36de82e1278abb02f'.lower()

conn = sqlite3.connect(db_path)
cur  = conn.cursor()

# 插入（已存在则忽略）
cur.execute(
    "INSERT OR IGNORE INTO hashes (md5) VALUES (?)",
    (eicar_md5,)
)

conn.commit()
conn.close()

print(f"Inserted EICAR MD5 {eicar_md5} into database.")
