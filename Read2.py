import requests,json
import webbrowser
import time,random
import win32clipboard as w
import win32con
import win32api,json
import win32gui
import win32ui
import win32api
import win32con,os
from datetime import datetime
import psutil
#from pymouse import PyMouse
#dt=datetime.now() #创建一个datetime类对象
#print dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.month

#建立全局变量

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def GetPid():
	pids = psutil.pids()
	p = psutil.Process(pid)
	print("pid-%d,pname-%s" %(pid,p.name()))


def getText():#读取剪切板
	try:
		w.OpenClipboard()  
		d = w.GetClipboardData(win32con.CF_TEXT)  
		w.CloseClipboard()  
		if(len(d)>0):
			print(len(d))
			s = d.decode("gb18030")
			print(s)
			return s
	except Exception as e:
		raise e  
	return ""

def setText(aString):#写入剪切板  
    w.OpenClipboard()  
    w.EmptyClipboard()  
    w.SetClipboardText(aString)  
    w.CloseClipboard()  
#模拟鼠标点击
def mouse_click(x, y):
	win32api.SetCursorPos([x, y])
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def copytext():
	setText("")
	#mouse_click(880,700)
	#time.sleep(1)
	#mouse_click(880,700)
	#time.sleep(1)
	win32api.keybd_event(9,0,0,0)  #TAB的键位码
	win32api.keybd_event(9,0,win32con.KEYEVENTF_KEYUP,0) 
	time.sleep(1)
	win32api.keybd_event(17,0,0,0)  #ctrl的键位码是17  
	win32api.keybd_event(65,0,0,0)  #A的键位码是86  
	win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
	win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)  
	time.sleep(1)
	Key_Ctrl_c()
	time.sleep(1)
	r= getText()
	Key_Alt_s()
	#mouse_click(880,700)
	return r

def Key_Ctrl_v():
	win32api.keybd_event(17,0,0,0)  #ctrl的键位码是17  
	win32api.keybd_event(86,0,0,0)#v的键位码是86  
	win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
	win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)  
	#win32api.keybd_event(13,0,0,0)#Enter的键位码是13  
	#win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
def Key_Ctrl_c():
	win32api.keybd_event(17,0,0,0)  #ctrl的键位码是17  
	win32api.keybd_event(67,0,0,0)#v的键位码是86  
	win32api.keybd_event(67,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
	win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)  
	#win32api.keybd_event(13,0,0,0)#Enter的键位码是13  
	#win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
def Key_Alt_s():
	win32api.keybd_event(18,0,0,0)  #ctrl的键位码是17  
	win32api.keybd_event(83,0,0,0)#v的键位码是86  
	win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
	win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)  


def Key_Alt_c():
	win32api.keybd_event(18,0,0,0)  #ctrl的键位码是17  
	win32api.keybd_event(67,0,0,0)#v的键位码是86  
	win32api.keybd_event(67,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
	win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
	win32api.keybd_event(32,0,0,0)  #ctrl的键位码是17 
	win32api.keybd_event(32,0,win32con.KEYEVENTF_KEYUP,0) 


def Save_Log(filename, text):
	with open(filename,'a',encoding='utf-8') as f:
		f.write(text)

#获取链接:点击链接加入群聊【一带一路资料群】：https://jq.qq.com/?_wv=1027&k=5ui5cYI
#点击链接加入群聊【wap站长变现交流群】：https://jq.qq.com/?_wv=1027&k=5UtybQp
def GetUrl(url):
	ret = {"state":1}
	#url = "https://jq.qq.com/?_wv=1027&k=5ui5cYI"
	#url = "https://jq.qq.com/?_wv=1027&k=5UtybQp"
	print(url)
	try:
		r = requests.get(url)
		txt = r.text

		#print(r.text)
		#查找群ID:"var rawuin ="
		startflag = "var rawuin ="
		endflag   = ";"
		iStart = txt.find(startflag)
		iEnd   = txt.find(endflag,iStart)
		qunid  = ""
		if(iEnd>iStart) and (iStart!=-1) and (iEnd!=-1):
			qunid  = txt[iStart+13:iEnd]
			print(iStart, iEnd,"群ID:", qunid)
			ret["state"] = 0
			ret["qunid"] = qunid
		else:
			print("获取群ID出错")


		#查找群链接:"var rawuin ="
		startflag = "tencent://groupwpa"
		endflag   = "\";"
		iStart    = txt.find(startflag)
		iEnd      = txt.find(endflag,iStart)
		qunurl    = ""
		if(iEnd>iStart) and (iStart!=-1) and (iEnd!=-1):
			qunurl    = txt[iStart:iEnd]
			#print(iStart, iEnd,"群链接:", qunurl)
			ret["qunurl"] = qunurl
			if(ret["state"]!=0):
				ret["state"] = 2
			else:
				ret["state"] = 0
		else:
			print("获取群链接")



	except Exception as e:
		raise e
	return ret


#打开qq群界面
def OepnQUN_ui(ret):
	#print("正在打开群:", ret["qunid"])
	webbrowser.open( ret["qunurl"],new=2,autoraise=True)
	time.sleep(1)

#输入文字
def inputText(text):
	setText(text)
	Key_Ctrl_v()



 

#读取配置
#点击链接加入群聊【海外大带宽站群服务器】：https://jq.qq.com/?_wv=1027&k=5aUMYPA,1
QunList = {}
Adword  = []
Hellword= []
fileterarr = []

#发送文字
def SendMessage3(ret):
	i_find = 0
	for k in fileterarr:
		if(ret["qunid"] == k):
			i_find = 1
			break
	if(i_find == 1):
		print("被屏蔽的群:", ret["qunid"])	
		return
	print("正在打开群:", ret["qunid"])
	OepnQUN_ui(ret)
	time.sleep(2)
	r = copytext()
	if(r.find("胡勇") != -1):
		
		print("关闭对话框:ALT+C")
		Key_Alt_c()
		print("\n\n")
		print("x"*50)
		print("QUN:" + ret["qunid"] )
		print("QUNlink:" + ret["qunlink"] )
		print("有我发得消息, 不发送")
		print("x"*50)
		print("\n\n")
		return

	#输入文字
	print("输入文字:", ret["adword"])
	inputText(ret["adword"])
	#time.sleep(random.randint(1,8))

	#发送文字
	print("发送文字:ALT+S")
	Key_Alt_s()
	time.sleep(3)

	#关闭对话框
	print("关闭对话框:ALT+C")
	Key_Alt_c()
	print("\n\n")
	print("*"*50)
	print("QUN:" + ret["qunid"] )
	print("QUNlink:" + ret["qunlink"] )
	print("发送广告和文字")
	print("*"*50)
	print("\n\n")


def ReadQunList():
	QunList.clear()
	filename = 'list.txt'
	with open(filename, 'r') as f:
		while True:
			lines = f.readline() # 整行读取数据
			if not lines:
				break
			if(len(lines)<10):
				#print("数据错误:",lines)
				continue
			#print(lines)
			iStart = lines.find("https://")
			iEnd   = lines.find(",")
			if(iStart==-1) or (iEnd==-1) or (iStart>iEnd):
				#print("数据错误:",lines)
				continue

			url = lines[iStart:iEnd]
			#print(url)
			iFind = lines.find(",1")
			if(iFind >10):
				QunList[url] = 1
				#print("纯广告:", url)
				continue

			iFind = lines.find(",0")
			if(iFind>10):
				QunList[url] = 0
				#print("可表情:", url)
				continue
			else:
				print("数据错误2:",lines)
				continue
	#读取数据放入qunlist中
	#print(QunList)
	iCount = 0
	for x in QunList:
		#print(QunList[x])
		iCount = iCount + 1
	print("获取群链接:", iCount)

#读取广告
def ReadAdword():
	Adword.clear()
	filename = 'adword.txt'
	with open(filename, 'r') as f:
		while True:
			lines = f.readline() # 整行读取数据
			if not lines:
				break
			if(len(lines)<10):
				#print("数据错误:",lines)
				continue
			js = json.loads(lines)
			#print(js[0])
			Adword.append(js[0])
	print("广告:",len(Adword))


#读取招呼词语
def ReadHelloword():
	Hellword.clear()
	filename = 'hellword.txt'
	with open(filename, 'r') as f:
		while True:
			lines = f.readline() # 整行读取数据
			if not lines:
				break
			if(len(lines)<2):
				continue
			#print(lines)
			Hellword.append(lines)
	print("打招呼:",len(Hellword))

def ReadFilter():
	fileterarr.clear()
	filename = 'filter.txt'
	with open(filename, 'r') as f:
		while True:
			lines = f.readline() # 整行读取数据
			if not lines:
				break
			if(len(lines)<5):
				#print("数据错误:",lines)
				continue
			lines = lines.replace("\r", "")
			lines = lines.replace("\n","")
			fileterarr.append(lines)
	print("过滤:",len(fileterarr))

def SendOnce():
	dt=datetime.now() #创建一个datetime类对象
	print(dt.strftime( '%Y-%m-%d %H:%M:%S' ))
	for x in QunList:
		#print(x,QunList[x])
		ret = GetUrl(x)
		if(ret["state"] != 0):
			print("获取数据错误")
			continue
		ret["qunlink"] = x
		tmp = json.dumps(ret) +"\n"
		Save_Log("out_result.txt", tmp)
		if( QunList[x]==0 ):#表示只能发表情	
			iLen  = len(Hellword)
			index = random.randint(0,(len(Hellword)-1) )
			ret["adword"] = Hellword[index]
			print("表情:",index)
			continue
		else:
			iLen  = len(Adword)
			index = random.randint(0,(len(Adword)-1) )
			ret["adword"] = Adword[index] #"点击链接加入群聊【IDC香港服务器租用】https://jq.qq.com/?_wv=1027&k=5k4j534"
			print("广告:",index)
			

		#发送广告和文字
		SendMessage3(ret)
		#print(ret)


#控制流程
def AutoMain():
	dt=datetime.now() #创建一个datetime类对象
	#print(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.month)
	#print('时间：(%Y-%m-%d %H:%M:%S %f): ' , dt.strftime( '%Y-%m-%d %H:%M:%S %f' )) and (dt.second==10)
	#print(dt.weekday())
	print(dt.strftime( '%Y-%m-%d %H:%M:%S' ))
	if ( (dt.hour==6) or (dt.hour==10) or (dt.hour==12) or (dt.hour==15) or (dt.hour==23) ) and (dt.minute==26):
		for x in QunList:
			#print(x,QunList[x])
			ret = GetUrl(x)
			if( QunList[x]==0 ):#表示只能发表情
				if(dt.weekday()==5):#周六
					if(dt.hour != 10) or (dt.hour != 23): #只允许10,23点发一次
						continue

				if(dt.weekday()==6):#周天
					if(dt.hour != 14): #只允许14点发一次
						continue
				
				iLen  = len(Hellword)
				index = random.randint(0,(len(Hellword)-1) )
				ret["adword"] = Hellword[index]
				print("表情:",index)
			else:
				iLen  = len(Adword)
				index = random.randint(0,(len(Adword)-1) )
				ret["adword"] = Adword[index]
				print("广告:",index)

			#发送广告和文字
			SendMessage3(ret)

if __name__ == '__main__':
	ReadQunList()
	ReadAdword()
	ReadHelloword()
	ReadFilter()
	os.system("cmd.exe/c mode con cols=56 lines=30")
	#time.sleep(3)
	#ra = copytext()
	#print(ra)
	#if(ra.find("胡勇") == -1):
	#	print("没有我发得消息")
	#else:
	#	print("有我发得消息")
	

	#执行一次鼠标移动
	#mouse_click(880,700)

	#执行一次发送操作		

	#sendNow = input("是否立即执行一次发送(y/n):")
	#print(sendNow)

	#if(sendNow == "y") or (sendNow == "Y"):
	#	print("准备立即发送")
	#SendOnce()
	#else:
	#	print("稍后发送")

	
	#while True:
	SendOnce()
	#getText()
	time.sleep(50)
	print("Process is Over!!!")
	#main()
	#SendMessage()
	#SendMessage2()
