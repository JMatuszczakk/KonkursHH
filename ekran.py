#!/usr/bin/env python3
import socket
import time
from subprocess import check_output
from smbus2 import SMBus
from RPLCD.i2c import CharLCD

def get_ip_address():
    """Get the local IP address of the Raspberry Pi"""
    try:
        # Try to get IP from eth0 first
        ip = check_output(['hostname', '-I']).decode('utf-8').strip().split()[0]
        return ip
    except:
        try:
            # Fallback to socket method
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "No IP found"

def setup_lcd():
    """Initialize the LCD display"""
    # Common I2C address for 16x2 LCD is 0x27, but might be 0x3F
    try:
        lcd = CharLCD('PCF8574', 0x27, port=1, cols=16, rows=2)
    except:
        try:
            lcd = CharLCD('PCF8574', 0x3F, port=1, cols=16, rows=2)
        except Exception as e:
            print(f"Error initializing LCD: {e}")
            return None
    return lcd

def main():
    # Initialize LCD
    lcd = setup_lcd()
    if not lcd:
        print("Failed to initialize LCD. Exiting...")
        return

    # Initial display
    lcd.clear()
    lcd.write_string("IP Address:")
    
    # Main loop
    while True:
        try:
            # Get IP address
            ip = get_ip_address()
            
            # Clear second line and display IP
            lcd.cursor_pos = (1, 0)
            lcd.write_string(ip.ljust(16))  # Pad with spaces to clear old characters
            
            # Wait 30 seconds before next update
            time.sleep(30)
            
        except Exception as e:
            print(f"Error: {e}")
            lcd.clear()
            lcd.write_string("Error getting IP")
            time.sleep(5)
            
        except KeyboardInterrupt:
            lcd.clear()
            break

if __name__ == "__main__":
    main()
