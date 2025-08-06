import sqlite3,os

# 脚本位于 .../ZeroLux_Antivirus/db/add.py
base_dir = os.path.dirname(__file__)                # .../ZeroLux_Antivirus/db
root_dir = os.path.abspath(os.path.join(base_dir, '..'))  # .../ZeroLux_Antivirus
db_path  = os.path.join(root_dir, 'db', 'mal_hashes.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 测试一个已知的hash值（假设这个hash在你的txt里）
test_hash = 'ecdca2b158cf3197bd38dc3139008685'  # 这是MD5空文件的hash，换成你库里的一个实际hash

cur.execute("SELECT md5 FROM hashes WHERE md5 = ?", (test_hash,))

result = cur.fetchone()

if result:
    print(f"Hash {test_hash} 找到了，数据库有效！")
else:
    print(f"Hash {test_hash} 不存在，数据库可能不完整！")

conn.close()
