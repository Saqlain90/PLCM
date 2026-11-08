import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="EV Battery Management System",
    page_icon="⚡",
    layout="wide"
)

# Title & Metadata Header
st.title("⚡ Electric Vehicle Battery Health & Thermal Portal")
st.markdown("""
**Student Name:** Vipul R | **USN:** 4VV23ME116  
**System Module:** Advanced Battery Management System (BMS) Telemetry & Analytics
""")
st.divider()

# Sidebar Controls
st.sidebar.header("Vehicle & Pack Filters")
pack_chemistry = st.sidebar.selectbox("Cell Chemistry Type", ["LFP (Lithium Iron Phosphate)", "NMC (Nickel Manganese Cobalt)"])
temp_threshold = st.sidebar.slider("Critical Temp Alert (°C)", min_value=35, max_value=60, value=45)

# Key Performance Indicators
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg State of Health (SoH)", "96.4%", "+0.8%")
col2.metric("Mean Pack Temp", "32.1 °C", "-1.4 °C")
col3.metric("State of Charge (SoC)", "78%", "-12% (discharging)")
col4.metric("Thermal Alerts", "2 Units", "Requires Cooling")

st.divider()

# Sample Fleet Battery Pack Data
pack_data = {
    "Vehicle ID": ["EV-101", "EV-102", "EV-103", "EV-104", "EV-105"],
    "Pack Model": ["72V 100Ah LFP", "96V 150Ah NMC", "72V 100Ah LFP", "96V 200Ah NMC", "72V 100Ah LFP"],
    "SoC (%)": [82, 45, 91, 23, 67],
    "SoH (%)": [98.1, 94.5, 99.0, 91.2, 95.8],
    "Pack Temp (°C)": [31.5, 47.2, 29.8, 48.0, 34.1],
    "Voltage (V)": [73.2, 95.1, 74.0, 94.8, 73.5],
    "Cooling Status": ["Normal", "HIGH FLOW", "Normal", "HIGH FLOW", "Normal"]
}

df_bms = pd.DataFrame(pack_data)

# Tabs Navigation
tab1, tab2, tab3 = st.tabs(["🔋 Fleet Pack Diagnostics", "🔥 Thermal Monitoring", "📝 Log BMS Diagnostic Entry"])

with tab1:
    st.subheader("Real-Time Pack Telemetry")
    st.dataframe(df_bms, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### State of Charge (SoC) Distribution")
        st.bar_chart(df_bms.set_index("Vehicle ID")["SoC (%)"])
    with c2:
        st.markdown("### Battery Health Index (SoH)")
        st.line_chart(df_bms.set_index("Vehicle ID")["SoH (%)"])

with tab2:
    st.subheader("Thermal Safety Analysis")
    overtemp_df = df_bms[df_bms["Pack Temp (°C)"] >= temp_threshold]
    
    if not overtemp_df.empty:
        st.error(f"⚠️ Warning: {len(overtemp_df)} vehicle packs exceeded the critical thermal threshold of {temp_threshold}°C!")
        st.table(overtemp_df[["Vehicle ID", "Pack Model", "Pack Temp (°C)", "Cooling Status"]])
    else:
        st.success(f"✅ All pack temperatures are operating below the set threshold ({temp_threshold}°C).")

with tab3:
    st.subheader("Log Manual BMS Inspection")
    with st.form("bms_form"):
        vid = st.text_input("Vehicle Identification Number", value="EV-106")
        soc = st.slider("Logged SoC (%)", 0, 100, 85)
        temp = st.number_input("Measured Pack Temperature (°C)", min_value=15.0, max_value=80.0, value=33.0)
        cooling = st.selectbox("Cooling Circuit Status", ["Inactive", "Low Flow", "High Flow", "Fault"])
        
        submitted = st.form_submit_button("Record BMS Diagnostic")
        if submitted:
            st.success(f"Diagnostic record updated for vehicle **{vid}**: SoC = {soc}%, Temp = {temp}°C.")
