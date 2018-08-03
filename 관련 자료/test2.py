#! /usr/bin/env python

# Client and server for udp (datagram) echo.
#
# Usage: udpecho -s [port]            (to start a server)
# or:    udpecho -c host [port] <file (client)

import time
import cv2
import numpy as np
import sys
import base64
from socket import *

# ECHO_PORT basic port
ECHO_PORT = 50000 + 7

# buffer size
BUFSIZE = 1024

# main func 
def main():
	# if parameter less than 2
	if len(sys.argv) < 2:
		# print usage
		usage()

	# if first parameter is '-s'
	if sys.argv[1] == '-s':
		#call server func
		server()

	# if first parameter is '-c'
	elif sys.argv[1] == '-c':
		#call client func
		client()

	# if not '-s' or '-c' 
	else:
		# print usage
		usage()

# print usage func
def usage():
	sys.stdout = sys.stderr
	print ('Usage: udpecho -s [port]            (server)')
	print ('or:    udpecho -c host [port] <file (client)')
	# exit
	sys.exit(2)

# server func
def server():
    
	# if parameters more than 2
	# ex>$ python udp_echo.py -s 8001
	if len(sys.argv) > 2:
		# set second parameter to port
		port = eval(sys.argv[2])

	# if the number of parameter is two
	# ex>$ python udp_echo.py -s
	else:
		# set basic port    
		port = ECHO_PORT

	# create socket (UDP = SOCK_DGRAM, TCP = SOCK_STREAM)
	s = socket(AF_INET, SOCK_DGRAM)
    
	# set port
	s.bind(('', port))
    
	# print ready
	print ('udp echo server ready')

	cam=cv2.VideoCapture(0)
	cam.set(3,1280) #CV_CAP_PROP_FRAME_WIDTH
	cam.set(4,720) #CV_CAP_PROP_FRAME_HEIGHT
				
	data, addr = s.recvfrom(BUFSIZE)
	#print received message and client address
	print ('server received %r from %r' % (data, addr))


	# enter loop
	while 1:
		# if client receive message continue next line
		# else wait(Blocking)
		startTime = time.time()

		ret,img=cam.read()
		img=cv2.resize(img, (128, 80), interpolation = cv2.INTER_AREA)

		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
		result,imagencode=cv2.imencode('.jpg',img,encode_param)
		data=np.array(imagencode)
		stringData=base64.encodestring(data.tostring())
		
		start=0
		end=len(stringData)
		while start < end :
			temp = stringData[start:start+1024]
			s.sendto(temp, addr)
			start+=1024
		
		#s.sendto(stringData, addr)
		#print('send data')
		
		endTime = time.time()-startTime
		
		if endTime < 0.5 :
			time.sleep(0.5-endTime)
		
		print(endTime)
		# echo message to client
		# s.sendto(data, addr)
		# go to first loop


# client func
def client():
	# if the number of parameter is less than 3
	if len(sys.argv) < 3:
		# print usage
		# exit program in usage func
		usage()

	# set second parameter to server IP
	host = sys.argv[2]

	# if the number of parameter more than 3
	# ex>$ python udp_echo.py -c 127.0.0.1 8001
	if len(sys.argv) > 3:
		# set third parameter to port
		port = eval(sys.argv[3])

	# else 
	# ex>$ python udp_echo.py -c 127.0.0.1
	else:
		# set basic port
		port = ECHO_PORT

	# set server address and port
	addr = host, port

	# create port
	s = socket(AF_INET, SOCK_DGRAM)
   
	# set client port : auto
	s.bind(('', 0))

	# print ready
	print ('udp echo client ready, reading stdin')

	# loop
	while 1:
		#by enter string in terminal 
			
		line = sys.stdin.readline()
		#if nothing in var
		if not line:
			break

		# send message to server
		s.sendto(line.encode(), addr)
		# wait return
		data, fromaddr = s.recvfrom(BUFSIZE)
		# print recieved message from server
		print ('client received %r from %r' % (data, fromaddr))
		

main()
