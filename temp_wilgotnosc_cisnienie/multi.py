import time
import smbus2
import bme280
import csv
from datetime import datetime
import os

# BME280 sensor address (default address)
address = 0x76
# Initialize I2C bus
bus = smbus2.SMBus(1)
# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# CSV Configuration
CSV_FILENAME = 'environmental_data.csv'
CSV_HEADERS = ['Timestamp', 'Temperature_C', 'Temperature_F', 'Pressure_hPa', 'Humidity_%']

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def setup_csv():
    # Create CSV file with headers if it doesn't exist
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

def log_reading(temp_c, temp_f, pressure, humidity):
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append data to CSV file
    with open(CSV_FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp,
            f"{temp_c:.2f}",
            f"{temp_f:.2f}",
            f"{pressure:.2f}",
            f"{humidity:.2f}"
        ])

def main():
    # Setup CSV file
    setup_csv()
    
    print(f"Logging environmental data to {CSV_FILENAME}")
    print("Press CTRL+C to stop")
    
    while True:
        try:
            # Read sensor data
            data = bme280.sample(bus, address, calibration_params)
            
            # Extract temperature, pressure, and humidity
            temperature_celsius = data.temperature
            pressure = data.pressure
            humidity = data.humidity
            
            # Convert temperature to Fahrenheit
            temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)
            
            # Print the readings
            print("\nCurrent Readings:")
            print("Temperature: {:.2f} °C, {:.2f} °F".format(
                temperature_celsius, temperature_fahrenheit))
            print("Pressure: {:.2f} hPa".format(pressure))
            print("Humidity: {:.2f} %".format(humidity))
            
            # Log the readings to CSV
            log_reading(
                temperature_celsius,
                temperature_fahrenheit,
                pressure,
                humidity
            )
            
            # Wait for a few seconds before the next reading
            time.sleep(10)
            
        except KeyboardInterrupt:
            print('\nProgram stopped by user')
            break
        except Exception as e:
            print('\nAn unexpected error occurred:', str(e))
            break
    
    print(f"Data has been saved to {CSV_FILENAME}")

if __name__ == "__main__":
    main()
