import struct
import sys

kernel = open(sys.argv[1], "rb").read()
fdt = open(sys.argv[2], "rb").read()

import usb.core

dev = usb.core.find(idVendor=0x05ac, idProduct=0x4141)
if dev is None:
    raise ValueError('Device not found')
dev.set_configuration()

print("Loading device tree...")

dev.ctrl_transfer(0x21, 2, 0, 0, 0)
dev.ctrl_transfer(0x21, 1, 0, 0, 0)
dev.write(2, fdt)

dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "fdt\n")
print("Device tree loaded successfully!")

print("Loading kernel...")
kernel_size = len(kernel)
print("kernel_size = " + str(kernel_size))
dev.ctrl_transfer(0x21, 2, 0, 0, 0)
dev.ctrl_transfer(0x21, 1, 0, 0, struct.pack('I', kernel_size))

dev.write(2, kernel, 1000000)

print("done?")
dev.ctrl_transfer(0x21, 4, 0, 0, 0)

print("Booting...")
try:
	dev.ctrl_transfer(0x21, 3, 0, 0, "bootl\n")
except:
	# if the device disconnects without acknowledging it usually means it succeeded
	print("Success.")
