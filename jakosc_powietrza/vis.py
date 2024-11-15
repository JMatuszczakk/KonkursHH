import pandas as pd

import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('mq135_readings.csv')

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], data['Voltage'], label='Pollution Level')
plt.xlabel('Time')
plt.ylabel('Pollution Level')
plt.title('Pollution Level Over Time')
plt.legend()
plt.grid(True)
plt.show()