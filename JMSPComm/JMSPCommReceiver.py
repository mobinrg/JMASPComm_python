# -*- coding: utf-8 -*-
#
#	JMSPCommSender
#
# Usage:
#
#   myComm = new JMSPCommReceiver()
#
#
#	Kunpeng Zhang
#	2018.10.25
#	
#	v1.0
#
import sys
import JMSPCRC8
from JMSPComm_1_0_0 import JMSPComm_config as COM_CONFIG
from JMSPComm_1_0_0 import JMSPCommDataFrameCheckStatus as COM_CHK_ST
from JMSPComm import JMSPComm

class JMSPCommReceiver(JMSPComm):
	_maxFrameLen = None
	_receiveCount = None
	_lastByte = None
	_hearder1 = None
	_hearder2 = None
	_frameLen = None

	# 数据帧开始 - 检测到 hearder1 = 0x02 && hearder2 = 0x3C
	_beginFrame = None


	# callback()
	onBeforeFrameVerifyCRC = None
	# callback()
	onFrameReceived = None
	# callback(err_code). eg. callback( 104 )
	onFrameErr = None
	# callback()
	onFrameBegin = None

	def __init__(self, maxFrameLen = 255):
		if sys.version_info < (3, 0):JMSPComm.__init__(self)
		if sys.version_info >= (3, 0): super().__init__()

		self._maxFrameLen = maxFrameLen
		self._receiveCount = 0x00
		self._lastByte= 0x00
		self._hearder1= 0x00
		self._hearder2= 0x00
		self._frameLen= 0x00

		# 数据帧开始 - 检测到 hearder1 = 0x02 && hearder2 = 0x3C
		self._beginFrame= False

	def initFrame(self):
		self.clearBuffer()
		self.dataFrame.append(COM_CONFIG.DATA_FRAME_HEADER_1)
		# self.dataFrame.append(COM_CONFIG.DATA_FRAME_HEADER_2)


	def addByte(self, aByte):
		"""!
		/~english
		Receive data
		@param aByte, 
			Adding a received byte of data to the buffer. Arise the onFrameReceived event if the packet is received correctly.
			Arise onFrameErr event If the packet is received with an error.
			Arise the onFrameBegin event when starting to receive new packets

		/~chinese
		接收数据

		@param aByte, 
			把接收的一个字节数据添加到缓存区，如果数据包接收正确，将会触发 onFrameReceived 事件。
			如果数据包接收有错误触发 onFrameErr 事件并传递错误代码。
			当开始接收新的数据包时触发 onFrameBegin 事件
		"""
		# 接收字符计数
		self._receiveCount += 1

		# 接收到完整头标志 - 清空当前数据缓存，然后初始化一个新数据缓存区
		# 0x3C and 0x02
		if ( COM_CONFIG.DATA_FRAME_HEADER_2 == aByte and COM_CONFIG.DATA_FRAME_HEADER_1 == self._lastByte ):
			self._beginFrame = True
			self._receiveCount = 2;
			self.initFrame()
			# print("<<< FRAME BEGIN >>>")
			if callable(self.onFrameBegin):
				self.onFrameBegin()

		if ( 3 == self._receiveCount ): self._frameLen = aByte

		# 记录字节数据
		self.dataFrame.append(aByte)


		if ( self._receiveCount - 3 == self._frameLen ):

			if callable(self.onBeforeFrameVerifyCRC):
				self.onBeforeFrameVerifyCRC()

			# 数据帧接收完毕，检测数据帧，如果正确马上进行解析。之后清空
			isOK = self.checkDataFrames(True)
			if (isOK == COM_CHK_ST.DF_CHECK_OK):
				# 传递数据成功接收并且解析完毕消息
				# print("--- FRME OK ---")
				if callable(self.onFrameReceived):
					self.onFrameReceived()
			else:
				# 数据帧错误，通常丢弃
				# print("--- FRME ERROR ---", isOK)
				if callable(self.onFrameErr):
					self.onFrameErr(isOK)

			# 清空数据帧，等待接收新的数据
			self._receiveCount = 0;
			self._beginFrame = False;
			self._lastByte = 0x00;
			self._frameLen = 0x00;
			self.clearBuffer()

		self._lastByte = aByte

		# 数据帧长度不能超过 256字节，超过就自动清空
		if (self._receiveCount > self._maxFrameLen):
			self._receiveCount = 0;
			self._beginFrame = False;
			self._lastByte = 0x00;
			self._frameLen = 0x00;
			self.clearBuffer()

			# print("--- FRME LEN OVER ---")
			if callable(self.onFrameErr):
				self.onFrameErr(COM_CHK_ST.DF_CHECK_ERROR_FRAME_LENGTH_OVER)

