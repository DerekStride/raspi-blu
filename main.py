from bluetooth import *
import sys

if sys.version < '3':
    input = raw_input

addr = None

if len(sys.argv) < 2:
    print("no device specified.  Searching all nearby bluetooth devices for")
    print("the SampleServer service")
else:
    addr = sys.argv[1]
    print("Searching for SampleServer on %s" % addr)

# search for the SampleServer service
uuid = "2e417dae-6c5f-476e-bcfb-295d161b5b81"

service_matches = []

while len(service_matches) == 0:
    service_matches = find_service( uuid = uuid, address = addr )

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s, port: %s" % (name, host, port))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print("connected.  receiving data.")
data = ""
try:
    while True:
        recv = sock.recv(1024)
        if len(recv) == 0: break
        print(recv)
        data += recv
except IOError:
    print("pass")
    pass

print("received [%s]" % data)
ssid, psk = data.split("|")
print("SSID: %s\nPSK:  %s", ssid, psk)
