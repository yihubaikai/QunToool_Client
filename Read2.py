# -*- coding: utf-8 -*- 
import os
import codecs
import hashlib
import time,datetime
import re
import json
import copy

from datetime import datetime, date, timedelta


def CMD5(txt):
	if(len(txt)==0):
		return ''
	m = hashlib.md5()
	b = txt.encode(encoding='utf-8')
	m.update(b)
	str_md5 = m.hexdigest()
	return str_md5

def Save_Log(filename, text):
	with open(filename,'a',encoding='utf-8') as f:
		f.write(text)

def StrToTimeCuo(a1):
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
 
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp


FilterArr = []
def FilterWord(aWord):
	if(len(FilterArr)==0):
		with open('filterword.txt', 'r', encoding='utf-8') as f:
			for txt in f:
				txt = txt.replace("\n", "")
				txt = txt.replace("\r", "")
				if(len(txt)>0):
					#print(txt)
					FilterArr.append(txt)
	#注意了	
	for x in FilterArr:
		if(aWord.find(x) != -1):
			#print("FilterWord:", x)
			return 1
	return 0

def is_valid_date(strdate):
	'''判断是否是一个有效的日期字符串'''
	try:
		if ":" in strdate:
			time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
		else:
			time.strptime(strdate, "%Y-%m-%d")
		return 0
	except:
		return 1


def main():
	cstruct = {"num": 1, "txt":""}
	cnode = cstruct
	data = dict()
	today = time.strftime("%Y-%m-%d") #今天
	yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d") 
	print(today,yesterday)
	print("*" * 60)
	with open('广告群.txt', 'r', encoding='utf-8') as f:
		strc = ""
		strt = ""
		strmd5 = ""
		iCount = 0
		iValid = 0
		for txt in f:
			if is_valid_date(txt[:19])==0:
				iValid = 0
			
			if( txt.find(today) != -1 or txt.find(yesterday) != -1 ): #表示找到了日期是当天
				txt2 = txt
				txt2 = txt2.replace("\n", "")
				txt2 = txt2.replace("\r", "")

				#保存记录
				if len(strt)>0:
					print(strt)
					print(strc)

				#print(len(strt))
				if( len(strt)>0):
					md5 = CMD5(strc)
					if md5 not in data:
						cnode = {"num":1, "title":strt,"content":strc}
						data[md5]=cnode
						#print("不存在")
					else:
						cnode = {}
						cnode["num"]  = int(data[md5]["num"]) + 1
						cnode["title"]  = data[md5]["title"]
						cnode["content"]  = data[md5]["content"]
						data[md5] = cnode
						#print("存在:",md5)

				strt  = txt2
				strc  =  ""
				iValid = 1
			else:
				if(iValid == 1):
					strc = strc + txt

	#print(json.dumps(data,indent=4))
	#Save_Log("all.json.txt",json.dumps(data,indent=4))
	iCount = 0
	mStr = "<table width=\"100%\" border=1 cellspacing=0 cellpadding=0><tr><td>编号</td><td>出现次数</td> <td>QQ</td>    <td>内容</td>  </tr>"
	for tmpnode in data:
		if(FilterWord(data[tmpnode]["content"])>0):
			print("跳过:" , data[tmpnode]["content"], end='')
			continue
		if(len(data[tmpnode]["content"])>150):
			continue
		if(len(data[tmpnode]["content"])<3):
			continue
		iCount = iCount + 1
		mStr = mStr+"<tr><td>"+str(iCount)+"</td><td>"+str(data[tmpnode]["num"])+"</td><td>"+data[tmpnode]["title"]+"</td><td>"+data[tmpnode]["content"]+"</td></tr>\n"
	mStr = mStr + "</table>"
	fpath = "all.Table.html"
	if os.path.exists(fpath):
		os.remove(fpath)
	Save_Log(fpath,mStr)



def main2():
	cnode = {"num":1}
	cnode2 = {"num":2}
	cnode3 = {"num":3}


	cdata = dict()
	cdata["a"] = cnode
	cdata["b"] = cnode2
	cdata["c"] = cnode3
	t = {}
	t["num"] = cdata["c"]["num"] + 1
	cdata["c"] = t
	print(json.dumps(cdata,indent=4))
def main3():
	strdate = "2020-04-22"
	if ":" in strdate:
		time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
	else:
		time.strptime(strdate, "%Y-%m-%d")
	return 0
	
if __name__ == '__main__':
	main()
	#print(FilterWord("213123123123加2入本群123"))