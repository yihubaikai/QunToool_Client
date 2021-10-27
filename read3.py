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

def SaveLog(filepath, text, isNewfile=False):
	if(isNewfile==True and os.path.isfile(filepath) and os.path.exists(filepath)):
		os.remove(filepath)
	with open(filepath,"a",encoding='utf-8') as f:
	#with open(filepath,"a") as f:
		f.write(text)
		#f.flush()

def StrToTimeCuo(a1):
	timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
 
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return timeStamp
def gettimecuo():
	mtimecuo = str(int(round(time.time() * 1000)))
	return mtimecuo
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



class MSGCLASS(object):
	"""消息群处理函数"""
	cur_path     = ""
	FilterArr    = []
	DIRECTORYS   = []

	def __init__(self):
		self.cur_path = os.getcwd() + "\\"
		super(MSGCLASS, self).__init__()


	#加载过滤文件
	def Load_Dict(self):
		fDict = self.cur_path + "\\dict\\filterword.txt"
		with open(fDict, 'r', encoding='utf-8') as f:
			for txt in f:
				txt = txt.replace("\n", "")
				txt = txt.replace("\r", "")
				if(len(txt)>0):
					self.FilterArr.append(txt)
		return self.FilterArr

	#判断过滤
	def CheckWorld(self,fWord):
		for x in self.FilterArr:
			if(fWord.find(x) != -1):
				return 1
		return 0

	#获取文件列表
	def Get_DirS(self):
		rootDir = self.cur_path + "\\source\\"
		self.DIRECTORYS.clear()
		items = os.listdir(rootDir)
		for x in items:
			self.DIRECTORYS.append(rootDir + x)
		'''for root,dirs,files in os.walk(rootDir):
			for file in files: #先遍历文件
				print(os.path.join(root,file))
			for dir in dirs:  #再遍历文件夹
				bianLi(dir)'''
		return self.DIRECTORYS

	def Read_MSG(self, rPath):
		if( False == os.path.exists(rPath) ):
			return
		cstruct = {"num": 1, "txt":""}
		cnode = cstruct
		data = dict()
		today = time.strftime("%Y-%m-%d") #今天
		yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d") 
		yesterday2 = (date.today() + timedelta(days = -2)).strftime("%Y-%m-%d") 
		yesterday3 = (date.today() + timedelta(days = -3)).strftime("%Y-%m-%d") 
		#print(today,yesterday)
		print("*" * 60)
		with open(rPath, 'r', encoding='utf-8') as f:
			strc = ""
			strt = ""
			strmd5 = ""
			iCount = 0
			iValid = 0
			for txt in f:
				if is_valid_date(txt[:19])==0:
					iValid = 0
				print(txt)
				if( txt.find(today) != -1 or txt.find(yesterday) != -1 or txt.find(yesterday2) != -1 or txt.find(yesterday3) != -1 ): #表示找到了日期是当天
				#if( txt.find(today) != -1 or  txt.find(yesterday) != -1): #表示找到了日期是当天
					txt2 = txt
					txt2 = txt2.replace("\n", "")
					txt2 = txt2.replace("\r", "")

					#保存记录
					if len(strt)>0:
						print(strt)
						print(strc[:20])

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

		iCount = 0
		mStr = "<table width=\"100%\" border=1 cellspacing=0 cellpadding=0><tr><td>编号</td><td>出现次数</td> <td>QQ</td>    <td>内容</td>  </tr>"
		for tmpnode in data:
			if(self.CheckWorld(data[tmpnode]["content"])>0):
				print("跳过:" , data[tmpnode]["content"][:20])
				continue
			if(self.CheckWorld(data[tmpnode]["title"])>0):
				print("跳过:" , data[tmpnode]["content"][:20])
				continue
			if(len(data[tmpnode]["content"])>150):
				continue
			if(len(data[tmpnode]["content"])<3):
				continue
			if(data[tmpnode]["num"]>3):
				continue
			iCount = iCount + 1
			tt = data[tmpnode]["content"]
			if( tt.find("谁") != -1 or  tt.find("有没有") != -1  or  tt.find("价格") != -1 or  tt.find("多少钱") != -1 or  tt.find("来一") != -1  or  tt.find("带价") != -1 or  tt.find("接单") != -1):
				mStr = mStr+"<tr><td>"+str(iCount)+"</td><td>"+str(data[tmpnode]["num"])+"</td><td>"+data[tmpnode]["title"]+"</td><td><font color=red>"+data[tmpnode]["content"]+"</font></td></tr>\n"
			else:
				#mStr = mStr+"<tr><td>"+str(iCount)+"</td><td>"+str(data[tmpnode]["num"])+"</td><td>"+data[tmpnode]["title"]+"</td><td>"+data[tmpnode]["content"]+"</td></tr>\n"
				pass
		mStr = mStr + "</table>"
		fpath = self.cur_path + "\\out\\"+str(gettimecuo())+"-all.Table.html"
		SaveLog(fpath,mStr,True)





def main():
	cli = MSGCLASS()
	cli.Load_Dict() #获取过滤列表
	arr = cli.Get_DirS()  #获取消息列表
	for x in arr:
		cli.Read_MSG(x)
	os.system('explorer ' + os.getcwd() + "\\out")
	print("完成了,敲回车退出")
	input()

	



if __name__ == '__main__':
	main()