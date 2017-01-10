import sys

scanner = open('/dev/hidraw0', 'rb')
write_file = open('./output.txt', 'w')


while True:
	buffer = scanner.read(8)
	for c in buffer:
		if ord(c) > 0:
			print(ord(c))
			write_file.write("%d " % ord(c))
print("\n")
