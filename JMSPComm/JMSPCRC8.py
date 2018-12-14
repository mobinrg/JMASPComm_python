# -*- coding: utf-8 -*-
#
#  lbcrc8.c
#  Simulator LBC100
#
#  Created by 张鲲鹏 on 2014-2-10.
#  Copyright (c) 2014年 JungleMetal Inc. All rights reserved.
#
#	Kunpeng Zhang
#	2018.10.26 modified for Python
#

def crc8FromByte( inByte, prevCRC ):
	crc = prevCRC
	for i in range(0,8):
		if ( ((inByte & 0x01) ^ (crc & 0x01)) == 0 ):
			crc >>= 1
		else:
			# 做(1),(2); (1)=0,则CRC向高位移1位

			# (1)=1,则异或18
			crc = crc ^ 0x18
			crc >>= 1
			# 置CRC.0为1
			crc |= 0x80

		inByte >>= 1

	return crc


def crc8FromBytes( aBytes, loc = 0, len = None ):
	"""!
	Calc bytes crc
	@param aBytes: a bytes list or tuple
	@param loc: start index
	@param len: calc length (default: None, mean is calc all data )

	@return byte
	"""
	crc = 0x00

	if len == None:
		for bt in aBytes:
			crc = crc8FromByte(bt, crc)
			# print(bt, crc)
	else:
		for i in range(loc, loc+len):
			crc = crc8FromByte(aBytes[i], crc)
			# print(i, aBytes[i], crc)

	return crc
