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

from microcontroller import watchdog as w
from watchdog import WatchDogMode

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Initialize Watchdog
w.timeout=16 # timeout in seconds
w.mode = WatchDogMode.RESET
w.feed()

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
w.feed()

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
w.feed()

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
w.feed()

# Initialize a requests object with a socket and esp32spi interface
socket.set_interface(esp)
requests.set_socket(socket, esp)
w.feed()
    
url = 'https://guarded-lake-30538.herokuapp.com/'
headers = {'X-Api-Key': secrets['api-key']}
w.feed()


matrixportal = MatrixPortal(esp=esp, debug=False)

FONT = "/fonts/helvR10.bdf"

matrixportal.add_text(text_font=FONT, text_position=(1,3), text_color=0xEF7F31)
w.feed()
matrixportal.add_text(text_font=FONT, text_position=(1,14), text_color=0xEF7F31)
w.feed()
matrixportal.add_text(text_font=FONT, text_position=(1,24), text_color=0xEF7F31)
w.feed()



while True:
    try:
        w.feed()

        r = requests.get(url, headers=headers)
        w.feed()
        
        for message in r.json()['data']:
            matrixportal.set_text(message[0], 0)
            w.feed()
            matrixportal.set_text(message[1], 1)
            w.feed()
            matrixportal.set_text(message[2], 2)
            w.feed()
            
            time.sleep(5)
            w.feed()
    
    except Exception as e:
        w.feed()
        
        matrixportal.set_text('There', 0)
        w.feed()
        matrixportal.set_text('is an', 1)
        w.feed()
        matrixportal.set_text('Error', 2)
        w.feed()
        time.sleep(5)
        w.feed()
        pass

matrixportal.set_text('Outside', 0)
matrixportal.set_text('While', 1)
matrixportal.set_text('Loop', 2)