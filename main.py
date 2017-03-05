from bluetooth import *
import sys
import os
import time

SSID_PLACEHOLDER = "RASPI_BLU_SSID"
PSK_PLACEHOLDER = "RASPI_BLU_PSK"
RASPI_UUID = "2e417dae-6c5f-476e-bcfb-295d161b5b81"
CONFIG_TEMPLATE = "config/wpa_supplicant.conf"
CONFIG_BACKUP = "backup/wpa_supplicant.conf"
CONFIG_DEST = "/etc/wpa_supplicant/wpa_supplicant.conf"
# CONFIG_DEST = "test/wpa_supplicant.conf"

if sys.version < '3':
    input = raw_input

def restore():
    backup = read_config(CONFIG_BACKUP)
    write_config(CONFIG_DEST, backup)

def read_config(path):
    f = open(path, "r")
    in_str = f.read()
    f.close()
    return in_str

def write_config(path, output):
    f = open(path, "w")
    f.write(output)
    f.close()

def build_config(ssid, psk):
    f = open(CONFIG_TEMPLATE, "r")
    file_string = f.read()
    f.close()
    output = file_string.replace(SSID_PLACEHOLDER, ssid).replace(PSK_PLACEHOLDER, psk)
    print(output)
    return output

# search for the SampleServer service
def fetch_info():
    service_matches = []

    while len(service_matches) == 0:
        service_matches = find_service( uuid = RASPI_UUID, address = None )

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("connecting to \"%s\" on %s, port: %s" % (name, host, port))

    # Create the client socket
    sock = BluetoothSocket( RFCOMM )
    sock.connect((host, port))

    print("connected.  receiving data.")
    data = ""
    try:
        data = sock.recv(1024)
    except IOError:
        pass

    print("received [%s]" % data)
    ssid, psk = data.split("|")
    print("SSID: %s\nPSK:  %s" % (ssid, psk))
    return ssid, psk

ssid, psk = fetch_info()
# ssid, psk = "SLAM", "ieeeisthebest"

backup = read_config(CONFIG_DEST)
output = build_config(ssid, psk)
write_config(CONFIG_BACKUP, backup)
write_config(CONFIG_DEST, output)

time.sleep(3)

os.system('sudo wpa_cli reconfigure')
