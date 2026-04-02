import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")
st.title("🛒 Retail Analytics Dashboard")
st.caption("Self-serve insights platform · Built with Streamlit + DuckDB")

@st.cache_data
def load_data():
    return pd.read_csv("data/sample_data.csv", parse_dates=["date"])

@st.cache_data
def run_query(sql, df):
    con = duckdb.connect()
    con.register("sales", df)
    return con.execute(sql).df()

def load_sql(filename):
    return Path(f"sql/{filename}").read_text()

df = load_data()

# ── Sidebar filters ──────────────────────────────────────────────
st.sidebar.header("Filters")
brands = st.sidebar.multiselect("Brand", df["brand"].unique(), default=list(df["brand"].unique()))
regions = st.sidebar.multiselect("Region", df["region"].unique(), default=list(df["region"].unique()))
date_range = st.sidebar.date_input("Date range", [df["date"].min(), df["date"].max()])

filtered = df[
    df["brand"].isin(brands) &
    df["region"].isin(regions) &
    (df["date"] >= pd.Timestamp(date_range[0])) &
    (df["date"] <= pd.Timestamp(date_range[1]))
]

# ── KPI Cards ────────────────────────────────────────────────────
st.subheader("Overview")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${filtered['revenue'].sum():,.0f}")
k2.metric("Total Units Sold", f"{filtered['units_sold'].sum():,}")
k3.metric("Active Stores", filtered["store_id"].nunique())
k4.metric("Avg Data Freshness", f"{filtered['data_freshness_lag_days'].mean():.1f} days")

st.divider()

# ── Charts ───────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Brand")
    brand_data = run_query(load_sql("sales_by_brand.sql"), filtered)
    fig = px.bar(brand_data, x="brand", y="total_revenue", color="brand",
                 labels={"total_revenue": "Revenue ($)", "brand": "Brand"},
                 color_discrete_sequence=px.colors.qualitative.Teal)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue Trend Over Time")
    trend = filtered.groupby("date")["revenue"].sum().reset_index()
    fig2 = px.line(trend, x="date", y="revenue",
                   labels={"revenue": "Daily Revenue ($)", "date": "Date"})
    fig2.update_traces(line_color="#1D9E75")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Store Performance")
store_data = run_query(load_sql("store_performance.sql"), filtered)
fig3 = px.scatter(store_data, x="transactions", y="total_revenue",
                  color="region", size="total_units", hover_name="store_id",
                  labels={"total_revenue": "Revenue ($)", "transactions": "Transactions"},
                  color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Data Freshness Monitor")
freshness = run_query(load_sql("data_freshness.sql"), filtered)
color_map = {"Fresh": "#1D9E75", "Stale": "#EF9F27", "Critical": "#E24B4A"}
fig4 = px.bar(freshness.head(20), x="store_id", y="avg_lag_days",
              color="freshness_status", color_discrete_map=color_map,
              labels={"avg_lag_days": "Avg Lag (days)", "store_id": "Store"})
st.plotly_chart(fig4, use_container_width=True)

with st.expander("View raw data"):
    st.dataframe(filtered.sort_values("date", ascending=False).head(200))
