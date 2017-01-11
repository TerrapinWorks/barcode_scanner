__author__ = "Adam Anderson"
__maintainer__ = "Adam Anderson"
__email__ = "adam.b.anderson.96@gmail.com"

""" Store barcode-color mapping to JSON
In ../bin/handwritten_color_key.txt, a list of
HID Keyboard Usage IDs with their corresponding 
fillament color has been compiled. 
This script parses that manually writen list
into a JSON file 
"""

# To store the barcode-color mapping dictionary to a JSON
import json

mappings = {}
with open('../bin/handwritten_color_key.txt', 'r') as file:
	# Each mapping is stored on a separate line
	lines = file.read().splitlines()
	for line in lines:
		# Usage ID/color pairs are separated by ' - '
		split_line = line.split(' - ')
		mappings.update({split_line[0] : split_line[1]})

# Save the dictionary to color_key.json
with open('../bin/color_key.json', 'w') as color_key:
	json.dump(mappings, color_key)
