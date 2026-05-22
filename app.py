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
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None,
    }
)

# Enhanced Custom CSS for better styling
st.markdown("""
    <style>
        /* Hide Streamlit menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Main color scheme */
        :root {
            --primary-color: #1f77b4;
            --secondary-color: #ff7f0e;
            --success-color: #2ca02c;
            --danger-color: #d62728;
            --info-color: #9467bd;
        }
        
        /* Body styling */
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Header styling */
        h1, h2, h3 {
            color: #1a1a2e;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        /* Metric cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 119, 180, 0.2);
            color: white;
            border-left: 5px solid #ff7f0e;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 119, 180, 0.3);
        }
        
        /* Tabs styling */
        [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0 !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            background-color: #f0f0f0 !important;
            color: #666 !important;
            border: 1px solid #ddd !important;
            transition: all 0.3s ease !important;
        }
        
        [aria-selected="true"] [data-baseweb="tab"] {
            background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%) !important;
            color: white !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(31, 119, 180, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(31, 119, 180, 0.4);
        }
        
        /* Input field styling */
        [data-baseweb="input"] {
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
            padding: 12px !important;
            transition: border-color 0.3s ease !important;
        }
        
        [data-baseweb="input"]:focus {
            border-color: #1f77b4 !important;
            box-shadow: 0 0 8px rgba(31, 119, 180, 0.2) !important;
        }
        
        /* Selectbox styling */
        [data-baseweb="select"] {
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
        }
        
        /* Subheader styling */
        .stSubheader {
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        /* Dataframe styling */
        [data-testid="stDataframe"] {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Card containers */
        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border-top: 4px solid #1f77b4;
        }
        
        /* Success/Error messages */
        .stSuccess, .stError, .stWarning {
            border-radius: 8px;
            border-left: 5px solid;
            padding: 15px;
            font-weight: 500;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            border-right: 2px solid #dee2e6;
        }
        
        /* Sidebar header */
        .stSidebar .stSelectbox label, 
        .stSidebar .stRadio label,
        .stSidebar .stCheckbox label {
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 10px;
        }
        
        /* Fix calendar popup visibility */
        [role="dialog"] {
            z-index: 9999 !important;
            position: fixed !important;
        }
        
        [data-testid="stSidebar"] {
            overflow: visible !important;
        }
        
        .stDateInput {
            z-index: 1000 !important;
        }
        
        [data-baseweb="popover"] {
            z-index: 9999 !important;
        }
        
        /* Metrics styling */
        [data-testid="metric-container"] {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #1f77b4;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        /* Caption styling */
        .stCaption {
            color: #666;
            font-size: 14px;
        }
        
        /* Custom title style */
        .title-style {
            background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5em;
            font-weight: 800;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Header with styling
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 style="background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5em;">📈 Stock Market Trend Analysis</h1>', unsafe_allow_html=True)
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
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                df = df.reset_index()
                df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        else:
            # For other stocks, download from yfinance
            df = yf.download(ticker, period="2y", progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
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
st.sidebar.subheader("📉 Chart Types")
chart_type = st.sidebar.radio(
    "Select visualization",
    ["Closing Price", "High-Low Range", "Open-Close Comparison", "Volume Trend", 
     "Area Chart", "Bar Chart", "OHLC (Candlestick)", "Price Distribution Pie"],
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

# ============ MAIN CONTENT - KEY METRICS ============
st.subheader("📊 Key Statistics")
metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

with metric_col1:
    current_price = filtered_df['Close'].iloc[-1]
    price_change = current_price - filtered_df['Close'].iloc[0]
    st.metric(
        label="Current Price",
        value=f"${current_price:.2f}",
        delta=f"${price_change:.2f}"
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

with metric_col5:
    pct_change = (price_change / filtered_df['Close'].iloc[0]) * 100
    st.metric(
        label="Change %",
        value=f"{pct_change:.2f}%",
        delta=f"{abs(pct_change):.2f}%"
    )

st.markdown("---")

# Charts Section with Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Charts", "📋 Data Table", "📊 Analytics", "📉 Technical"])

with tab1:
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Price Visualization")
        
        # Create figure based on chart type
        fig, ax = plt.subplots(figsize=(14, 6))
        
        if chart_type == "Closing Price":
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=2.5, 
                   label='Closing Price', color='#1f77b4', marker='o', markersize=4)
            
            if show_moving_avg:
                filtered_df['MA20'] = filtered_df['Close'].rolling(window=20).mean()
                ax.plot(filtered_df['Date'], filtered_df['MA20'], linewidth=2, 
                       label='20-Day MA', color='#ff7f0e', linestyle='--', alpha=0.8)
            
            if show_50_ma:
                filtered_df['MA50'] = filtered_df['Close'].rolling(window=50).mean()
                ax.plot(filtered_df['Date'], filtered_df['MA50'], linewidth=2, 
                       label='50-Day MA', color='#2ca02c', linestyle='--', alpha=0.8)
            
            ax.fill_between(filtered_df['Date'], filtered_df['Close'], alpha=0.1, color='#1f77b4')
        
        elif chart_type == "High-Low Range":
            ax.fill_between(filtered_df['Date'], filtered_df['Low'], filtered_df['High'], 
                            alpha=0.3, color='#1f77b4', label='High-Low Range')
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=2.5, 
                   color='#d62728', label='Close', marker='o', markersize=3)
            ax.plot(filtered_df['Date'], filtered_df['Open'], linewidth=1.5, 
                   color='#2ca02c', label='Open', linestyle=':', alpha=0.7)
        
        elif chart_type == "Open-Close Comparison":
            ax.plot(filtered_df['Date'], filtered_df['Open'], linewidth=2, 
                   label='Open', color='#1f77b4', marker='o', markersize=4)
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=2, 
                   label='Close', color='#d62728', marker='s', markersize=4)
            ax.fill_between(filtered_df['Date'], filtered_df['Open'], filtered_df['Close'], 
                           alpha=0.2, color='#9467bd')
        
        elif chart_type == "Volume Trend":
            colors = ['#2ca02c' if filtered_df['Close'].iloc[i] > filtered_df['Open'].iloc[i] 
                     else '#d62728' for i in range(len(filtered_df))]
            ax.bar(filtered_df['Date'], filtered_df['Volume'], color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
            ax.set_ylabel('Volume', fontsize=12, fontweight='bold')
        
        elif chart_type == "Area Chart":
            ax.fill_between(filtered_df['Date'], filtered_df['Close'], alpha=0.5, color='#1f77b4', label='Close')
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=2.5, color='#1f77b4')
            ax.fill_between(filtered_df['Date'], filtered_df['High'], alpha=0.2, color='#ff7f0e', label='High')
        
        elif chart_type == "Bar Chart":
            colors = ['#2ca02c' if filtered_df['Close'].iloc[i] >= filtered_df['Open'].iloc[i] 
                     else '#d62728' for i in range(len(filtered_df))]
            ax.bar(filtered_df['Date'], filtered_df['Close'], color=colors, alpha=0.7, label='Close', edgecolor='black', linewidth=0.5)
            ax.plot(filtered_df['Date'], filtered_df['Close'], linewidth=1.5, color='black', alpha=0.3)
        
        elif chart_type == "OHLC (Candlestick)":
            # Simplified OHLC chart
            width = 0.6
            for idx, row in filtered_df.iterrows():
                date_num = idx
                open_price = row['Open']
                close_price = row['Close']
                high_price = row['High']
                low_price = row['Low']
                
                # Color based on close vs open
                color = '#2ca02c' if close_price >= open_price else '#d62728'
                
                # High-Low line
                ax.plot([date_num, date_num], [low_price, high_price], color=color, linewidth=1)
                
                # Open-Close body
                height = abs(close_price - open_price)
                bottom = min(open_price, close_price)
                ax.bar(date_num, height, width, bottom=bottom, color=color, edgecolor='black', linewidth=0.5)
            
            ax.set_xticks(range(0, len(filtered_df), max(1, len(filtered_df)//10)))
            ax.set_xticklabels([filtered_df['Date'].iloc[i].strftime('%m-%d') 
                                for i in range(0, len(filtered_df), max(1, len(filtered_df)//10))], rotation=45)
        
        elif chart_type == "Price Distribution Pie":
            # Create price ranges for pie chart
            price_ranges = pd.cut(filtered_df['Close'], bins=5)
            price_dist = price_ranges.value_counts().sort_index()
            colors_pie = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            
            wedges, texts, autotexts = ax.pie(price_dist.values, labels=[f'${i.left:.0f}-${i.right:.0f}' 
                                                                           for i in price_dist.index],
                                              autopct='%1.1f%%', colors=colors_pie, startangle=90)
            ax.set_title(f"Price Distribution", fontsize=13, fontweight='bold')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        if chart_type != "Price Distribution Pie":
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Price ($)' if chart_type != "Volume Trend" else 'Volume', 
                         fontsize=12, fontweight='bold')
            ax.set_title(f"{stock_name} - {chart_type}", fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='best', framealpha=0.95, fontsize=10)
            ax.grid(True, alpha=0.3, linestyle='--')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col_chart2:
        st.subheader("💹 Quick Stats")
        
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
        
        st.markdown("**Performance Summary**")
        price_change = filtered_df['Close'].iloc[-1] - filtered_df['Close'].iloc[0]
        pct_change = (price_change / filtered_df['Close'].iloc[0]) * 100
        
        if price_change >= 0:
            st.success(f"📈 +${abs(price_change):.2f} ({pct_change:+.2f}%)")
        else:
            st.error(f"📉 -${abs(price_change):.2f} ({pct_change:.2f}%)")

with tab2:
    st.subheader("📋 Stock Data Table")
    
    # Search/Filter in table
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_term = st.text_input("🔍 Search in data", key="search_table", placeholder="Enter date or price...")
    
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
        }).background_gradient(cmap='RdYlGn', subset=['Close']),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"stock_data_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

with tab3:
    st.subheader("📊 Advanced Analytics")
    
    col_ana1, col_ana2 = st.columns(2)
    
    with col_ana1:
        st.markdown("**Price Distribution**")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(filtered_df['Close'], bins=40, color='#1f77b4', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Price ($)', fontweight='bold', fontsize=11)
        ax.set_ylabel('Frequency', fontweight='bold', fontsize=11)
        ax.set_title('Distribution of Closing Prices', fontweight='bold', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        st.pyplot(fig)
    
    with col_ana2:
        st.markdown("**Daily Returns**")
        filtered_df['Daily_Return'] = filtered_df['Close'].pct_change() * 100
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#2ca02c' if x >= 0 else '#d62728' for x in filtered_df['Daily_Return'].dropna()]
        ax.bar(range(len(filtered_df['Daily_Return'].dropna())), 
              filtered_df['Daily_Return'].dropna(), color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.set_xlabel('Days', fontweight='bold', fontsize=11)
        ax.set_ylabel('Return (%)', fontweight='bold', fontsize=11)
        ax.set_title('Daily Returns Trend', fontweight='bold', fontsize=12)
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
        st.metric("Avg Daily Return", f"{daily_avg_return:.2f}%")
    with ana_col3:
        max_daily_gain = filtered_df['Daily_Return'].max()
        st.metric("Max Daily Gain", f"{max_daily_gain:.2f}%")

with tab4:
    st.subheader("📉 Technical Indicators")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("**RSI (Relative Strength Index)**")
        
        # Calculate RSI
        delta = filtered_df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        filtered_df['RSI'] = 100 - (100 / (1 + rs))
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(filtered_df['Date'], filtered_df['RSI'], linewidth=2, color='#1f77b4', label='RSI')
        ax.axhline(y=70, color='#d62728', linestyle='--', label='Overbought (70)', alpha=0.7)
        ax.axhline(y=30, color='#2ca02c', linestyle='--', label='Oversold (30)', alpha=0.7)
        ax.fill_between(filtered_df['Date'], 30, 70, alpha=0.1, color='gray')
        ax.set_ylabel('RSI', fontweight='bold')
        ax.set_title('RSI (14-period)', fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    with tech_col2:
        st.markdown("**MACD (Moving Average Convergence Divergence)**")
        
        # Calculate MACD
        ema12 = filtered_df['Close'].ewm(span=12).mean()
        ema26 = filtered_df['Close'].ewm(span=26).mean()
        filtered_df['MACD'] = ema12 - ema26
        filtered_df['Signal'] = filtered_df['MACD'].ewm(span=9).mean()
        filtered_df['Histogram'] = filtered_df['MACD'] - filtered_df['Signal']
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(filtered_df['Date'], filtered_df['MACD'], label='MACD', color='#1f77b4', linewidth=2)
        ax.plot(filtered_df['Date'], filtered_df['Signal'], label='Signal', color='#ff7f0e', linewidth=2)
        colors = ['#2ca02c' if x > 0 else '#d62728' for x in filtered_df['Histogram']]
        ax.bar(filtered_df['Date'], filtered_df['Histogram'], label='Histogram', color=colors, alpha=0.3)
        ax.set_ylabel('MACD', fontweight='bold')
        ax.set_title('MACD', fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

st.markdown("---")
st.caption("💡 Tip: Explore different chart types and technical indicators. Use the sidebar to customize your analysis with moving averages and various stock selections.")