import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv('light_readings.csv')

# Convert the timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Create a line plot
plt.figure(figsize=(12, 6))
plt.plot(data['Timestamp'], data['Light_Level_lx'])
plt.xlabel('Timestamp')
plt.ylabel('Light Intensity (lx)')
plt.title('Light Intensity Over Time')
plt.grid()
plt.savefig('light_intensity_plot.png')

# Create a histogram
plt.figure(figsize=(8, 6))
plt.hist(data['Light_Level_lx'], bins=20)
plt.xlabel('Light Intensity (lx)')
plt.ylabel('Frequency')
plt.title('Distribution of Light Intensity')
plt.savefig('light_intensity_histogram.png')

print('Visualizations saved as light_intensity_plot.png and light_intensity_histogram.png')