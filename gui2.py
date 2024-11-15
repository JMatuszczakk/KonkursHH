import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Dane Środowiskowe",
    page_icon="🌍",
    layout="wide"
)

# Polish translations
TRANSLATIONS = {
    'title': "Panel Danych Środowiskowej",
    'env_data': "Dane Środowiskowe",
    'light_data': "Pomiary Światła",
    'air_quality': "Pomiary Jakości Powietrza",
    'voltage_server': "Pomiary Napięcia z Serwera",
    'loading_error': "Błąd wczytywania pliku",
    'file_not_found': "Nie znaleziono pliku",
    'rows': "wierszy",
    'columns': "kolumn",
    'temperature': "Temperatura",
    'pressure': "Ciśnienie",
    'humidity': "Wilgotność",
    'light_level': "Poziom Światła",
    'voltage': "Napięcie",
    'raw_value': "Wartość Surowa",
    'device_id': "ID Urządzenia",
    'time': "Czas",
    'chart_tab': "Wykres",
    'data_tab': "Dane",
    'comparison_tab': "Porównanie",
    'celsius': "°C",
    'fahrenheit': "°F",
    'hpa': "hPa",
    'percent': "%",
    'lux': "lx",
    'volts': "V",
    'all_devices': "Wszystkie Urządzenia",
    'select_device': "Wybierz Urządzenie",
    'voltage_comparison': "Porównanie Napięć",
    'raw_values': "Wartości Surowe"
}

def load_and_prepare_csv(file_path):
    """Load CSV file and prepare data for visualization"""
    try:
        if os.path.exists(file_path):
            # For voltage_readings_server.csv, only load 'Timestamp' and 'voltage' columns
            if 'voltage_readings_server.csv' in file_path:
                df = pd.read_csv(file_path, usecols=['Timestamp', 'voltage'])
                # Ensure columns are lowercase for consistency in server data
                df.columns = df.columns.str.lower()
            else:
                df = pd.read_csv(file_path)

            # Check for timestamp column (both lowercase and uppercase)
            timestamp_col = 'timestamp' if 'timestamp' in df.columns else 'Timestamp'
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])

            return df
        else:
            st.error(f"{TRANSLATIONS['file_not_found']}: {file_path}")
            return None
    except Exception as e:
        st.error(f"{TRANSLATIONS['loading_error']} {file_path}: {str(e)}")
        return None

def create_environmental_charts(df):
    """Create charts for environmental data"""
    if df is not None:
        # Temperature chart
        fig_temp = px.line(df, x='Timestamp', y=['Temperature_C', 'Temperature_F'],
                          title=f"{TRANSLATIONS['temperature']} ({TRANSLATIONS['celsius']}/{TRANSLATIONS['fahrenheit']})")
        fig_temp.update_layout(xaxis_title=TRANSLATIONS['time'])
        st.plotly_chart(fig_temp, use_container_width=True)

        # Pressure chart
        fig_pressure = px.line(df, x='Timestamp', y='Pressure_hPa',
                             title=f"{TRANSLATIONS['pressure']} ({TRANSLATIONS['hpa']})")
        fig_pressure.update_layout(xaxis_title=TRANSLATIONS['time'])
        st.plotly_chart(fig_pressure, use_container_width=True)

        # Humidity chart
        fig_humidity = px.line(df, x='Timestamp', y='Humidity_%',
                             title=f"{TRANSLATIONS['humidity']} ({TRANSLATIONS['percent']})")
        fig_humidity.update_layout(xaxis_title=TRANSLATIONS['time'])
        st.plotly_chart(fig_humidity, use_container_width=True)

def create_light_chart(df):
    """Create chart for light readings"""
    if df is not None:
        fig = px.line(df, x='Timestamp', y='Light_Level_lx',
                     title=f"{TRANSLATIONS['light_level']} ({TRANSLATIONS['lux']})")
        fig.update_layout(xaxis_title=TRANSLATIONS['time'])
        st.plotly_chart(fig, use_container_width=True)

def create_air_quality_chart(df):
    """Create chart for air quality readings"""
    if df is not None:
        fig = px.line(df, x='Timestamp', y='Voltage',
                     title=f"{TRANSLATIONS['voltage']} ({TRANSLATIONS['volts']})")
        fig.update_layout(xaxis_title=TRANSLATIONS['time'])
        st.plotly_chart(fig, use_container_width=True)

def create_voltage_server_charts(df):
    """Create charts for voltage server readings"""
    if df is not None:
        # Voltage chart using lowercase Timestamp
        fig_voltage = px.line(df, x='timestamp', y='voltage',
                            title=f"{TRANSLATIONS['voltage']} ({TRANSLATIONS['volts']})")
        fig_voltage.update_layout(xaxis_title=TRANSLATIONS['time'])
        st.plotly_chart(fig_voltage, use_container_width=True)

def create_voltage_comparison(mq135_df, voltage_server_df):
    """Create voltage comparison chart"""
    if mq135_df is not None and voltage_server_df is not None:
        fig = go.Figure()

        # Add MQ135 voltage trace
        fig.add_trace(go.Scatter(
            x=mq135_df['Timestamp'],
            y=mq135_df['Voltage'],
            name='MQ135',
            mode='lines'
        ))

        # Add server voltage trace (using lowercase timestamp)
        fig.add_trace(go.Scatter(
            x=voltage_server_df['timestamp'],
            y=voltage_server_df['voltage'],
            name='Server Sensor',
            mode='lines'
        ))

        fig.update_layout(
            title=TRANSLATIONS['voltage_comparison'],
            xaxis_title=TRANSLATIONS['time'],
            yaxis_title=f"{TRANSLATIONS['voltage']} ({TRANSLATIONS['volts']})"
        )
        st.plotly_chart(fig, use_container_width=True)

def display_data_section(df, title, chart_function, comparison_function=None, comparison_df=None):
    """Display data section with tabs for chart and raw data"""
    if df is not None:
        st.subheader(title)

        # Determine number of tabs based on whether comparison is available
        if comparison_function and comparison_df is not None:
            tab1, tab2, tab3 = st.tabs([
                TRANSLATIONS['chart_tab'],
                TRANSLATIONS['data_tab'],
                TRANSLATIONS['comparison_tab']
            ])
            with tab3:
                comparison_function(df, comparison_df)
        else:
            tab1, tab2 = st.tabs([TRANSLATIONS['chart_tab'], TRANSLATIONS['data_tab']])

        with tab1:
            chart_function(df)

        with tab2:
            st.write(f"📊 {len(df)} {TRANSLATIONS['rows']}, {len(df.columns)} {TRANSLATIONS['columns']}")
            st.dataframe(df)

def main():
    # Page title
    st.title(TRANSLATIONS['title'])

    # Load datasets
    env_df = load_and_prepare_csv('environmental_data.csv')
    light_df = load_and_prepare_csv('light_readings.csv')
    air_df = load_and_prepare_csv('mq135_readings.csv')
    voltage_server_df = load_and_prepare_csv('voltage_readings_server.csv')

    # Create column layout
    col1, col2 = st.columns(2)

    # Display sections
    with col1:
        display_data_section(env_df, TRANSLATIONS['env_data'], create_environmental_charts)
        display_data_section(light_df, TRANSLATIONS['light_data'], create_light_chart)

    with col2:
        display_data_section(air_df, TRANSLATIONS['air_quality'], create_air_quality_chart)
        # Add the voltage server display section
        display_data_section(
            voltage_server_df,
            TRANSLATIONS['voltage_server'],
            create_voltage_server_charts,
            create_voltage_comparison,
            air_df
        )

if __name__ == "__main__":
    main()

