import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import csv
from datetime import datetime
import os

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)

# CSV file setup
CSV_FILENAME = 'mq135_readings.csv'
CSV_HEADERS = ['Timestamp', 'Voltage']

# Check if file exists and create with headers if it doesn't
if not os.path.exists(CSV_FILENAME):
    with open(CSV_FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)

try:
    while True:
        # Get current timestamp and voltage reading
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        voltage = chan.voltage
        
        # Append data to CSV file
        with open(CSV_FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, voltage])
        
        # Print to console for monitoring
        print(f"MQ-135 Voltage: {voltage:.3f}V - Data logged at {timestamp}")
        
        # Wait for 1 second before next reading
        time.sleep(10)

except KeyboardInterrupt:
    print("\nLogging stopped by user")
except Exception as e:
    print(f"\nAn error occurred: {str(e)}")
finally:
    print(f"\nData has been saved to {CSV_FILENAME}")
