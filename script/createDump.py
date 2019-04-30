#!/usr/bin/env python3
#Takes hexdumps (eg. xxd -g 1 [file]) and makes binaries out of them.
import struct
import sys

EXPECTEDADDR = 0
binaryData = b''

if len(sys.argv) > 3:
    BASEADDR = int(sys.argv[3], 16) #Where is it loaded in RAM?
    with open(sys.argv[1]) as k:
        data = k.read()
        data = data.split('\n')   
        for i, line in enumerate(data):
            try:
                address = line[:8]
                address
                fileAddr = int(address, 16)-BASEADDR
                if(fileAddr != EXPECTEDADDR):
                    raise ValueError
                hexBytes = line[10:57]
                hexBytes = hexBytes.split(' ')
                for byte in hexBytes:
                    binaryData += struct.pack("B", int(byte, 16))
                EXPECTEDADDR += 16
                print(i)
            except ValueError:  #read address is not the one expected
                print("Error in line: ", i)
                exit(1)
    
    binaryData = bytearray(binaryData)
    with open(sys.argv[2], "wb") as out:
        out.write(binaryData)
        print("File has been written to", sys.argv[2])

else:
    print("Usage:", sys.argv[0], "[inputfile] [outputfile] [baseaddress]")