#!/usr/bin/env python
# -*-coding:utf-8 -*-

#Author:wuyi

from base.method import Requests
from utils.operationExcel import OperationExcel,ExcelVariable
from common.public import *
import pytest
import json
import allure
import subprocess

excel = OperationExcel()
obj = Requests()

@pytest.mark.parametrize('datas',excel.runs())
def test_login_book(datas):
	# 对请求参数做反序列化的处理
	params = datas[ExcelVariable.params]
	if len(str(params).strip()) == 0:
		pass
	elif len(str(params).strip()) >= 0:
		params = json.loads(params)
	
	# 对请求头做反序列化的处理
	headers = datas[ExcelVariable.headers]
	if len(str(headers).strip()) == 0:
		pass
	elif len(str(headers).strip()) >= 0:
		headers = json.loads(headers)
	
	'''
		1、先获取到所有前置测试点的测试用例
		2、执行前置测试点
		3、获取它的结果信息
		4、拿它的结果信息替换对应测试点的变量
		'''
	
	# 执行前置条件关联的测试点
	r = obj.post(url=excel.case_prev(datas[ExcelVariable.casePre])[ExcelVariable.caseUrl],
	             json=json.loads(excel.case_prev(datas[ExcelVariable.casePre])[ExcelVariable.params]))
	
	# 替换被关联测试点中请求头信息的变量
	headers = excel.prevHeaders(r.json()['access_token'])
	
	# 断言
	def case_assert_result(r):
		assert r.status_code == int(datas[ExcelVariable.status_code])
		assert datas[ExcelVariable.expect] in json.dumps(r.json(), ensure_ascii=False)
	
	def getUrl():
		url = datas[ExcelVariable.caseUrl]
		return url
	
	def setUrl():
		url = str(datas[ExcelVariable.caseUrl]).replace('{bookID}',readContent())
		return url
	
	if datas[ExcelVariable.method] == 'get':
		if '/books' in datas[ExcelVariable.caseUrl]:
			r = obj.get(url=getUrl(),
			            headers=headers)
		else:
			r = obj.get(url=setUrl(),
			            headers=headers)
		case_assert_result(r=r)
		
	elif datas[ExcelVariable.method] == 'post':
		r = obj.post(url=getUrl(),
		             json=params,
		             headers=headers)
		writeContent(content=str(r.json()[0]['datas']['id']))
		case_assert_result(r=r)
	
	elif datas[ExcelVariable.method] == 'put':
		r = obj.put(url=setUrl(),
		            json=params,
		            headers=headers)
		case_assert_result(r=r)
	
	elif datas[ExcelVariable.method] == 'delete':
		r = obj.delete(url=setUrl(),
		               headers=headers)
		case_assert_result(r=r)
		
	allure.title("API测试报告")
if __name__ == '__main__':
	pytest.main(["-s","-v","test_login_token_book.py","--alluredir","./report/result"])
	subprocess.call('allure generate report/result/ -o report/html --clean',shell=True)
	subprocess.call('allure open -h 127.0.0.1 -p 8088 ./report/html',shell=True)