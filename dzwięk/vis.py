import pandas as pd

import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('halas_przekonwertowany.csv')

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], data['dB'], label='Noise Level')
plt.xlabel('Time')
plt.ylabel('Noise Level')
plt.title('Noise Level Over Time')
plt.legend()
plt.grid(True)
plt.show()