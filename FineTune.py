import os
import numpy as np
import pandas as pd
from typing import Dict, Optional, Union, List
from dataclasses import dataclass

import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    PreTrainedTokenizer,
    PreTrainedModel
)
from sklearn.metrics import f1_score

@dataclass
class ModelConfig:
    """Configuration for model training"""
    model_name: str = "google-bert/bert-large-uncased"
    num_labels: int = 3
    max_length: int = 512
    train_batch_size: int = 32
    eval_batch_size: int = 32
    learning_rate: float = 2e-5
    num_epochs: int = 5
    weight_decay: float = 0.01
    warmup_steps: int = 500
    logging_steps: int = 100
    save_steps: int = 500
    output_dir: str = "./model_output"
    
class TextDataset(Dataset):
    """Custom dataset for text classification"""
    def __init__(self, texts: List[str], labels: List[int], tokenizer: PreTrainedTokenizer, max_length: int):
        self.encodings = tokenizer(
            texts,
            truncation = True,
            padding = True,
            max_length = max_length,
            return_tensors = "pt"
        )
        self.labels = labels

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        item = {
            key: val[idx] for key, val in self.encodings.items()
        }
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self) -> int:
        return len(self.labels)

class BERTFineTuner:
    """Main class for BERT fine-tuning process"""
    def __init__(self, config: ModelConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = None
        self.trainer = None
        
    def prepare_model(self, label2id: Optional[Dict[str, int]] = None) -> None:
        """Initialize the model with given configuration"""
        model_config = {
            "num_labels": self.config.num_labels,
        }
        if label2id:
            model_config.update({
                "label2id": label2id,
                "id2label": {v: k for k, v in label2id.items()}
            })
            
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.config.model_name,
            **model_config
        ).to(self.device)

    def prepare_data(self, df: pd.DataFrame, text_col: str, label_col: str, 
                    test_size: float = 0.2, val_size: float = 0.1) -> tuple:
        """Prepare datasets for training, validation and testing"""
        train_df, temp_df = train_test_split(
            df, test_size = test_size + val_size, stratify = df[label_col], random_state = 42
        )
        
        relative_val_size = val_size / (test_size + val_size)
        val_df, test_df = train_test_split(
            temp_df, test_size = 0.5, stratify = temp_df[label_col], random_state = 42
        )
        
        # Create datasets
        train_dataset = TextDataset(
            train_df[text_col].tolist(),
            train_df[label_col].tolist(),
            self.tokenizer,
            self.config.max_length
        )
        
        val_dataset = TextDataset(
            val_df[text_col].tolist(),
            val_df[label_col].tolist(),
            self.tokenizer,
            self.config.max_length
        )
        
        test_dataset = TextDataset(
            test_df[text_col].tolist(),
            test_df[label_col].tolist(),
            self.tokenizer,
            self.config.max_length
        )
        
        return train_dataset, val_dataset, test_dataset

    @staticmethod
    def compute_metrics(eval_pred) -> Dict[str, float]:
        """Compute metrics for evaluation"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis = 1)
        return {
            "f1_score": f1_score(predictions, labels, average = "weighted")
        }

    def train(self, train_dataset: Dataset, val_dataset: Dataset) -> None:
        """Train"""
        training_args = TrainingArguments(
            output_dir = self.config.output_dir,
            num_train_epochs = self.config.num_epochs,
            per_device_train_batch_size = self.config.train_batch_size,
            per_device_eval_batch_size = self.config.eval_batch_size,
            learning_rate = self.config.learning_rate,
            weight_decay = self.config.weight_decay,
            warmup_steps = self.config.warmup_steps,
            logging_steps = self.config.logging_steps,
            save_steps = self.config.save_steps,
            evaluation_strategy = "steps",
            load_best_model_at_end = True,
            metric_for_best_model = "f1_score"
        )

        self.trainer = Trainer(
            model = self.model,
            args = training_args,
            train_dataset = train_dataset,
            eval_dataset = val_dataset,
            compute_metrics = self.compute_metrics
        )
        
        self.trainer.train()

    def evaluate(self, test_dataset: Dataset) -> Dict[str, float]:
        """Evaluate"""
        return self.trainer.evaluate(test_dataset)

    def save_model(self, path: str) -> None:
        """Save the fine-tuned model and tokenizer"""
        if not os.path.exists(path):
            os.makedirs(path)
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)

    def predict(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Make predictions on new texts"""
        if isinstance(texts, str):
            texts = [texts]
            
        inputs = self.tokenizer(
            texts,
            truncation = True,
            padding = True,
            max_length = self.config.max_length,
            return_tensors = "pt"
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.softmax(outputs.logits, dim = -1)
            
        return predictions.cpu().numpy()

if __name__  ==  "__main__":
    config = ModelConfig(
        model_name = "google-bert/bert-large-uncased",
        num_labels = 3,
        train_batch_size = 32,
        eval_batch_size = 32,
        learning_rate = 2e-5,
        num_epochs = 5
    )

    fine_tuner = BERTFineTuner(config)
    label2id = {"negative": 0, "neutral": 1, "positive": 2}
    
    fine_tuner.prepare_model(label2id)
    
    ## Earnings call
    df = pd.read_csv("earningscall_final.csv", encoding = "utf-8", names = ["summary","label","score","Generated_Text"])
    
    ## News
    # df = pd.read_csv("training_set.csv", encoding = "utf-8", names = ["summary","label","score","Generated_Text"])
    # df["label"].replace({"neutral": "0", "positive": "1", "negative": "1"}, inplace = True)
    train_dataset, val_dataset, test_dataset = fine_tuner.prepare_data(
        df, 
        text_col = "text", 
        label_col = "label"
    )
    
    fine_tuner.train(train_dataset, val_dataset)

    results = fine_tuner.evaluate(test_dataset)
    print(f"Evaluation results: {results}")
    
    fine_tuner.save_model("./saved_model")
    
    torch.cuda.empty_cache()