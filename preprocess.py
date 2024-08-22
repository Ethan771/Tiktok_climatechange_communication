import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch

# 加载数据
df = pd.read_csv('base_data.csv')

# 转换类别标签为数值编码
categories = df['category'].unique().tolist()
df['label'] = df['category'].apply(lambda x: categories.index(x))

# 拆分数据集
train_texts, val_texts, train_labels, val_labels = train_test_split(df['video_description'].tolist(), df['label'].tolist(), test_size=0.2)

# 加载分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 编码数据
def tokenize_function(texts):
    return tokenizer(texts, padding="max_length", truncation=True, max_length=128, return_tensors="pt")

train_encodings = tokenize_function(train_texts)
val_encodings = tokenize_function(val_texts)

# 创建自定义数据集
class VideoDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = VideoDataset(train_encodings, train_labels)
val_dataset = VideoDataset(val_encodings, val_labels)

# 加载预训练的BERT模型
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(categories))

# 定义训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch"
)

# 使用Trainer进行训练
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()

# 保存模型
model.save_pretrained('./bert_model')
tokenizer.save_pretrained('./bert_model')

print("Model training completed and saved.")
