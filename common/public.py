#!/usr/bin/env python
# -*-coding:utf-8 -*-

#Author:wuyi

import os

# base_url = os.path.dirname(os.path.dirname(__file__))
# print(os.path.join(base_url,'data','login.yaml'))

def filePath(fileDir='data',fileName='login.yaml'):
	'''
	:param fileDir: 目录
	:param fileName: 文件的名称
	:return:
	'''
	return os.path.join(
		os.path.dirname(os.path.dirname(__file__)),fileDir,fileName)

def writeContent(content):
	with open(filePath(fileDir='data',fileName='bookID'),'w') as f:
		f.write(str(content))

def readContent():
	with open(filePath(fileDir='data',fileName='bookID'),'r') as f:
		return f.read()