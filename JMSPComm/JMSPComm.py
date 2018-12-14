# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2018 Kunpeng Zhang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# #########################################################
#	Small Pack Comm
#
#	Kunpeng Zhang
#	2018.10.25
#	
#	v1.0
#

import struct
from JMSPComm_1_0_0 import JMSPComm_config as COM_CONFIG
from JMSPComm_1_0_0 import JMSPCommDataFrameCheckStatus as COM_CHK_ST
import JMSPCRC8

# 通讯协议版本
LASTE_COMM_MAIN_VER = COM_CONFIG.COMM_MAIN_VER
# 通讯协议数据格式版本
LASTE_COMM_DATA_VER = COM_CONFIG.COMM_DATA_VER

class JMSPComm:

	# 数据缓冲区 (bytearray)
	dataFrame = None

	# 启用CRC校验
	enabledCRC = True

	# 通讯协议版本 - 解析数据帧，该数值由解析函数赋值。要生成数据帧则设置该数值。
	comDataVer = None
	# 数据协议版本 - 解析数据帧，该数值由解析函数赋值。要生成数据帧则设置该数值。
	comMainVer = None

	# 数据帧中的 CRC 校验码
	dataCRC = None

	def __init__(self):
		self.dataFrame = bytearray()


	def checkDataFrames( self, parseData = False ):
		"""!
		/~english
		Check if the data frame is correct.

		@param parseData: if the data frame is correct then parsed the data  [ False(default) | True ] 
		@return: boolean. return YES to indicate the correct data frame, otherwise the data frame error

		/~chinese
		检查数据帧是否正确，返回 YES 代表是正确数据帧，否则 数据帧错误

		@param parseData: 是否解析数据－如果数据帧正确才执行 [ False(默认) | True ]
		@return: boolean. 返回 YES 代表是正确数据帧，否则 数据帧错误
		"""

		# 如果数据帧总长度小于 7 字节说明数据帧不完整
		if len(self.dataFrame) < COM_CONFIG.DATA_FRAME_MIN_LENGTH:
			return COM_CHK_ST.DF_CHECK_ERROR_FRAME_TOTAL_LENGTH

		# 检查数据帧头
		header = bytearray(self.dataFrame[COM_CONFIG.DATA_POS_HEADER : COM_CONFIG.DATA_LEN_HEADER])
		hdv = struct.unpack(">H", header)
		# 数据帧头不正确
		if ( hdv[0] != COM_CONFIG.DATA_FRAME_HEADER ):
			return COM_CHK_ST.DF_CHECK_ERROR_FRAME_HEADER;

		# 检查数据帧长度
		frameLength = self.dataFrame[COM_CONFIG.DATA_POS_FRAME_LENGTH]
		if (len(self.dataFrame) != frameLength + 3 ):
			# 数据帧长超过预定义长度
			return COM_CHK_ST.DF_CHECK_ERROR_DATA_LENGTH;

		# 检查数据帧 CRC
		if self.enabledCRC == True:
			crc = self.dataFrame[frameLength + COM_CONFIG.DATA_LEN_HEADER]
			d_crc = JMSPCRC8.crc8FromBytes(self.dataFrame, COM_CONFIG.DATA_POS_FRAME_LENGTH, frameLength);
			if crc != d_crc:
				return COM_CHK_ST.DF_CHECK_ERROR_CRC
			self.dataCRC = crc

		# Update property of SPComm
		self.comMainVer = self.dataFrame[COM_CONFIG.DATA_POS_MAIN_VERSION]
		self.comDataVer = self.dataFrame[COM_CONFIG.DATA_POS_DATA_VERSION]
		if parseData == True:
			self.parseData( (COM_CONFIG.DATA_POS_DATA, frameLength - 3) )

		return COM_CHK_ST.DF_CHECK_OK;


	def parseData(self, dataRange):
		"""!
		/~english
		Analyze data - subclass succession to achieve specific data analysis

		/~chinese
		解析数据-子类继成实现具体数据的解析
		"""
		pass

	def clearBuffer(self):
		self.dataFrame = None
		self.dataFrame = bytearray()

	def addBuffer( self, aBytes ):
		"""!
		/~english
		Add data into buffer

		@param aBytes, is int or array of int

		/~chinese
		增加数据到缓存

		@param aBytes, 整数或者整数数组
		"""
		if (type(aBytes) == int):
			self.dataFrame.append(aBytes)
		else:
			for aByte in aBytes:
				self.dataFrame.append(aByte)


	def getFrameLength(self):
		"""!
		/~english
		Data frame length = version + data area (exclude: CRC)
		@return: integer.

		/~chinese
		数据帧长度 = 版本 + 数据区 (exclude: CRC)
		@return: integer.
		"""
		return self.dataFrame[COM_CONFIG.DATA_POS_FRAME_LENGTH]


	def getCRCRange(self, frameLength ):
		"""!
		/~english
		Get the location of the CRC data
		@return: (loc, len).

		/~chinese
		获取 CRC 数据的位置

		@return: (loc, len).

		"""
		return (frameLength + COM_CONFIG.DATA_LEN_HEADER - 1, 1);
