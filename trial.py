import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# 1. Page setup
# -----------------------------------------------------
st.set_page_config(page_title="Moon Phase Stock Dashboard", layout="wide")
st.title("🌙 Interactive Stock Analysis by Moon Phase")

# -----------------------------------------------------
# 2. Load data
# -----------------------------------------------------
df = pd.read_csv("filtered_stock_data_moon_cycle.csv")
df['Date'] = pd.to_datetime(df['Date'])

# -----------------------------------------------------
# 3. Sidebar filters
# -----------------------------------------------------
st.sidebar.header("🔍 Filter Options")

# Ticker dropdown
tickers = sorted(df['Ticker'].unique())
selected_tickers = st.sidebar.multiselect(
    "Select Ticker(s):",
    options=tickers,
    default=["WU", "ZSL"]
)

# Moon Phase dropdown
phases = sorted(df['Moon_Phase'].unique())
selected_phases = st.sidebar.multiselect(
    "Select Moon Phase(s):",
    options=phases,
    default=phases
)

# -----------------------------------------------------
# 4. Filter data based on user selection
# -----------------------------------------------------
filtered_df = df[df['Ticker'].isin(selected_tickers) & df['Moon_Phase'].isin(selected_phases)]

# -----------------------------------------------------
# 5. Plotly interactive chart
# -----------------------------------------------------
if not filtered_df.empty:
    fig = px.scatter(
        filtered_df,
        x='Date',
        y='Close',
        color='Moon_Phase',
        symbol='Moon_Phase',
        facet_col='Ticker',
        hover_data=['Open', 'High', 'Low', 'Close', 'Volume', 'Ticker', 'Moon_Phase'],
        title="📈 Stock Closing Price vs Moon Phase",
        height=600
    )

    # Add line trend for each ticker
    for ticker in selected_tickers:
        ticker_data = filtered_df[filtered_df['Ticker'] == ticker]
        fig.add_scatter(
            x=ticker_data['Date'],
            y=ticker_data['Close'],
            mode='lines',
            name=f"{ticker} Trend",
            line=dict(width=1.5),
            showlegend=True
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Close Price",
        legend_title="Moon Phase",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ No data available for the selected filters.")

# -----------------------------------------------------
# 6. Data table below chart
# -----------------------------------------------------
with st.expander("📊 Show Filtered Data Table"):
    st.dataframe(filtered_df)
