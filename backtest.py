import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from pickle import load
from sklearn.preprocessing import MinMaxScaler

def backtest(symbol, start_date, end_date, model_path, f_scaler_path, t_scaler_path, 
             strategy='long_short', stop_loss_pct=0.05, take_profit_pct=None):
    """
    Backtests a trading strategy based on a trained LSTM model with enhanced stop loss.

    Args:
        symbol (str): Stock symbol to backtest.
        start_date (str): Start date for backtesting data.
        end_date (str): End date for backtesting data.
        model_path (str): Path to the trained Keras model.
        f_scaler_path (str): Path to the feature scaler.
        t_scaler_path (str): Path to the target scaler.
        strategy (str): 'long_short', 'long_only', or 'short_only'. Defaults to 'long_short'.
        stop_loss_pct (float): Stop loss percentage (default 0.05 = 5%).
        take_profit_pct (float): Take profit percentage (optional).
    """

    # Load model and scalers
    model = load_model(model_path)
    f_scaler = load(open(f_scaler_path, 'rb'))
    t_scaler = load(open(t_scaler_path, 'rb'))

    # Fetch data
    df = yf.download(symbol, start=start_date, end=end_date).reset_index()
    df.columns = df.columns.droplevel(1)
    df = df.reset_index()
    vix = yf.download("^VIX", start=start_date, end=end_date).reset_index()
    vix.columns = vix.columns.droplevel(1)
    vix = vix.reset_index()
    df = pd.merge(df, vix[['Close']], left_index=True, right_index=True, suffixes=('_STOCK', '_VIX'))
    df['Open_Close'] = ((df['Open'] - df['Close_STOCK']) * 100 / df['Open'])
    df['High_Low'] = ((df['High'] - df['Low']) * 100 / df['Low'])
    
    # Prepare features for prediction
    features = df[["Close_STOCK", "Volume", "Close_VIX", "Open_Close", "High_Low"]]
    features_scaled = f_scaler.transform(features)
    
    # Get predictions
    predictions_scaled = model.predict(np.reshape(features_scaled, (features_scaled.shape[0], 1, features_scaled.shape[1])))
    predictions = t_scaler.inverse_transform(predictions_scaled)
    df['Predicted_Close'] = predictions

    # Initialize columns for enhanced tracking
    df['Signal'] = 0
    df['Position'] = 0  # Track actual position (considering stop loss)
    df['Entry_Price'] = np.nan
    df['Stop_Loss_Price'] = np.nan
    df['Take_Profit_Price'] = np.nan
    df['Exit_Reason'] = ''
    
    # Generate initial signals
    df.loc[df['Predicted_Close'] > df['Close_STOCK'].shift(1), 'Signal'] = 1
    df.loc[df['Predicted_Close'] < df['Close_STOCK'].shift(1), 'Signal'] = -1

    # Apply strategy type
    if strategy == 'long_only':
        df.loc[df['Signal'] == -1, 'Signal'] = 0
    elif strategy == 'short_only':
        df.loc[df['Signal'] == 1, 'Signal'] = 0

    # Enhanced position management with stop loss and take profit
    current_position = 0
    entry_price = 0
    
    for i in range(1, len(df)):
        prev_position = current_position
        current_price = df.loc[i, 'Close_STOCK']
        
        # Check for stop loss or take profit exit first
        if current_position != 0:
            if current_position == 1:  # Long position
                # Check stop loss
                if current_price <= df.loc[i-1, 'Stop_Loss_Price']:
                    current_position = 0
                    df.loc[i, 'Exit_Reason'] = 'Stop Loss'
                # Check take profit
                elif take_profit_pct and current_price >= df.loc[i-1, 'Take_Profit_Price']:
                    current_position = 0
                    df.loc[i, 'Exit_Reason'] = 'Take Profit'
                    
            elif current_position == -1:  # Short position
                # Check stop loss (price going up)
                if current_price >= df.loc[i-1, 'Stop_Loss_Price']:
                    current_position = 0
                    df.loc[i, 'Exit_Reason'] = 'Stop Loss'
                # Check take profit (price going down)
                elif take_profit_pct and current_price <= df.loc[i-1, 'Take_Profit_Price']:
                    current_position = 0
                    df.loc[i, 'Exit_Reason'] = 'Take Profit'
        
        # If no position or exited, check for new signal
        if current_position == 0 and df.loc[i, 'Signal'] != 0:
            current_position = df.loc[i, 'Signal']
            entry_price = current_price
            df.loc[i, 'Entry_Price'] = entry_price
            df.loc[i, 'Exit_Reason'] = 'New Entry'
            
            # Set stop loss and take profit levels
            if current_position == 1:  # Long position
                df.loc[i, 'Stop_Loss_Price'] = entry_price * (1 - stop_loss_pct)
                if take_profit_pct:
                    df.loc[i, 'Take_Profit_Price'] = entry_price * (1 + take_profit_pct)
            elif current_position == -1:  # Short position
                df.loc[i, 'Stop_Loss_Price'] = entry_price * (1 + stop_loss_pct)
                if take_profit_pct:
                    df.loc[i, 'Take_Profit_Price'] = entry_price * (1 - take_profit_pct)
        
        # Update position and carry forward stop loss/take profit levels
        df.loc[i, 'Position'] = current_position
        if current_position != 0 and i > 0:
            if pd.isna(df.loc[i, 'Stop_Loss_Price']):
                df.loc[i, 'Stop_Loss_Price'] = df.loc[i-1, 'Stop_Loss_Price']
            if take_profit_pct and pd.isna(df.loc[i, 'Take_Profit_Price']):
                df.loc[i, 'Take_Profit_Price'] = df.loc[i-1, 'Take_Profit_Price']
    
    # Calculate returns
    df['Market_Returns'] = df['Close_STOCK'].pct_change()
    df['Strategy_Returns'] = df['Market_Returns'] * df['Position'].shift(1)

    # Transaction costs
    transaction_costs = 0.0005  # 5bps
    position_changes = df['Position'] != df['Position'].shift(1)
    df['Strategy_Returns'] -= position_changes * transaction_costs
    
    # PnL
    df['Cumulative_Market_Returns'] = (1 + df['Market_Returns']).cumprod()
    df['Cumulative_Strategy_Returns'] = (1 + df['Strategy_Returns']).cumprod()

    # Performance metrics
    annualized_return = (df['Cumulative_Strategy_Returns'].iloc[-1]) ** (252 / len(df)) - 1
    sharpe_ratio = (df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()) * np.sqrt(252)
    
    # Max Drawdown
    cumulative_returns = df['Cumulative_Strategy_Returns']
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns / peak) - 1
    max_drawdown = drawdown.min()

    # Enhanced trade statistics
    active_trade_days = df[df['Position'].shift(1) != 0]
    winning_days = active_trade_days[active_trade_days['Strategy_Returns'] > 0]
    total_active_days = len(active_trade_days)
    win_rate = len(winning_days) / total_active_days if total_active_days > 0 else 0
    
    # Count stop loss and take profit exits
    stop_loss_exits = len(df[df['Exit_Reason'] == 'Stop Loss'])
    take_profit_exits = len(df[df['Exit_Reason'] == 'Take Profit']) if take_profit_pct else 0
    
    # Average trade duration
    position_changes = df[df['Position'] != df['Position'].shift(1)]
    trade_durations = []
    entry_idx = None
    for i, row in position_changes.iterrows():
        if row['Position'] != 0:  # Entry
            entry_idx = i
        elif entry_idx is not None:  # Exit
            trade_durations.append(i - entry_idx)
            entry_idx = None
    avg_trade_duration = np.mean(trade_durations) if trade_durations else 0

    # Benchmark Performance
    benchmark_annualized_return = (df['Cumulative_Market_Returns'].iloc[-1]) ** (252 / len(df)) - 1
    benchmark_sharpe_ratio = (df['Market_Returns'].mean() / df['Market_Returns'].std()) * np.sqrt(252)
    benchmark_cumulative_returns = df['Cumulative_Market_Returns']
    benchmark_peak = benchmark_cumulative_returns.expanding(min_periods=1).max()
    benchmark_drawdown = (benchmark_cumulative_returns / benchmark_peak) - 1
    benchmark_max_drawdown = benchmark_drawdown.min()
    benchmark_winning_days = df[df['Market_Returns'] > 0]
    benchmark_total_days = len(df['Market_Returns'].dropna())
    benchmark_win_rate = len(benchmark_winning_days) / benchmark_total_days if benchmark_total_days > 0 else 0

    # Output results
    print(f"--- Enhanced Backtesting Results for: {strategy.replace('_', ' ').title()} ---")
    print(f"Stop Loss: {stop_loss_pct:.1%}")
    if take_profit_pct:
        print(f"Take Profit: {take_profit_pct:.1%}")
    print(f"Annualized Return: {annualized_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Win Rate: {win_rate:.2%}")
    print(f"Total Active Trading Days: {total_active_days}")
    print(f"Stop Loss Exits: {stop_loss_exits}")
    if take_profit_pct:
        print(f"Take Profit Exits: {take_profit_exits}")
    print(f"Average Trade Duration: {avg_trade_duration:.1f} days")
    print("\n")

    print(f"--- Benchmark Results ({symbol}) ---")
    print(f"Annualized Return: {benchmark_annualized_return:.2%}")
    print(f"Sharpe Ratio: {benchmark_sharpe_ratio:.2f}")
    print(f"Max Drawdown: {benchmark_max_drawdown:.2%}")
    print(f"Win Rate: {benchmark_win_rate:.2%}")
    print("\n")

    # Enhanced Plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))
    
    # PnL Curve
    ax1.plot(df.index, df['Cumulative_Strategy_Returns'], label='Strategy', linewidth=2)
    ax1.plot(df.index, df['Cumulative_Market_Returns'], label=f'Benchmark ({symbol})', linewidth=2)
    ax1.set_title(f'PnL Curve - {strategy.replace("_", " ").title()} (Stop Loss: {stop_loss_pct:.1%})')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Position over time
    ax2.plot(df.index, df['Position'], label='Position', linewidth=1, alpha=0.7)
    ax2.fill_between(df.index, 0, df['Position'], alpha=0.3)
    ax2.set_title('Position Over Time')
    ax2.set_ylabel('Position')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Price with stop loss levels
    ax3.plot(df.index, df['Close_STOCK'], label=f'{symbol} Price', linewidth=2)
    stop_loss_data = df.dropna(subset=['Stop_Loss_Price'])
    if not stop_loss_data.empty:
        ax3.scatter(stop_loss_data.index, stop_loss_data['Stop_Loss_Price'], 
                   c='red', s=10, alpha=0.5, label='Stop Loss Levels')
    if take_profit_pct:
        take_profit_data = df.dropna(subset=['Take_Profit_Price'])
        if not take_profit_data.empty:
            ax3.scatter(take_profit_data.index, take_profit_data['Take_Profit_Price'], 
                       c='green', s=10, alpha=0.5, label='Take Profit Levels')
    ax3.set_title(f'{symbol} Price with Stop Loss/Take Profit Levels')
    ax3.set_ylabel('Price')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return df

def compare_all_strategies(symbol, start_date, end_date, model_path, f_scaler_path, t_scaler_path):
    """
    Compare all trading strategies with different stop loss levels.
    """
    strategies = ['long_short', 'long_only', 'short_only']
    stop_loss_levels = [0.03, 0.05, 0.07]
    
    results = []
    all_dfs = {}
    
    print("=" * 80)
    print("COMPREHENSIVE STRATEGY COMPARISON")
    print("=" * 80)
    
    for strategy in strategies:
        print(f"\n{'='*20} {strategy.replace('_', ' ').upper()} STRATEGY {'='*20}")
        
        for stop_loss in stop_loss_levels:
            print(f"\n--- Stop Loss: {stop_loss:.1%} ---")
            
            # Run backtest (suppress individual plots for now)
            plt.ioff()  # Turn off interactive plotting
            df = backtest(symbol, start_date, end_date, model_path, f_scaler_path, t_scaler_path, 
                         strategy=strategy, stop_loss_pct=stop_loss)
            plt.close('all')  # Close all figures
            
            # Calculate metrics
            annualized_return = (df['Cumulative_Strategy_Returns'].iloc[-1]) ** (252 / len(df)) - 1
            sharpe_ratio = (df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()) * np.sqrt(252)
            
            cumulative_returns = df['Cumulative_Strategy_Returns']
            peak = cumulative_returns.expanding(min_periods=1).max()
            drawdown = (cumulative_returns / peak) - 1
            max_drawdown = drawdown.min()
            
            active_trade_days = df[df['Position'].shift(1) != 0]
            winning_days = active_trade_days[active_trade_days['Strategy_Returns'] > 0]
            total_active_days = len(active_trade_days)
            win_rate = len(winning_days) / total_active_days if total_active_days > 0 else 0
            
            stop_loss_exits = len(df[df['Exit_Reason'] == 'Stop Loss'])
            
            # Store results
            results.append({
                'Strategy': strategy.replace('_', ' ').title(),
                'Stop Loss': f"{stop_loss:.1%}",
                'Annual Return': f"{annualized_return:.2%}",
                'Sharpe Ratio': f"{sharpe_ratio:.2f}",
                'Max Drawdown': f"{max_drawdown:.2%}",
                'Win Rate': f"{win_rate:.2%}",
                'Active Days': total_active_days,
                'Stop Loss Exits': stop_loss_exits,
                'Final Value': f"{df['Cumulative_Strategy_Returns'].iloc[-1]:.3f}"
            })
            
            # Store dataframe for plotting
            key = f"{strategy}_{stop_loss:.0%}"
            all_dfs[key] = df
            
            print(f"Annual Return: {annualized_return:.2%}")
            print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
            print(f"Max Drawdown: {max_drawdown:.2%}")
            print(f"Win Rate: {win_rate:.2%}")
            print(f"Final Portfolio Value: {df['Cumulative_Strategy_Returns'].iloc[-1]:.3f}")
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    print("\n" + "=" * 80)
    print("SUMMARY TABLE - ALL STRATEGIES")
    print("=" * 80)
    print(results_df.to_string(index=False))
    
    # Benchmark comparison
    benchmark_df = list(all_dfs.values())[0]  # Use first df for benchmark data
    benchmark_return = (benchmark_df['Cumulative_Market_Returns'].iloc[-1]) ** (252 / len(benchmark_df)) - 1
    benchmark_sharpe = (benchmark_df['Market_Returns'].mean() / benchmark_df['Market_Returns'].std()) * np.sqrt(252)
    
    benchmark_cumulative = benchmark_df['Cumulative_Market_Returns']
    benchmark_peak = benchmark_cumulative.expanding(min_periods=1).max()
    benchmark_drawdown = (benchmark_cumulative / benchmark_peak) - 1
    benchmark_max_dd = benchmark_drawdown.min()
    
    print(f"\n--- BENCHMARK ({symbol}) ---")
    print(f"Annual Return: {benchmark_return:.2%}")
    print(f"Sharpe Ratio: {benchmark_sharpe:.2f}")
    print(f"Max Drawdown: {benchmark_max_dd:.2%}")
    
    # Turn plotting back on
    plt.ion()
    
    # Create comprehensive comparison plots
    fig = plt.figure(figsize=(20, 15))
    
    # Plot 1: PnL curves for all strategies with 5% stop loss
    ax1 = plt.subplot(2, 3, 1)
    colors = ['blue', 'green', 'red']
    for i, strategy in enumerate(strategies):
        key = f"{strategy}_5%"
        if key in all_dfs:
            df = all_dfs[key]
            ax1.plot(df.index, df['Cumulative_Strategy_Returns'], 
                    label=f"{strategy.replace('_', ' ').title()}", 
                    color=colors[i], linewidth=2)
    
    # Add benchmark
    ax1.plot(benchmark_df.index, benchmark_df['Cumulative_Market_Returns'], 
             label=f'Benchmark ({symbol})', color='black', linewidth=2, linestyle='--')
    ax1.set_title('Strategy Comparison - 5% Stop Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylabel('Cumulative Returns')
    
    # Plot 2: Long-Short strategy with different stop loss levels
    ax2 = plt.subplot(2, 3, 2)
    stop_colors = ['lightblue', 'blue', 'darkblue']
    for i, stop_loss in enumerate(stop_loss_levels):
        key = f"long_short_{stop_loss:.0%}"
        if key in all_dfs:
            df = all_dfs[key]
            ax2.plot(df.index, df['Cumulative_Strategy_Returns'], 
                    label=f"Stop Loss {stop_loss:.1%}", 
                    color=stop_colors[i], linewidth=2)
    ax2.plot(benchmark_df.index, benchmark_df['Cumulative_Market_Returns'], 
             label=f'Benchmark ({symbol})', color='black', linewidth=2, linestyle='--')
    ax2.set_title('Long-Short Strategy - Different Stop Loss Levels')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylabel('Cumulative Returns')
    
    # Plot 3: Long-Only strategy with different stop loss levels
    ax3 = plt.subplot(2, 3, 3)
    for i, stop_loss in enumerate(stop_loss_levels):
        key = f"long_only_{stop_loss:.0%}"
        if key in all_dfs:
            df = all_dfs[key]
            ax3.plot(df.index, df['Cumulative_Strategy_Returns'], 
                    label=f"Stop Loss {stop_loss:.1%}", 
                    color=stop_colors[i], linewidth=2)
    ax3.plot(benchmark_df.index, benchmark_df['Cumulative_Market_Returns'], 
             label=f'Benchmark ({symbol})', color='black', linewidth=2, linestyle='--')
    ax3.set_title('Long-Only Strategy - Different Stop Loss Levels')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylabel('Cumulative Returns')
    
    # Plot 4: Short-Only strategy with different stop loss levels
    ax4 = plt.subplot(2, 3, 4)
    for i, stop_loss in enumerate(stop_loss_levels):
        key = f"short_only_{stop_loss:.0%}"
        if key in all_dfs:
            df = all_dfs[key]
            ax4.plot(df.index, df['Cumulative_Strategy_Returns'], 
                    label=f"Stop Loss {stop_loss:.1%}", 
                    color=stop_colors[i], linewidth=2)
    ax4.plot(benchmark_df.index, benchmark_df['Cumulative_Market_Returns'], 
             label=f'Benchmark ({symbol})', color='black', linewidth=2, linestyle='--')
    ax4.set_title('Short-Only Strategy - Different Stop Loss Levels')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylabel('Cumulative Returns')
    
    # Plot 5: Risk-Return Scatter Plot
    ax5 = plt.subplot(2, 3, 5)
    returns = []
    risks = []
    labels = []
    colors_scatter = []
    
    color_map = {'Long Short': 'blue', 'Long Only': 'green', 'Short Only': 'red'}
    
    for result in results:
        annual_ret = float(result['Annual Return'].strip('%')) / 100
        max_dd = abs(float(result['Max Drawdown'].strip('%')) / 100)
        returns.append(annual_ret)
        risks.append(max_dd)
        labels.append(f"{result['Strategy']} ({result['Stop Loss']})")
        colors_scatter.append(color_map.get(result['Strategy'], 'gray'))
    
    scatter = ax5.scatter(risks, returns, c=colors_scatter, s=100, alpha=0.7)
    
    # Add benchmark point
    benchmark_risk = abs(benchmark_max_dd)
    ax5.scatter(benchmark_risk, benchmark_return, c='black', s=150, marker='*', 
               label=f'Benchmark ({symbol})')
    
    ax5.set_xlabel('Max Drawdown')
    ax5.set_ylabel('Annual Return')
    ax5.set_title('Risk-Return Profile')
    ax5.grid(True, alpha=0.3)
    
    # Add text labels for points
    for i, label in enumerate(labels):
        ax5.annotate(label, (risks[i], returns[i]), xytext=(5, 5), 
                    textcoords='offset points', fontsize=8)
    
    # Plot 6: Win Rate Comparison
    ax6 = plt.subplot(2, 3, 6)
    strategies_list = []
    win_rates = []
    stop_losses = []
    
    for result in results:
        strategies_list.append(result['Strategy'])
        win_rates.append(float(result['Win Rate'].strip('%')))
        stop_losses.append(result['Stop Loss'])
    
    # Create grouped bar chart
    strategy_types = ['Long Short', 'Long Only', 'Short Only']
    stop_loss_types = ['3%', '5%', '7%']
    
    x = np.arange(len(strategy_types))
    width = 0.25
    
    for i, stop_loss in enumerate(stop_loss_types):
        win_rates_for_stop_loss = []
        for strategy_type in strategy_types:
            for j, result in enumerate(results):
                if result['Strategy'] == strategy_type and result['Stop Loss'] == stop_loss:
                    win_rates_for_stop_loss.append(float(result['Win Rate'].strip('%')))
                    break
        
        ax6.bar(x + i*width, win_rates_for_stop_loss, width, 
               label=f'Stop Loss {stop_loss}', alpha=0.8)
    
    ax6.set_xlabel('Strategy Type')
    ax6.set_ylabel('Win Rate (%)')
    ax6.set_title('Win Rate by Strategy and Stop Loss')
    ax6.set_xticks(x + width)
    ax6.set_xticklabels(strategy_types)
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return results_df, all_dfs

if __name__ == '__main__':
    # Define parameters
    SYMBOL = 'TSLA'
    START_DATE = '2023-05-30'
    END_DATE = '2024-05-30'
    MODEL_PATH = '/content/drive/MyDrive/GDSC-ai-stock/LSTM/lstm_tsla_model.keras'
    F_SCALER_PATH = '/content/drive/MyDrive/GDSC-ai-stock/LSTM/lstm_tsla_scaler_features.pkl'
    T_SCALER_PATH = '/content/drive/MyDrive/GDSC-ai-stock/LSTM/lstm_tsla_scaler_target.pkl'

    # Run comprehensive comparison
    results_df, strategy_dfs = compare_all_strategies(
        SYMBOL, START_DATE, END_DATE, MODEL_PATH, F_SCALER_PATH, T_SCALER_PATH
    )
    
    # Save results to CSV for further analysis
    results_df.to_csv('strategy_comparison_results.csv', index=False)
    print(f"\nResults saved to 'strategy_comparison_results.csv'")
    
    # Find best performing strategy
    results_df['Annual_Return_Numeric'] = results_df['Annual Return'].str.rstrip('%').astype(float)
    best_strategy = results_df.loc[results_df['Annual_Return_Numeric'].idxmax()]
    
    print(f"\n{'='*50}")
    print("BEST PERFORMING STRATEGY:")
    print(f"{'='*50}")
    print(f"Strategy: {best_strategy['Strategy']}")
    print(f"Stop Loss: {best_strategy['Stop Loss']}")
    print(f"Annual Return: {best_strategy['Annual Return']}")
    print(f"Sharpe Ratio: {best_strategy['Sharpe Ratio']}")
    print(f"Max Drawdown: {best_strategy['Max Drawdown']}")
    print(f"Win Rate: {best_strategy['Win Rate']}")
    print(f"Final Portfolio Value: {best_strategy['Final Value']}")
    
    # Additional analysis - most consistent strategy (best risk-adjusted)
    results_df['Sharpe_Numeric'] = results_df['Sharpe Ratio'].astype(float)
    best_risk_adjusted = results_df.loc[results_df['Sharpe_Numeric'].idxmax()]
    
    print(f"\n{'='*50}")
    print("BEST RISK-ADJUSTED STRATEGY (Highest Sharpe):")
    print(f"{'='*50}")
    print(f"Strategy: {best_risk_adjusted['Strategy']}")
    print(f"Stop Loss: {best_risk_adjusted['Stop Loss']}")
    print(f"Annual Return: {best_risk_adjusted['Annual Return']}")
    print(f"Sharpe Ratio: {best_risk_adjusted['Sharpe Ratio']}")
    print(f"Max Drawdown: {best_risk_adjusted['Max Drawdown']}")
    print(f"Win Rate: {best_risk_adjusted['Win Rate']}")