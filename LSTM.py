import numpy as np
import pandas as pd
import yfinance as yf
import keras_tuner as kt

from pickle import dump
from tensorflow.keras.models import Sequential
from typing import Tuple, List, Dict, Any
from pandas_datareader import data as pdr
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import save_model

class StockPredictor:
    def __init__(self, symbol: str, start_date: str, end_date: str):
        """
        Initialize the StockPredictor with stock symbol and date range.
        
        Args:
            symbol: Stock ticker symbol
            start_date: "YYYY-MM-DD"
            end_date: "YYYY-MM-DD"
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.model = None
        self.f_scaler = MinMaxScaler()
        self.t_scaler = MinMaxScaler()
        
    def _fetch_data(self) -> pd.DataFrame:
        """Fetch stock data and additional features."""
        df = yf.download(self.symbol, start=self.start_date, end=self.end_date).reset_index()
        df.columns = df.columns.droplevel(1)
        df = df.reset_index()
        print(df.head())
        vix = yf.download("^VIX", start=self.start_date, end=self.end_date).reset_index()
        vix.columns = vix.columns.droplevel(1)
        vix = vix.reset_index()
        print(vix.head())

        vix = vix[["Date", "Close"]]
        df["Delta"] = round(df["Close"].pct_change()*100, 4)
        df.dropna(inplace=True)

        df = pd.merge(df, vix, on="Date", suffixes=("_STOCK", "_VIX"))
        df.set_index("Date", inplace=True)

        # Calculate technical indicators
        df["Open_Close"] = ((df["Open"] - df["Close_STOCK"]) * 100 / df["Open"])
        # df["Open_Close"] = ((df["Open_STOCK"] - df["Close_STOCK"]) * 100 / df["Open_STOCK"])
        df["High_Low"] = ((df["High"] - df["Low"]) * 100 / df["Low"])
        
        df["Target"] = df["Close_STOCK"].shift(-1)
        df.dropna(inplace = True)
        
        return df
    
    def _prepare_data(self, df: pd.DataFrame, train_split: float = 0.7) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Prepare data for LSTM model."""
        features = df[["Close_STOCK", "Volume", "Close_VIX", "Open_Close", "High_Low"]]
        target = df["Target"]
        
        features_scaled = self.f_scaler.fit_transform(features)
        target_scaled = self.t_scaler.fit_transform(target.values.reshape(-1, 1))
        
        num_train = int(len(features_scaled) * train_split)
        x_train = features_scaled[:num_train]
        x_test = features_scaled[num_train:]
        y_train = target_scaled[:num_train]
        y_test = target_scaled[num_train:]
        
        # Reshape for LSTM
        x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
        x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
        
        return x_train, x_test, y_train, y_test
    
    def _build_model(self, hp: kt.HyperParameters) -> Sequential:
        """Build LSTM model with hyperparameters."""
        model = Sequential()
        
        model.add(LSTM(
            hp.Int("input_unit", 32, 512, step = 32),
            return_sequences = True,
            input_shape = (1, 5)  # 5 features
        ))
        
        # Additional LSTM layers
        for i in range(hp.Int("n_layers", 1, 4)):
            model.add(LSTM(
                hp.Int(f"lstm_{i}_units", 32, 512, step = 32),
                return_sequences = True
            ))
        
        model.add(Dropout(hp.Float("dropout_1", 0, 0.5, step = 0.1)))
        model.add(LSTM(hp.Int("layer_2_neurons", 32, 512, step = 32)))
        model.add(Dropout(hp.Float("dropout_2", 0, 0.5, step = 0.1)))
        model.add(Dense(hp.Int("dense_1_units", 32, 512, step = 32)))
        model.add(Dense(1))
        
        model.compile(loss = "mean_squared_error", optimizer = "adam", metrics = ["mse"])
        return model
    
    def train(self, max_trials: int = 20, epochs: int = 20, batch_size: int = 32) -> Dict[str, Any]:
        """
        Train the model using hyperparameter tuning.
        
        Returns:
            Dictionary containing training results and best parameters
        """
        df = self._fetch_data()
        x_train, x_test, y_train, y_test = self._prepare_data(df)
        
        # Initialize tuner
        tuner = kt.RandomSearch(
            self._build_model,
            objective = "val_mse",
            max_trials = max_trials,
            executions_per_trial = 1,
            overwrite = True,
            directory = "tuner_results",
            project_name = f"LSTM_{self.symbol}"
        )
        
        tuner.search(
            x = x_train,
            y = y_train,
            epochs = epochs,
            batch_size = batch_size,
            validation_data = (x_test, y_test)
        )
        
        self.model = tuner.get_best_models(num_models = 1)[0]
        loss = self.model.evaluate(x_test, y_test)
        
        return {
            "best_params": tuner.get_best_hyperparameters()[0].values,
            "test_loss": loss[0],
            "test_mse": loss[1]
        }
    
    def predict_next_days(self, days: int = 1) -> List[float]:
        """Predict stock prices for the next n days."""
        
        df = self._fetch_data()
        features = df[["Close_STOCK", "Volume", "Close_VIX", "Open_Close", "High_Low"]]
        last_features = self.f_scaler.transform(features.iloc[-1:])
        x_new = np.reshape(last_features, (1, 1, last_features.shape[1]))
        
        predictions = []
        for _ in range(days):
            predicted_scaled = self.model.predict(x_new)
            x_new[0, 0, 0] = predicted_scaled[0, 0]  # Update close price for next prediction
            predicted = self.t_scaler.inverse_transform(predicted_scaled)
            predictions.append(float(predicted[0, 0]))
        
        return predictions
    
    def save_model(self, model_path: str, scaler_path: str) -> None:
        """Save the trained model and scalers."""
        if self.model is None:
            raise ValueError("No trained model to save")
        
        save_model(self.model, model_path)
        dump(self.f_scaler, open(f"{scaler_path}_features.pkl", "wb"))
        dump(self.t_scaler, open(f"{scaler_path}_target.pkl", "wb"))
        
if __name__ == "__main__":
    predictor = StockPredictor(symbol = "TSLA", start_date = "2015-01-01", end_date = "2024-05-30")
    results = predictor.train(max_trials = 30, epochs = 50, batch_size = 32)
    print("Training Results:", results)
    
    next_day_prediction = predictor.predict_next_days(days = 1)
    print("Next Day Prediction:", next_day_prediction)
    
    predictor.save_model(model_path = "/content/drive/MyDrive/GDSC-ai-stock/LSTM/lstm_tsla_model.keras", scaler_path = "/content/drive/MyDrive/GDSC-ai-stock/LSTM/lstm_tsla_scaler")