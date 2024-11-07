# Stock Market Analysis and Prediction System

A comprehensive system that combines web crawling, sentiment analysis, and deep learning to predict short-term stock price movements. The system integrates news sentiment with technical indicators to provide more accurate stock price predictions.

Check out [our portfolio](https://scfengv.github.io/GDSC-ai-stock/)

## Contributors
[scfengv](https://github.com/scfengv)
- LSTM model developing
  - Check [`StockPredictor`](https://github.com/scfengv/GDSC-ai-stock/blob/main/LSTM.py) in `LSTM.py`
- News, Tweets, Earnings Call BERT model fine-tuning
  - Check [`FineTune.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/FineTune.py) and [`PyTorch BertClassification Model Training.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/PyTorch%20BertClassification%20Model%20Training.py)
- CNBC and Yahoo Finance News Web crawling
  - Check [`News_Crawler.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/News_Crawler.py)

[CX330Blake](https://github.com/CX330Blake)
- Tweets Web crawling
  - Check [`Tweet_Crawler.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/Tweet_Crawler.py)
- Tweets BERT model fine-tuning
  - Check [`FineTune.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/FineTune.py)

[3Frank3](https://github.com/3Frank3) & [weip12](https://github.com/weip12)
- Earnings Call BERT model fine-tuning
  - Check [`FineTune.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/FineTune.py)
- Earnings Call summarization
  - Check [`Summary.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/data/Earnings%20Call/Summary.py)

[C0D1R](https://github.com/C0D1R)
- Portfolio pages design
  - Check [GitHub pages](https://scfengv.github.io/GDSC-ai-stock/)

[yichen7299](https://github.com/yichen7299)
- News BERT model fine-tuning
  - Check [`FineTune.py`](https://github.com/scfengv/GDSC-ai-stock/blob/main/FineTune.py)

## 🌟 Features

- Automated data collection from multiple sources:
  - Yahoo Finance news articles
  - CNBC news articles
  - Earnings call transcripts
  - Tweets
- Sentiment analysis using fine-tuned BERT model
- Stock price prediction using LSTM with sentiment features
- Scalable architecture for multiple stocks

## 🏗 System Architecture

### 1. Data Collection (`News_Crawler.py`)
- Implements web crawling using Selenium and BeautifulSoup4
- Collects news titles from Yahoo Finance and CNBC
- Stores data in CSV format with timestamps
- Handles rate limiting and browser automation

### 2. Sentiment Analysis (`FineTune.py`)
- Fine-tunes BERT model for financial sentiment analysis
- Uses pseudo-labeling technique for efficient data labeling
- Supports three sentiment classes: positive, neutral, negative
- Includes custom dataset handling and metrics computation

### 3. Stock Price Prediction (`LSTM.py`)
- Implements LSTM model for time series prediction
- Features:
  - Technical indicators integration
  - VIX index integration
  - Sentiment score integration
  - Hyperparameter tuning using Keras Tuner

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

Required packages:
- tensorflow
- torch
- transformers
- pandas
- numpy
- selenium
- beautifulsoup4
- yfinance
- keras-tuner
- scikit-learn

### Running the Pipeline

1. **Data Collection**
```bash
python News_Crawler.py
```

2. **Model Fine-tuning**
```bash
python FineTune.py
```

3. **Stock Prediction**
```bash
python LSTM.py
```

## 📊 Model Architecture

### BERT Fine-tuning
- Base model: google-bert/bert-large-uncased
- Custom classification head
- Configurable hyperparameters:
  - Learning rate
  - Batch size
  - Number of epochs
  - Maximum sequence length

### LSTM Model
- Features:
  - Close price
  - Volume
  - VIX index
  - Technical indicators
  - Sentiment scores
- Configurable architecture:
  - Number of LSTM layers
  - Units per layer
  - Dropout rates
  - Dense layer configuration

## 🔧 Configuration

### BERT Fine-tuning Configuration
```python
config = ModelConfig(
    model_name = "google-bert/bert-large-uncased",
    num_labels = 3,
    train_batch_size = 32,
    eval_batch_size = 32,
    learning_rate = 2e-5,
    num_epochs = 5
)
```

### LSTM Configuration
- Configurable through `StockPredictor` class initialization
- Supports hyperparameter tuning via Keras Tuner

## 📈 Performance Metrics

### Sentiment Analysis
- F1 Score (weighted average)
- Classification accuracy
- Confusion matrix

### Stock Prediction
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- Direction accuracy

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Future Improvements

1. Add support for more news sources
2. Implement real-time prediction pipeline
3. Add more technical indicators
4. Enhance model interpretability
5. Add backtesting framework
6. Implement portfolio optimization

## ⚠️ Disclaimer

This project is for educational purposes only. The predictions should not be used as financial advice. Always do your own research before making investment decisions.
