import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Stock Market Trend Analysis")

# Read CSV correctly
df = pd.read_csv("dataset/stock_data.csv", skiprows=2)

# Rename columns
df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

# Convert Close column to numeric
df['Close'] = pd.to_numeric(df['Close'])

# Show data
st.write(df.head())

# Create graph
fig, ax = plt.subplots(figsize=(10,5))

ax.plot(df['Close'])

ax.set_title("Apple Stock Closing Price Trend")
ax.set_xlabel("Days")
ax.set_ylabel("Closing Price")

# Show graph in website
st.pyplot(fig)