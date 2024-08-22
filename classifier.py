import sqlite3
import os
from collections import defaultdict

# 定义类别和对应的关键词
categories = {
    "Category1": ["keyword1", "keyword2", "keyword3"],
    "Category2": ["keyword4", "keyword5"],
    "Category3": ["keyword6", "keyword7", "keyword8"],
    # 添加更多类别和关键词
}

def categorize_description(description, categories):
    description = description.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in description:
                return category
    return "Uncategorized"

def process_database(file_path, categories):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    cursor.execute("ALTER TABLE videos ADD COLUMN category TEXT")
    
    cursor.execute("SELECT rowid, video_description FROM videos")
    rows = cursor.fetchall()
    
    for row in rows:
        rowid, description = row
        category = categorize_description(description, categories)
        cursor.execute("UPDATE videos SET category = ? WHERE rowid = ?", (category, rowid))
    
    conn.commit()
    conn.close()

# 遍历所有数据库文件
db_folder = "/path/to/your/databases"
for filename in os.listdir(db_folder):
    if filename.endswith(".db"):
        file_path = os.path.join(db_folder, filename)
        process_database(file_path, categories)

print("All databases processed.")
