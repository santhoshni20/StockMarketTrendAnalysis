import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv("dataset/stock_data.csv", skiprows=2)

# Rename columns properly
df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

# Convert Close column to numeric
df['Close'] = pd.to_numeric(df['Close'])

# Print first rows
print(df.head())

# Create graph
plt.figure(figsize=(10,5))

plt.plot(df['Close'])

plt.title("Apple Stock Closing Price Trend")

plt.xlabel("Days")
plt.ylabel("Closing Price")

plt.show()