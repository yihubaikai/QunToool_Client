'''
 脚本名称：自动打招呼软件

'''
import requests,json
import webbrowser
import time,random
import win32clipboard as w
import win32con,win32com.client 
import win32api,json
import win32gui
import win32ui
import win32api
import win32con,os,subprocess,codecs
from datetime import datetime
from winreg import *
import psutil
import sys
import threading


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
	except:
		pass  
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
	time.sleep(1)
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
	time.sleep(0.1)

def Key_Alt_c2():
	win32api.keybd_event(18,0,0,0)  #ctrl的键位码是17  
	win32api.keybd_event(67,0,0,0)#v的键位码是86  
	win32api.keybd_event(67,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
	win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
	time.sleep(0.1)

	
def Save_Log(filename, text):
	with open(filename,'a',encoding='utf-8') as f:
		f.write(text)

#输入文字
def inputText(text):
	setText(text)
	Key_Ctrl_v()

#获取快捷方式路径
def Get_FullPath(pathx):
	ret = {"state":1, "msg":"不是标准的QQ好友格式"}
	try:
		shell = win32com.client.Dispatch("WScript.Shell")
		shortcut = shell.CreateShortCut(pathx)
		#print(shortcut.Targetpath)
		#print(shortcut.arguments )
		#print(shortcut.fullname )
		s = shortcut.arguments
		if(s.find("uin") != -1  and (s.find("quicklunch") != -1) ):
			#获取uin
			#获取启动参数
			#获取快捷方式名称
			t = s.split(":")
			t1 = t[1].replace(" /quicklunch", "")
			ret["uin"] = t1
			ret["arg"] = t[2]
			p = pathx.split("\\")
			#print(s)
			for x in p:
				if(x.find(".lnk") != -1):
					t3 = x.replace(".lnk", "")
					ret["name"] = t3
					ret["state"] = 0
					ret["msg"] = "获取成功"
					return ret
	except:
		print("except")
	return ret


#获取
def GetFilelist(pathx):
	if os.path.isdir( pathx ):
		return os.listdir(pathx)
	else:
		return []

#发消息控制流程
#D:\soft\RTX\1\Bin\QQScLauncher.exe /uin:3001300721 /quicklunch:9267E345AA0DE3867A4983C6C9FD354D343084EF75AE6611037DE3C62FB7B29B7CB3E95E53A884BC
def SendMessage(msgtxt, jsonp):
	#print(msgtxt, jsonp)
	print(jsonp["name"])
	#先组成一个cmdline
	cmdline = "cmd.exe /c D:\\soft\\RTX\\1\\Bin\\QQScLauncher.exe "
	cmdline = cmdline + "/uin:" 
	cmdline = cmdline + jsonp["uin"] 
	cmdline = cmdline + " /quicklunch:" 
	cmdline = cmdline + jsonp["arg"]
	#print(cmdline)
	
	#开启对话框
	os.system(cmdline)
	time.sleep(3)

	#输入文字
	inputText(msgtxt)
	time.sleep(0.2)

	#发送文字
	Key_Alt_s()
	time.sleep(1)

	#关闭对话框
	#print("ALT+C")
	Key_Alt_c2()
	time.sleep(1)



#python main.py file.txt des_dir
def main():

	#处理目录
	argv_file = ""
	argv_dir  = ""
	if(len(sys.argv)>1):
		argv_file = sys.argv[1]
	if(len(sys.argv)>2):
		argv_dir  = sys.argv[2]
	if(os.path.isdir(argv_dir)==False):
		argv_dir =  os.getcwd()
	if(os.path.isfile(argv_file)==False):
		print("问候语.txt 未设置")
		return
	if(os.path.exists(argv_file)==False):
		print("问候语.txt文件不存在")
		return
	iLen = len(argv_dir) - 1
	if(argv_dir[iLen:] != "\\"):
		argv_dir = argv_dir + "\\"

	
	#读入问候语
	msgtxt = ""
	with open(argv_file, 'r', encoding='utf-8') as f:
		for txt in f:
			msgtxt = msgtxt + txt
	print(msgtxt)

	#遍历目录
	dirs = GetFilelist(argv_dir)
	for x in dirs:
		p = argv_dir + x
		s = Get_FullPath(p)
		if(s["state"] != 0):
			print("错误:", p)
			continue
		SendMessage(msgtxt,s)
		print("*" * 60)


if __name__ == '__main__':
	main()




