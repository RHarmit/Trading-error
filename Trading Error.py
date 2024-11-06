import pandas as pd
import numpy as np
import yfinance as yf
import time

# Step 1: Data Collection and Error Introduction
def get_data():
    data = yf.download("AAPL", start="2023-01-01", end="2023-12-31")
    trade_data = data[['Close']].copy()
    trade_data['Trade Price'] = trade_data['Close'] * (1 + np.random.normal(0, 0.01, len(trade_data)))
    return trade_data

def introduce_errors(trade_data):
    np.random.seed(42)
    # Introduce random errors
    for i in range(10):
        random_idx = np.random.randint(0, len(trade_data))
        trade_data.iloc[random_idx, trade_data.columns.get_loc('Trade Price')] *= 1 + np.random.normal(0, 0.05)
    # Introduce missing trade prices
    missing_idx = np.random.choice(trade_data.index, size=5, replace=False)
    trade_data.loc[missing_idx, 'Trade Price'] = np.nan
    return trade_data

# Step 2: Error Detection
def detect_errors(trade_data, threshold=0.03):
    trade_data['Price Difference'] = abs(trade_data['Trade Price'] - trade_data['Close'])
    trade_data['Error Flag'] = trade_data['Price Difference'] > (threshold * trade_data['Close'])
    errors = trade_data[trade_data['Error Flag'] | trade_data['Trade Price'].isna()]
    return errors

# Step 3: Real-Time Alerts
def real_time_alerts(trade_data, threshold=0.03):
    for idx, row in trade_data.iterrows():
        if pd.isna(row['Trade Price']) or abs(row['Trade Price'] - row['Close']) > (threshold * row['Close']):
            print(f"Alert: Trade error detected on {idx.date()} - Trade Price: {row['Trade Price']}, Close Price: {row['Close']}")
        time.sleep(0.1)  # Simulate delay for real-time alerts

# Step 4: Error Correction
def correct_errors(trade_data):
    # Fill missing values with the previous day's close price
    trade_data['Trade Price'].fillna(trade_data['Close'].shift(1), inplace=True)
    # Correct flagged errors by setting Trade Price to Close Price
    trade_data.loc[trade_data['Error Flag'], 'Trade Price'] = trade_data['Close']
    return trade_data

# Step 5: Summary Report
def summary_report(initial_errors, corrected_errors):
    accuracy_improvement = ((initial_errors - corrected_errors) / initial_errors) * 100
    print(f"Initial Errors Detected: {initial_errors}")
    print(f"Errors Remaining After Correction: {corrected_errors}")
    print(f"Accuracy Improvement: {accuracy_improvement:.2f}%")

# Main Execution
if __name__ == "__main__":
    # Collect data and introduce errors
    trade_data = get_data()
    trade_data = introduce_errors(trade_data)

    # Detect initial errors
    errors = detect_errors(trade_data)
    initial_errors = len(errors)
    print("Detected Errors:\n", errors)

    # Real-time alerts for errors
    print("\nReal-Time Alerts:")
    real_time_alerts(trade_data)

    # Correct errors
    corrected_data = correct_errors(trade_data)

    # Detect errors after correction
    corrected_errors = len(detect_errors(corrected_data))

    # Summary report
    summary_report(initial_errors, corrected_errors)
