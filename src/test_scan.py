""" Read numbers from the barcode scanner
This script reads numbers from the barcode scanner and
prints them to the terminal, as well as to
../bin/test_output.txt
"""

scanner = open('/dev/hidraw0', 'rb')
write_file = open('../bin/test_output.txt', 'w')

# Read input until keyboard interrupt
while True:
	# Read 8 bytes = 1 barcode
	buffer = scanner.read(8)
	for usage_id in buffer:
		if usage_id > 0:
			print(usage_id)
			write_file.write("%d " % usage_id)
print("\n")
