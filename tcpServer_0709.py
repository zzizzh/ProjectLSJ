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

'''
class that send image stringData to clinet(android)
'''
class Sender (Thread):

	def __init__(self, clientSocket):
		Thread.__init__(self) 
		self.clientSocket=clientSocket

	def run(self):
		while True:
			data=imageProcess.getStringData()
			
			self.clientSocket.send(imageProcess.getStringData())
			#print('send data : ', len(data))
		
			data=self.clientSocket.recv(1024)
			#print('receive Data : ', data.decode())

'''
main server has clientThread list
if connect client, make thread(Sender class) and and thread list(clientThreads)
and wait another connection from client
'''
class Server (Thread):

	def __init__(self, ip, port):
		Thread.__init__(self) 
		self.ip=ip
		self.port=port
		self.clientThreads=[]

	def run(self):
		serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		serverSocket.bind((self.ip, self.port))

		while True:
			print('wait client connect...')
			serverSocket.listen(0)
			clientSocket, addr=serverSocket.accept()

			print('client connect!')
			clientThread=Sender(clientSocket)
			self.clientThreads.append(clientThread)
			clientThread.start()

	def getClientThreads(self):
		return self.clientThreads

'''

'''
class ImageProcess(Thread):

	def __init__(self, cam):
		Thread.__init__(self) 
		self.cam=cam
		#self.width=int(cam.get(CV_CAP_PROP_FRAME_WIDTH)
		#self.height=int(cam.get(CV_CAP_PROP_FRAME_HEIGHT))
		self.lastMovement=time.time()
		self.detectingCount=1
		self.detectingMove = []

	def run(self):

		ret, self.bgImg=cam.read()

		while True:
			ret, curImg=self.cam.read()

			self.Img2String(curImg)
			self.getDiffCurBtwBg(curImg)

			term=time.time()-self.lastMovement

			if term > self.detectingCount * 3600 :
				self.detectingCount=self.detectingCount+1
				
	'''
	select comparing image to detect movement
	'''
	def getDiffCurBtwBg(self, curImg):
		print('diff func start')

		#convert current image to gray imae
		curGrayImg=cv2.cvtColor(curImg, cv2.COLOR_BGR2GRAY)
		#convert 
		bgGrayImg=cv2.cvtColor(self.bgImg, cv2.COLOR_BGR2GRAY)

		diffImg=cv2.absdiff(curGrayImg, bgGrayImg)

		count=0
		print('count init: ', count)
		#print(type(diffImg))
		#print(diffImg)
		#print(diffImg.shape)

		for diffList in diffImg:
			for diff in diffList:
				if diff > 50:
					count=count+1

		print('diff > 50 count : ', count)

		if count > 500 :
			self.lastMovement=time.time()
			self.detectingMove.append(time.ctime())
			self.detectingCount=1

		print('diff func end')

	'''
	read cam image and convert to stringData=base64
	'''
	def Img2String(self, culImg):
		ret, curImg=self.cam.read()
		sendImg=cv2.resize(curImg, (128, 80), interpolation = cv2.INTER_AREA)
		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
		result,imagencode=cv2.imencode('.jpg',sendImg,encode_param)
		data=np.array(imagencode)

		self.stringData=base64.encodestring(data.tostring())


	def getStringData(self):
		return self.stringData

	def getDiff(self):
		return self.diff
		
cam=cv2.VideoCapture(0)
time.sleep(1)

imageProcess=ImageProcess(cam)
imageProcess.start()

server=Server(SERVER_IP, SERVER_PORT)
server.start()
