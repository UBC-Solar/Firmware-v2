import urequests
import ujson
from machine import UART
import utime

server_name = ''
read_delay = 500       # time delay between consecutive UART reads (in ms)

# Initialising UART
# TODO: surround with try-except statement
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

while True:
    # TODO: surround with try-except statement
    message = uart.read(26)        # reads len of one CAN message into 'message' buffer

    can_hex_string = "0x" + message.decode()        # converts byte object into hex string

    data_array = []
    for i in range(0, 16, 2):
        data_array.append(int(can_hex_string[10 + i: 12 + i], 16))      # populates data_array

    can_msg = dict()            # stores the CAN message which will be converted to a JSON string

    can_msg["timestamp"] = int(can_hex_string[2:6], 16)       # separates the first four hex digits as timestamp
    can_msg["id"] = int(can_hex_string[6:10], 16)        # continues separating the hex string into JSON key-value pairs
    can_msg["data"] = data_array
    can_msg["len"] = int(can_hex_string[26:28], 16)

    can_msg_json = ujson.dumps(can_msg)                     # converts CAN message into JSON string
    response = urequests.post(server_name, json=can_msg_json)       # TODO: add error-handling for this line

    utime.sleep_ms(read_delay)
