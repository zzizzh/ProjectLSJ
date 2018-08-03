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

#Ŭ���̾�Ʈ�� ����� ����ϴ� Ŭ����. ������� ����.
class Sender (Thread):

	#���� ���ϰ� ����� Ŭ���̾�Ʈ ������ ���ڷ� ����
	#clientThreads�� ���� ������ ����� SenderŬ������ ����ִ� list��
	#���߿� ���� ����ų� �Ҷ� ���� ó���ҷ��� �־����.
	def __init__(self, clientSocket):
		Thread.__init__(self) 
		self.clientSocket=clientSocket

	#��� ������ �Լ�
	def run(self):
		while True:
			#�̹��� ĸ�� �����忡�� data���ͼ� Ŭ���̾�Ʈ���� ������ �������. ���ѷ���
			data=capture.getStringData()
			
			self.clientSocket.send(capture.getStringData())
			print('send data : ', len(data))
		
			data=self.clientSocket.recv(1024)
			print('receive Data : ', data.decode())


#Ŭ���̾�Ʈ�� ������ ����ϴ� Ŭ����. ������� ����
class Server (Thread):

	#���� ������ ������ IP�� PORT�� ���ڷ� ����
	clientThreads=[]

	def __init__(self, ip, port):
		Thread.__init__(self) 
		self.ip=ip
		self.port=port
		self.clientThreads=[]

	#Ŭ���̾�Ʈ ���� ������
	def run(self):
		#���� ���� ����
		serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		serverSocket.bind((self.ip, self.port))

		#Ŭ���̾�Ʈ�� ����� ������ Ŭ���̾�Ʈ ������ �����ؼ� 
		#SenderŬ������ �Ѱ��ְ� ��� �����带 ����
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


#ī�޶� ĸ�� ��� Ŭ����
class Capture(Thread):

	#ī�޶� ��ü�� ���ڷ� �ʱ�ȭ
	def __init__(self, cam):
		Thread.__init__(self) 
		self.cam=cam

	#ĸ�� ������
	def run(self):
		#�̹��� ĸ���ؼ� stringData ������ ����. 
		#SenderŬ�������� �������� getStringData()�Լ��� ������ �� �ִ�.
		while True:
			ret,img=self.cam.read()
			img=cv2.resize(img, (128, 80), interpolation = cv2.INTER_AREA)
			encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
			result,imagencode=cv2.imencode('.jpg',img,encode_param)
			data=np.array(imagencode)

			self.stringData=base64.encodestring(data.tostring())

	#�ٸ� Ŭ�������� ĸ���� stringData�� ���������� ���� �Լ�
	def getStringData(self):
		return self.stringData

#���� �ٸ� Ŭ�������� ��ߵǴ°� �� ����������
cam=cv2.VideoCapture(0)
capture = Capture(cam)
capture.start()

server = Server(SERVER_IP, SERVER_PORT)
server.start()
