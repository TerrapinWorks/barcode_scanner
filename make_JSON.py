import json
code_to_color = []
with open('./test_colors.txt', 'r') as file:
	lines = file.read().splitlines()
	for line in lines:
		barcode = line.split(' - ')
		code_to_color.append({barcode[0] : barcode[1]})
with open('./color_key.json', 'w') as file:
	json.dump(code_to_color, file)
