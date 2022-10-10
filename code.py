import board
import busio
import time
import terminalio
import json
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_matrixportal.matrixportal import MatrixPortal
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

# Initialize a requests object with a socket and esp32spi interface
socket.set_interface(esp)
requests.set_socket(socket, esp)
    
url = 'https://guarded-lake-30538.herokuapp.com/'
headers = {'X-Api-Key': secrets['api-key']}


matrixportal = MatrixPortal(esp=esp, debug=False)

FONT = "/fonts/helvR10.bdf"

matrixportal.add_text(text_font=FONT, text_position=(1,3), text_color=0xEF7F31)
matrixportal.add_text(text_font=FONT, text_position=(1,14), text_color=0xEF7F31)
matrixportal.add_text(text_font=FONT, text_position=(1,24), text_color=0xEF7F31)



while True:
    try:
        r = requests.get(url, headers=headers)
        
        for message in r.json()['data']:
            matrixportal.set_text(message[0], 0)
            matrixportal.set_text(message[1], 1)
            matrixportal.set_text(message[2], 2)
            
            time.sleep(5)
    
    except Exception as e:
        matrixportal.set_text('There', 0)
        matrixportal.set_text('is an', 1)
        matrixportal.set_text('Error', 2)
        time.sleep(5)
        pass

matrixportal.set_text('Outside', 0)
matrixportal.set_text('While', 1)
matrixportal.set_text('Loop', 2)