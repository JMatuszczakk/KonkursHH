#!/usr/bin/python
#---------------------------------------------------------------------
#    ___  ___  *_*__
#   / * \/ * \(_) **/**  
#  / , */ *__/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bh1750.py
# Read data from a BH1750 digital light sensor and log to CSV.
#
# Author : Matt Hawkins (Original)
# Modified: [Your name]
# Date   : [Current date]
#
#---------------------------------------------------------------------
import smbus
import time
import csv
from datetime import datetime
import os

# Define some constants from the datasheet
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

# CSV Configuration
CSV_FILENAME = 'light_readings.csv'
CSV_HEADERS = ['Timestamp', 'Light_Level_lx']

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number
    result=(data[1] + (256 * data[0])) / 1.2
    return (result)

def readLight(addr=DEVICE):
    # Read data from I2C interface
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

def setup_csv():
    # Create CSV file with headers if it doesn't exist
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

def log_reading(light_level):
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append data to CSV file
    with open(CSV_FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, f"{light_level:.2f}"])

def main():
    print(f"Logging light sensor data to {CSV_FILENAME}")
    print("Press CTRL+C to stop")
    
    # Setup CSV file
    setup_csv()
    
    try:
        while True:
            lightLevel = readLight()
            # Print to console
            print(f"Light Level : {lightLevel:.2f} lx")
            # Log to CSV
            log_reading(lightLevel)
            # Wait before next reading
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nLogging stopped by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print(f"\nData has been saved to {CSV_FILENAME}")

if __name__=="__main__":
    main()
