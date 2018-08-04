#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
# Usage:
#   mcast -s (sender, IPv4)
#   mcast -s -6 (sender, IPv6)
#   mcast    (receivers, IPv4)
#   mcast  -6  (receivers, IPv6)

MYPORT = 11117
MYGROUP_4 = '225.0.0.250'
MYGROUP_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
MYTTL = 1 # Increase to reach other networks

import base64
import time
import struct
import socket
import sys
import cv2
import numpy as np

def main():
	group = MYGROUP_6 if "-6" in sys.argv[1:] else MYGROUP_4

	if "-s" in sys.argv[1:]:
		sender(group)
	else:
		receiver(group)


def sender(group):
	cam=cv2.VideoCapture(0)

	addrinfo = socket.getaddrinfo(group, None)[0]

	s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

	# Set Time-to-live (optional)
	ttl_bin = struct.pack('@i', MYTTL)
	if addrinfo[0] == socket.AF_INET: # IPv4
		s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
	else:
		s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

	while True:
		data = capture(cam)
		#s.sendto(str(len(data)).encode(), (addrinfo[4][0], MYPORT))
		s.sendto(data, (addrinfo[4][0], MYPORT))
		print('send complete')
		time.sleep(1)


def receiver(group):
	# Look up multicast group address in name server and find out IP version
	addrinfo = socket.getaddrinfo(group, None)[0]

	# Create a socket
	s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

	# Allow multiple copies of this program on one machine
	# (not strictly needed)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind it to the port
	s.bind(('', MYPORT))

	group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
	# Join group
	if addrinfo[0] == socket.AF_INET: # IPv4
		mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	else:
		mreq = group_bin + struct.pack('@I', 0)
		s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop, printing any data we receive
	while True:
		data, sender = s.recvfrom(15000)
		while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
		print (str(sender) + '  ' + repr(data))

def capture(cam):
	ret,img=cam.read()
	img=cv2.resize(img, (128, 80), interpolation = cv2.INTER_AREA)
	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
	result,imagencode=cv2.imencode('.jpg',img,encode_param)
	data=np.array(imagencode)
	stringData=base64.encodestring(data.tostring())

	return stringData
		

if __name__ == '__main__':
	main()