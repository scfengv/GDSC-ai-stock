# pip install accelerate -U

import os
import torch
import evaluate
import warnings
import accelerate
import numpy as np
import pandas as pd

from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

warnings.simplefilter("ignore")

f = 'PATH_TO_FILE'
df = pd.read_csv(f)

id2label = {0: "Class1", 1: "Class2", 2: "Class3"}
label2id = {"Class1": 0, "Class2": 1, "Class3": 2}

## If necessary ##
# df["Topic"] = df["Topic"].map(label2id)

train_df, val_df = train_test_split(df, test_size = 0.3, stratify = df["Topic"], random_state = 42)

train_text = train_df["text"].to_list()
val_text = val_df["text"].to_list()

train_topic = train_df["Topic"].to_list()
val_topic = val_df["Topic"].to_list()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bert = "google-bert/bert-large-uncased"
tokenizer = AutoTokenizer.from_pretrained(bert)
model = AutoModelForSequenceClassification.from_pretrained(
    bert, num_labels = 3, id2label = id2label, label2id = label2id
    ).to(device)   ### num_labels ###

class GDSCDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)
    
train_encoding = tokenizer(train_text, truncation = True, padding = True, max_length = 512)
val_encoding = tokenizer(val_text, truncation = True, padding = True, max_length = 512)

train_ds = GDSCDataset(train_encoding, train_topic)
val_ds = GDSCDataset(val_encoding, val_topic)

### Determine optimal batch_size by training data size
training_args = TrainingArguments(
    logging_steps = 10,
    warmup_steps = 10,
    weight_decay = 0.01,
    learning_rate = 5e-5,
    num_train_epochs = 30,
    logging_dir = './logs',
    output_dir = './results',
    evaluation_strategy = "steps",
    load_best_model_at_end = True,
    per_device_eval_batch_size = 128,
    per_device_train_batch_size = 128,
)

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis = -1)
    return metric.compute(predictions = predictions, references = labels)

trainer = Trainer(
    model = model,
    args = training_args,
    train_dataset = train_ds,
    eval_dataset = val_ds,
    compute_metrics = compute_metrics
)

trainer.train()

model_path = "./MODEL_PATH"
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)

## Load the model ##
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)