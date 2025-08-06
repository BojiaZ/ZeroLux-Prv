# normalize_hashes.py
import os, sqlite3

base_dir = os.path.dirname(__file__)                # .../ZeroLux_Antivirus/db
root_dir = os.path.abspath(os.path.join(base_dir, '..'))  # .../ZeroLux_Antivirus
db_path  = os.path.join(root_dir, 'db', 'mal_hashes.db')

print(f"Normalizing database at: {db_path}")

# 2. 打开并更新
conn = sqlite3.connect(db_path)
cur  = conn.cursor()

# 3. 把所有 md5 转成小写
cur.execute("UPDATE hashes SET md5 = lower(md5);")
conn.commit()
conn.close()

print("✅ All hashes normalized to lowercase.")
