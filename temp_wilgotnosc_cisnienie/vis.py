import pandas as pd

import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'environmental_data.csv'
data = pd.read_csv(file_path)

# Convert the Timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Plot Temperature in Celsius
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], data['Temperature_C'], label='Temperature (C)')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (C)')
plt.title('Temperature Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot Pressure
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], data['Pressure_hPa'], label='Pressure (hPa)', color='orange')
plt.xlabel('Timestamp')
plt.ylabel('Pressure (hPa)')
plt.title('Pressure Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot Humidity
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], data['Humidity_%'], label='Humidity (%)', color='green')
plt.xlabel('Timestamp')
plt.ylabel('Humidity (%)')
plt.title('Humidity Over Time')
plt.legend()
plt.grid(True)
plt.show()