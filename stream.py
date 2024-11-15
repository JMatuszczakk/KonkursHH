import streamlit as st
import pandas as pd
import plotly.express as px
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
    'title': "Panel Danych Środowiskowych",
    'env_data': "Dane Środowiskowe",
    'light_data': "Pomiary Światła",
    'air_quality': "Pomiary Jakości Powietrza",
    'loading_error': "Błąd wczytywania pliku",
    'file_not_found': "Nie znaleziono pliku",
    'rows': "wierszy",
    'columns': "kolumn",
    'temperature': "Temperatura",
    'pressure': "Ciśnienie",
    'humidity': "Wilgotność",
    'light_level': "Poziom Światła",
    'voltage': "Napięcie",
    'time': "Czas",
    'chart_tab': "Wykres",
    'data_tab': "Dane",
    'celsius': "°C",
    'fahrenheit': "°F",
    'hpa': "hPa",
    'percent': "%",
    'lux': "lx",
    'volts': "V"
}

def load_and_prepare_csv(file_path):
    """Load CSV file and prepare data for visualization"""
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # Convert timestamp to datetime
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
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

def display_data_section(df, title, chart_function):
    """Display data section with tabs for chart and raw data"""
    if df is not None:
        st.subheader(title)
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

    # Display sections
    display_data_section(env_df, TRANSLATIONS['env_data'], create_environmental_charts)
    display_data_section(light_df, TRANSLATIONS['light_data'], create_light_chart)
    display_data_section(air_df, TRANSLATIONS['air_quality'], create_air_quality_chart)
    
    # Add footer
    st.markdown("---")
    st.markdown("💡 **Wskazówka:** Możesz przybliżać i oddalać wykresy, a także pobierać je jako obrazy.")

if __name__ == "__main__":
    main()
