#!/usr/bin/env python
import socket
import fcntl
import struct
import urllib
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
def sae_request(ip):
    url = "http://1.alive.sinaapp.com/raspberrypi.php"
    req = urllib.urlopen(url, data = ip)
    req.read()

if __name__ == '__main__':
    ip = get_ip_address('eth0')
    sae_request(ip)
# end
