#-*- coding:utf-8 -*-

import time
import sys
import socket
import base64
import cv2
from threading import Thread
import numpy as np

SERVER_PORT=11117
HOST_IP='125.137.84.142'
SERVER_IP='172.30.1.10'
BUF_SIZE=10240

#클라이언트와 통신을 담당하는 클래스. 쓰레드로 구현.
class Sender (Thread):

	#서버 소켓과 연결된 클라이언트 소켓을 인자로 받음
	#clientThreads는 현재 서버에 연결된 Sender클래스가 들어있는 list로
	#나중에 연결 끊기거나 할때 따로 처리할려고 넣어놓음.
	def __init__(self, clientSocket):
		Thread.__init__(self) 
		self.clientSocket=clientSocket

	#통신 쓰레드 함수
	def run(self):
		while True:
			#이미지 캡쳐 쓰레드에서 data얻어와서 클라이언트에게 보내고 응답받음. 무한루프
			data=capture.getStringData()
			
			self.clientSocket.send(capture.getStringData())
			print('send data : ', len(data))
		
			data=self.clientSocket.recv(1024)
			print('receive Data : ', data.decode())


#클라이언트와 연결을 담당하는 클래스. 쓰레드로 구현
class Server (Thread):

	#서버 소켓을 생성할 IP와 PORT를 인자로 받음
	clientThreads=[]

	def __init__(self, ip, port):
		Thread.__init__(self) 
		self.ip=ip
		self.port=port
		self.clientThreads=[]

	#클라이언트 연결 쓰레드
	def run(self):
		#서버 소켓 생성
		serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		serverSocket.bind((self.ip, self.port))

		#클라이언트가 연결될 때마다 클라이언트 소켓을 생성해서 
		#Sender클래스에 넘겨주고 통신 쓰레드를 돌림
		while True:
			print('wait client connect...')
			serverSocket.listen(0)
			clientSocket, addr=serverSocket.accept()

			print('client connect!')
			clientThread=Sender(clientSocket)
			clientThreads.append(clientThread)
			clientThread.start()


	def getClientThreads(self):
		return self.clientThreads


#카메라 캡쳐 담당 클래스
class Capture(Thread):

	#카메라 객체를 인자로 초기화
	def __init__(self, cam):
		Thread.__init__(self) 
		self.cam=cam

	#캡쳐 쓰레드
	def run(self):
		#이미지 캡쳐해서 stringData 변수에 저장. 
		#Sender클래스에서 언제든지 getStringData()함수로 꺼내갈 수 있다.
		while True:
			ret,img=self.cam.read()
			img=cv2.resize(img, (128, 80), interpolation = cv2.INTER_AREA)
			encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
			result,imagencode=cv2.imencode('.jpg',img,encode_param)
			data=np.array(imagencode)

			self.stringData=base64.encodestring(data.tostring())

	#다른 클래스에서 캡쳐한 stringData를 꺼내가도록 만든 함수
	def getStringData(self):
		return self.stringData

#각각 다른 클래스에서 써야되는건 다 전역변수로
cam=cv2.VideoCapture(0)
capture = Capture(cam)
capture.start()

server = Server(SERVER_IP, SERVER_PORT)
server.start()
