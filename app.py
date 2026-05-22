import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

# Page Configuration
st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .header-text {
            color: #1f77b4;
            font-weight: bold;
        }
        /* Fix calendar popup visibility */
        [role="dialog"] {
            z-index: 9999 !important;
            position: fixed !important;
        }
        /* Ensure sidebar doesn't clip calendar */
        [data-testid="stSidebar"] {
            overflow: visible !important;
        }
        /* Calendar and date picker fixes */
        .stDateInput {
            z-index: 1000 !important;
        }
        [data-baseweb="input"] {
            z-index: 1000 !important;
        }
        /* Popover positioning */
        [data-baseweb="popover"] {
            z-index: 9999 !important;
        }
        /* Modal and dialog fixes */
        div[class*="baseweb"] {
            z-index: inherit;
        }
        [class*="calendar"] {
            z-index: 9999 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📈 Stock Market Trend Analysis")
with col2:
    st.caption("Real-time Analysis Dashboard")

st.markdown("---")

# ============ SIDEBAR - CONTROLS ============
st.sidebar.header("🎛️ Dashboard Controls")

# Stock Selection with ticker mapping
stock_options = {
    "Apple (AAPL)": "AAPL",
    "Google (GOOGL)": "GOOGL",
    "Microsoft (MSFT)": "MSFT"
}

stock_name = st.sidebar.selectbox(
    "📊 Select Stock",
    list(stock_options.keys()),
    help="Choose a stock to analyze"
)

stock_ticker = stock_options[stock_name]

# Load data based on stock selection
@st.cache_data
def load_stock_data(ticker):
    try:
        # Try to load from CSV if it's AAPL
        if ticker == "AAPL":
            try:
                df = pd.read_csv("dataset/stock_data.csv", skiprows=2)
                df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
                df['Date'] = pd.to_datetime(df['Date'])
            except:
                # Fallback to yfinance
                df = yf.download(ticker, period="2y", progress=False)
                df = df.reset_index()
                df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        else:
            # For other stocks, download from yfinance
            df = yf.download(ticker, period="2y", progress=False)
            
            if df.empty:
                st.error(f"No data available for {ticker}")
                return None
            
            # Reset index to make Date a column
            df = df.reset_index()
            
            # Ensure Date is a datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            
            # Select only the columns we need
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        
        # Ensure Date column is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Convert price columns to numeric, handling any errors
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
        df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        
        # Drop rows with NaN values
        df = df.dropna()
        
        # Sort by date
        df = df.sort_values('Date').reset_index(drop=True)
        
        if len(df) == 0:
            st.error(f"No valid data available for {ticker}")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error loading data for {ticker}: {str(e)}")
        return None

# Load the selected stock data
df = load_stock_data(stock_ticker)

if df is None or len(df) == 0:
    st.stop()

# ============ MAIN CONTENT - DATE RANGE FILTER ============
st.subheader("📅 Select Date Range")
date_col1, date_col2, date_col3 = st.columns([2, 2, 2])

with date_col1:
    start_date = st.date_input(
        "From Date",
        value=df['Date'].min().date(),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date(),
        key="start_date_main"
    )

with date_col2:
    end_date = st.date_input(
        "To Date",
        value=df['Date'].max().date(),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date(),
        key="end_date_main"
    )

st.markdown("---")

# Chart Type Selection (keep in sidebar)
st.sidebar.subheader("📉 Chart Type")
chart_type = st.sidebar.radio(
    "Select chart type",
    ["Closing Price", "High-Low Range", "Open-Close Comparison", "Volume Trend"],
    help="Select the type of chart to display"
)

# Moving Average (keep in sidebar)
st.sidebar.subheader("📈 Moving Averages")
show_moving_avg = st.sidebar.checkbox("Show 20-Day Moving Average", value=True)
show_50_ma = st.sidebar.checkbox("Show 50-Day Moving Average", value=False)

# Data Filtering
filtered_df = df[(df['Date'] >= pd.Timestamp(start_date)) & 
                  (df['Date'] <= pd.Timestamp(end_date))].copy()

if len(filtered_df) == 0:
    st.error("⚠️ No data available for the selected date range. Please adjust your selection.")
    st.stop()

# ============ MAIN CONTENT ============

# Key Metrics Section
st.subheader("📊 Key Statistics")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    current_price = filtered_df['Close'].iloc[-1]
    st.metric(
        label="Current Price",
        value=f"${current_price:.2f}",
        delta=f"${current_price - filtered_df['Close'].iloc[0]:.2f}"
    )

with metric_col2:
    highest = filtered_df['High'].max()
    st.metric(
        label="Highest Price",
        value=f"${highest:.2f}"
    )

with metric_col3:
    lowest = filtered_df['Low'].min()
    st.metric(
        label="Lowest Price",
        value=f"${lowest:.2f}"
    )

with metric_col4:
    avg_volume = filtered_df['Volume'].mean() / 1_000_000
    st.metric(
        label="Avg Volume (M)",
        value=f"{avg_volume:.2f}M"
    )

st.markdown("---")

# Charts Section with Tabs
tab1, tab2, tab3 = st.tabs(["📈 Charts", "📋 Data Table", "📊 Analytics"])

with tab1:
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Price Trend Analysis")
        
        # Create figure based on chart type
        fig, ax = plt.subplots(figsize=(12, 5))
        
        if chart_type == "Closing Price":
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=2.5, 
                   label='Closing Price', color='#1f77b4')
            
            if show_moving_avg:
                filtered_df['MA20'] = filtered_df['Close'].rolling(window=20).mean()
                ax.plot(filtered_df['Date'], filtered_df['MA20'], linewidth=2, 
                       label='20-Day MA', color='#ff7f0e', linestyle='--', alpha=0.8)
            
            if show_50_ma:
                filtered_df['MA50'] = filtered_df['Close'].rolling(window=50).mean()
                ax.plot(filtered_df['Date'], filtered_df['MA50'], linewidth=2, 
                       label='50-Day MA', color='#2ca02c', linestyle='--', alpha=0.8)
        
        elif chart_type == "High-Low Range":
            ax.fill_between(filtered_df['Date'], filtered_df['Low'], filtered_df['High'], 
                            alpha=0.3, color='#1f77b4', label='High-Low Range')
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=2, 
                   color='#d62728', label='Close')
        
        elif chart_type == "Open-Close Comparison":
            ax.plot(filtered_df['Date'], filtered_df['Open'], linewidth=2, 
                   label='Open', color='#1f77b4', marker='o', markersize=3)
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=2, 
                   label='Close', color='#d62728', marker='s', markersize=3)
            ax.fill_between(filtered_df['Date'], filtered_df['Open'], filtered_df['Close'], 
                           alpha=0.2, color='#9467bd')
        
        elif chart_type == "Volume Trend":
            colors = ['#2ca02c' if filtered_df['Close'].iloc[i] > filtered_df['Open'].iloc[i] 
                     else '#d62728' for i in range(len(filtered_df))]
            ax.bar(filtered_df['Date'], filtered_df['Volume'], color=colors, alpha=0.6)
            ax.set_ylabel('Volume', fontsize=11, fontweight='bold')
        
        ax.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax.set_ylabel('Price ($)' if chart_type != "Volume Trend" else 'Volume', 
                     fontsize=11, fontweight='bold')
        ax.set_title(f"{stock_name} - {chart_type}", fontsize=13, fontweight='bold')
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
    
    with col_chart2:
        st.subheader("Price Statistics")
        
        stats_data = {
            "Metric": ["Min", "Max", "Mean", "Median", "Std Dev"],
            "Value": [
                f"${filtered_df['Close'].min():.2f}",
                f"${filtered_df['Close'].max():.2f}",
                f"${filtered_df['Close'].mean():.2f}",
                f"${filtered_df['Close'].median():.2f}",
                f"${filtered_df['Close'].std():.2f}"
            ]
        }
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, hide_index=True, use_container_width=True)
        
        st.markdown("**Performance Metrics**")
        price_change = filtered_df['Close'].iloc[-1] - filtered_df['Close'].iloc[0]
        pct_change = (price_change / filtered_df['Close'].iloc[0]) * 100
        
        if price_change >= 0:
            st.success(f"📈 Total Change: +${abs(price_change):.2f} ({pct_change:.2f}%)")
        else:
            st.error(f"📉 Total Change: -${abs(price_change):.2f} ({pct_change:.2f}%)")

with tab2:
    st.subheader("📋 Stock Data Table")
    
    # Search/Filter in table
    search_col1, search_col2 = st.columns([2, 1])
    with search_col1:
        search_term = st.text_input("🔍 Search in data (Date or Price range)", key="search_table")
    
    display_df = filtered_df.copy()
    
    if search_term:
        display_df = display_df[display_df.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        ]
    
    st.dataframe(
        display_df[['Date', 'Open', 'Close', 'High', 'Low', 'Volume']].style.format({
            'Open': '${:.2f}',
            'Close': '${:.2f}',
            'High': '${:.2f}',
            'Low': '${:.2f}',
            'Volume': '{:,.0f}'
        }),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"stock_data_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

with tab3:
    st.subheader("📊 Advanced Analytics")
    
    col_ana1, col_ana2 = st.columns(2)
    
    with col_ana1:
        st.markdown("**Price Distribution**")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(filtered_df['Close'], bins=30, color='#1f77b4', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Price ($)', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Distribution of Closing Prices')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col_ana2:
        st.markdown("**Daily Returns**")
        filtered_df['Daily_Return'] = filtered_df['Close'].pct_change() * 100
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#2ca02c' if x >= 0 else '#d62728' for x in filtered_df['Daily_Return'].dropna()]
        ax.bar(range(len(filtered_df['Daily_Return'].dropna())), 
              filtered_df['Daily_Return'].dropna(), color=colors, alpha=0.7)
        ax.set_xlabel('Days', fontweight='bold')
        ax.set_ylabel('Return (%)', fontweight='bold')
        ax.set_title('Daily Returns Trend')
        ax.grid(True, alpha=0.3, axis='y')
        st.pyplot(fig)
    
    # Additional Statistics
    st.markdown("---")
    st.markdown("**Volatility Analysis**")
    volatility = filtered_df['Close'].pct_change().std() * 100
    daily_avg_return = filtered_df['Daily_Return'].mean()
    
    ana_col1, ana_col2, ana_col3 = st.columns(3)
    with ana_col1:
        st.metric("Daily Volatility", f"{volatility:.2f}%")
    with ana_col2:
        st.metric("Average Daily Return", f"{daily_avg_return:.2f}%")
    with ana_col3:
        max_daily_gain = filtered_df['Daily_Return'].max()
        st.metric("Max Daily Gain", f"{max_daily_gain:.2f}%", delta=f"${filtered_df['Close'].max():.2f}")

st.markdown("---")
st.caption("💡 Tip: Use the controls on the left to customize your analysis. Update the date range and chart type to explore different perspectives of the data.")