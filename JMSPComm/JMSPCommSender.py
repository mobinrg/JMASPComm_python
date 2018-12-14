# -*- coding: utf-8 -*-
#
#	JMSPCommSender
#
# Usage:
#
#   myComm = new JMSPCommSender()
#
#
#	Kunpeng Zhang
#	2018.10.25
#	
#	v1.0
#

import JMSPCRC8
from JMSPComm_1_0_0 import JMSPComm_config as COM_CONFIG
from JMSPComm_1_0_0 import JMSPCommDataFrameCheckStatus as COM_CHK_ST
from JMSPComm import JMSPComm

class JMSPCommSender(JMSPComm):

	def initFrame(self):
		self.clearBuffer()
		self.dataFrame.append(COM_CONFIG.DATA_FRAME_HEADER_1)
		self.dataFrame.append(COM_CONFIG.DATA_FRAME_HEADER_2)
		# 初始化默认桢长
		self.dataFrame.append(0x00)
		self.dataFrame.append(self.comMainVer)
		self.dataFrame.append(self.comDataVer)

	def buildCommPack(self, callbackAlready = None):
		"""!
		/~english
		Calculate the CRC of the data frame (used to generate the communication protocol). When the send buffer is ready, call the CRC of the calculated data.
		@param callbackAlready. callback func for data already.

		/~chinese
		计算数据帧的 CRC 校验码（用于生成通讯协议）当发送缓存准备好以后调用计算数据的 CRC, 完成后即可发送
		@param callbackAlready. 数据准备好回调函数
		"""
		# 计算数据帧长
		fl = len(self.dataFrame) - COM_CONFIG.DATA_LEN_HEADER
		# 写入数据帧长度
		self.dataFrame[COM_CONFIG.DATA_POS_FRAME_LENGTH] = fl

		# ------- 计算CRC --------------
		# 取得需要计算 CRC 校验码的数据区数据
		# CRC 范围 = 数据帧长度 + 版本 + 数据区
		# 计算出数据CRC码

		if self.enabledCRC:
			dCRC = 0x00
			dCRC = JMSPCRC8.crc8FromBytes(self.dataFrame, COM_CONFIG.DATA_POS_FRAME_LENGTH, fl)
			self.dataFrame.append(dCRC)
			self.dataCRC = dCRC
		else:
			self.dataCRC = None

		if (callbackAlready != None): callbackAlready
		return True
