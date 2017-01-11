__author__ = "Adam Anderson"
__mainainer__ = "Adam Anderson"
__email__ = "adam.b.anderson.96@gmail.com"

""" Scan barcode from Makerbot filament spool to determine
the color. For now, the color is just printed to the terminal.
In the future, this will be integrated with the
filament tracking Google Sheet to automate filament tracking
in the MIC
"""

# The barcode-color mappings are stored in color_key.json
import json

# A scanned barcode returns 8 bytes
BYTES_PER_SCAN = 8

# Get the barcode-color mappings
with open('../bin/color_key.json', 'r') as mapping_file:
	mappings = json.loads(mapping_file.read())

# We can read bytes from the scanner using its device file, hidraw0
scanner = open('/dev/hidraw0', 'rb')

# Read barcodes from the scanner
current_code = ""
# Continue until keyboard Interrupt
while True:
	# Scanner will read 8 bytes from the barcode
	buffer = scanner.read(BYTES_PER_SCAN)

	""" Re-encode the bytes using HID Keyboard Usage ID mappings
	For a table of mappings, see page 53 of the below PDF:
	http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
	"""
	for usage_id in buffer:
		""" Python3 reads each byte as a number without encoding.
		In Python2, the bytes will be encoded as ASCII characters,
		so the usage_id will be equal to ord(ascii_char)
		"""
		if usage_id > 0:
			if usage_id == 40:
				""" 40 is the HID carriage return, meaning we have finished
				scanning a bar code. Trim whitespace from the code string and
				find the corresponding color.
				"""
				current_code = current_code.strip()
				color = mappings[current_code]
				print(color)
				current_code = ""
			else:
				current_code += str(usage_id) + " "
