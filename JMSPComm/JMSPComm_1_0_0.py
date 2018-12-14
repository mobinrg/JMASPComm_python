# -*- coding: utf-8 -*-
#
# 数据帧格式
#
# +--------+--------------+-------------+-----------+---------+
# | 0x023C | FRAME LENGTH | COM VERSION |   DATA    | CRC     |
# +--------+--------------+-------------+-----------+---------+
# | 2bytes | 1byte        | 2bytes      | 1~N Bytes | 1 Byte  |
# +--------+--------------+-------------+-----------+---------+
#
# +------------------------------------+
# |         DATA (N Bytes)             |
# +------------------------------------+
# | COMMAND | PARAM LENGTH | PARAMS    |
# |  1byte  | 1 byte       | N-2 Bytes |
#
#

from enum import Enum
class JMSPCommDataFrameCheckStatus(Enum):
	# 数据帧OK
	DF_CHECK_OK = 0
	# 数据帧总长度错误
	DF_CHECK_ERROR_FRAME_TOTAL_LENGTH = 100
	# 数据帧头错误
	DF_CHECK_ERROR_FRAME_HEADER = 102
	# 数据帧中数据区长度错误
	DF_CHECK_ERROR_DATA_LENGTH 	= 103
	# CRC校验错误
	DF_CHECK_ERROR_CRC			= 104
	DF_CHECK_ERROR_FRAME_LENGTH_OVER = 105


class JMSPComm_config:
	#
	# 通讯协议版本，采用 BCD 编码
	#
	COMM_MAIN_VER			= 0x10
	COMM_DATA_VER			= 0x10

	DATA_FRAME_MIN_LENGTH	= 7

	DATA_FRAME_HEADER 		= 0x023C
	DATA_FRAME_HEADER_1		= 0x02
	DATA_FRAME_HEADER_2		= 0x3C

	#数据帧头
	DATA_POS_HEADER			= 0
	DATA_LEN_HEADER			= 2

	#数据帧长
	DATA_POS_FRAME_LENGTH	= 2
	DATA_LEN_FRAME_LENGTH	= 1

	#通讯协议版本号
	DATA_POS_MAIN_VERSION	= 3
	DATA_LEN_MAIN_VERSION	= 1

	#通讯协议数据格式版本号
	DATA_POS_DATA_VERSION	= 4
	DATA_LEN_DATA_VERSION	= 1

	#通讯协议数据区 = 指令 + 指令参数长度 + 参数 [+ CRC]
	DATA_POS_DATA 			= 5

	#指令
	DATA_POS_COMMAND 		= 5
	DATA_LEN_COMMAND 		= 1

	#指令参数长度
	DATA_POS_COMMAND_PARAM	= 6
	DATA_LEN_COMMAND_PARAM	= 1

	#指令数据
	DATA_POS_COMMAND_DATA	= 7

	#CRC 长度
	DATA_LEN_CRC			= 1
