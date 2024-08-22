import sqlite3
import os
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 定义类别
categories = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]  # 添加更多类别

# 加载预训练的BERT模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(categories))

# 需要先训练模型，这里省略训练步骤，假设模型已经训练好并保存在`./bert_model`路径
# model.load_state_dict(torch.load("./bert_model/pytorch_model.bin"))

def categorize_description(description):
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=1).item()
    return categories[predicted_class_id]

def process_database(file_path):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    cursor.execute("ALTER TABLE videos ADD COLUMN category TEXT")
    
    cursor.execute("SELECT rowid, video_description FROM videos")
    rows = cursor.fetchall()
    
    for row in rows:
        rowid, description = row
        category = categorize_description(description)
        cursor.execute("UPDATE videos SET category = ? WHERE rowid = ?", (category, rowid))
    
    conn.commit()
    conn.close()

# 遍历所有数据库文件
db_folder = "/path/to/your/databases"
for filename in os.listdir(db_folder):
    if filename.endswith(".db"):
        file_path = os.path.join(db_folder, filename)
        process_database(file_path)

print("All databases processed.")
