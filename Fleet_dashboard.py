import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Fleet Operations Dashboard", layout="wide")

# --- Load Data (cached for performance) ---
@st.cache_data
def load_fleet_data():
    np.random.seed(42)
    n = 50
    data = pd.DataFrame({
        "Vehicle ID": [f"VH-{i:03d}" for i in range(1, n+1)],
        "Route": np.random.choice(["Route A", "Route B", "Route C", "Route D"], n),
        "Status": np.random.choice(["Active", "Idle", "Maintenance"], n),
        "Risk Level": np.random.choice(["High", "Low", "Medium"], n),
        "Mileage (km)": np.random.randint(5000, 150000, n),
        "Last Service (days ago)": np.random.randint(1, 365, n),
        "Fuel Efficiency (km/L)": np.round(np.random.uniform(6, 15, n), 2),
    })
    return data

data = load_fleet_data()

# --- Sidebar Filters ---
st.sidebar.title("Fleet Operations Dashboard")
st.sidebar.header("Settings")

selected_route = st.sidebar.multiselect(
    "Select Route(s)",
    options=data["Route"].unique(),
    default=data["Route"].unique()
)

selected_risk = st.sidebar.multiselect(
    "Filter by Risk Level",
    options=data["Risk Level"].unique(),
    default=data["Risk Level"].unique()
)

selected_status = st.sidebar.multiselect(
    "Filter by Status",
    options=data["Status"].unique(),
    default=data["Status"].unique()
)

# --- Filter Data ---
filtered_data = data[
    (data["Route"].isin(selected_route)) &
    (data["Risk Level"].isin(selected_risk)) &
    (data["Status"].isin(selected_status))
]

# --- Title ---
st.title("Fleet Operations Dashboard")

# --- KPI Metrics ---
st.subheader("📊 Fleet Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Vehicles", len(filtered_data))
col2.metric("High-Risk Vehicles", len(filtered_data[filtered_data["Risk Level"] == "High"]))
col3.metric("Active Vehicles", len(filtered_data[filtered_data["Status"] == "Active"]))
col4.metric("Avg Fuel Efficiency", f"{filtered_data['Fuel Efficiency (km/L)'].mean():.2f} km/L")

st.markdown("---")

# --- Charts ---
col_left, col_right = st.columns([3, 1])

with col_left:
    st.subheader("Vehicles by Route")
    route_counts = filtered_data["Route"].value_counts()
    st.bar_chart(route_counts)

with col_right:
    st.subheader("Risk Distribution")
    risk_counts = filtered_data["Risk Level"].value_counts()
    st.bar_chart(risk_counts)

st.markdown("---")

# --- Predictive Maintenance Flags ---
st.subheader("🔧 Predictive Maintenance Insights")
high_risk = filtered_data[
    (filtered_data["Risk Level"] == "High") |
    (filtered_data["Last Service (days ago)"] > 180)
]
st.write(f"**{len(high_risk)} vehicle(s)** flagged for maintenance review:")
st.dataframe(high_risk[["Vehicle ID", "Route", "Status", "Risk Level", "Mileage (km)", "Last Service (days ago)"]])

st.markdown("---")

# --- Raw Data ---
with st.expander("View Full Fleet Data"):
    st.dataframe(filtered_data)
