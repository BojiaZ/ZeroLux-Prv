import sqlite3

txt_path = "engine/engine_md5_db.txt"  # 你的txt路径
db_path = "mal_hashes.db"

con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS hashes (md5 TEXT PRIMARY KEY)")

batch = []
batch_size = 1000
progress_interval = 100000   # 每10万条报一次进度

with open(txt_path, "r") as f:
    for i, line in enumerate(f, 1):
        h = line.strip()
        if not h:
            continue
        batch.append((h,))
        if len(batch) == batch_size:
            cur.executemany("INSERT OR IGNORE INTO hashes VALUES (?)", batch)
            con.commit()
            batch.clear()
        if i % progress_interval == 0:
            print(f"已导入 {i:,} 行")
    # 插入剩余部分
    if batch:
        cur.executemany("INSERT OR IGNORE INTO hashes VALUES (?)", batch)
        con.commit()
print("导入完成！")
con.close()
