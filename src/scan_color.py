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

# google_api_functions used to update Spreadsheet
import sys
sys.path.append('google_api_functions')
import google_api_functions as api

# A scanned barcode returns 8 bytes
BYTES_PER_SCAN = 8

# Get the barcode-color mappings
with open('../bin/color_key.json', 'r') as mapping_file:
	mappings = json.loads(mapping_file.read())

# We can read bytes from the scanner using its device file, hidraw0
scanner = open('/dev/hidraw0', 'rb')

def scan():
	""" Read barcodes from the scanner until there is a
	Keyboard Interrupt. 
	"""
	print("Reading input from the scanner. Press Ctrl+c to quit.\n")
	current_code = ""
	while True:
		try:
			# Scanner will read 8 bytes from the barcode
			buffer = scanner.read(BYTES_PER_SCAN)
	
			""" Encode the bytes using HID Keyboard Usage ID mappings
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
						try:
							color = mappings[current_code]
							print("Scanned filament color %s" % color)
							count_filament(color)
						except KeyError:
							print("Barcode does not correspond to any known color")
						finally:
							# Reset the code string so more codes can be scanned
							current_code = ""
					else:
						current_code += str(usage_id) + " "
		except KeyboardInterrupt:
			print("\nKeyboard Interrupt: Stop scanning")
			sys.exit()
	
def count_filament(color):
	""" Log scanned color to the Filament Tracking spreadsheet
	"""
	sheets_service = api.get_sheets_service()
	# Get sheet ID from the file
	with open('../bin/sheet_id.txt', 'r') as sheet_id_file:
		spreadsheet_id = sheet_id_file.readline().splitlines()[0]
	range = "Sheet1!A2:B"
	# Check what values are currently in the sheet
	values_response = sheets_service.spreadsheets().values().get(
					spreadsheetId=spreadsheet_id, range=range).execute()
	values = values_response.get("values", [])
	# Update the correct row in the sheet
	current_row = 1
	row_number = -1
	for row in values:
		current_row = current_row + 1
		if row[0] == color:
			# Color has been found in sheet. Increment quantity
			try:
				new_quantity = int(row[1]) + 1
			except:
				# Handle case where cell is blank (row[1] will not exist)
				new_quantity = 1
			row_number = current_row
			print("%s found in sheet on row %d" %(color, row_number))
	if row_number < 0:
		# Color not yet in sheet. Add to sheet with quantity zero
		print("%s is not yet on the sheet. Adding with quantity 0" % color)
		new_quantity = 0
		row_number = current_row + 1
	update_values = [[color, new_quantity]]
	update_range = "A" + str(row_number) + ":B" + str(row_number)
	body = {"values" : update_values}
	# Parse input as if entered into Google Sheets UI
	value_input_option = "RAW"
	update_result = sheets_service.spreadsheets().values().update(
					spreadsheetId = spreadsheet_id, range=update_range,
					valueInputOption=value_input_option, body=body).execute()

# Scan barcodes if this file is executed
if __name__ == "__main__":
	scan()
