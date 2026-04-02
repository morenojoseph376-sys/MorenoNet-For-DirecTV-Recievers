import socket
import datetime

# The Heart of Knollcrest Ave
SERVER_IP = "192.168.1.55"
MCAST_GRP = "239.255.255.250"
MCAST_PORT = 1900

# Perfect formatting for the 2019 box
DATE_STR = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

SSDP_RESPONSE = f"""HTTP/1.1 200 OK
CACHE-CONTROL: max-age=1800
DATE: {DATE_STR}
EXT:
LOCATION: http://192.168.1.55:8080/device.xml
SERVER: Linux/5.15 UPnP/1.0 DIRECTV Genie/3.0
ST: urn:schemas-upnp-org:device:MediaServer:1
USN: uuid:5aa5db49-70b6-4400-bd38-a7c882b35536::urn:schemas-upnp-org:device:MediaServer:1

""".replace("\n", "\r\n")

def start_ssdp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", MCAST_PORT))

    # Join the group so we can hear the 2019 box
    mreq = socket.inet_aton(MCAST_GRP) + socket.inet_aton("0.0.0.0")
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"MorenoNet LIVE on {SERVER_IP}. Waiting for 2019 box...")

    while True:
        data, addr = sock.recvfrom(1024)
        if b"M-SEARCH" in data:
            print(f"Handshake attempt from: {addr[0]}")
            # Send the map (LOCATION) to the box
            sock.sendto(SSDP_RESPONSE.encode(), addr)

if __name__ == "__main__":
    start_ssdp()