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
    
url = 'https://guarded-lake-30538.herokuapp.com/'
headers = {'X-Api-Key': secrets['api-key']}


matrixportal = MatrixPortal(url=url, headers=headers, status_neopixel=board.NEOPIXEL, debug=False)

FONT = "/fonts/helvR10.bdf"

matrixportal.add_text(text_font=FONT, text_position=(1,3), text_color=0xEF7F31)
matrixportal.add_text(text_font=FONT, text_position=(1,14), text_color=0xEF7F31)
matrixportal.add_text(text_font=FONT, text_position=(1,24), text_color=0xEF7F31)



while True:
    try:
        r = matrixportal.fetch()
        r = json.loads(r)
        
        for message in r['data']:
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