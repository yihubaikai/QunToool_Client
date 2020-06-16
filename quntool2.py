import requests,json
import webbrowser
import time,random
import win32clipboard as w
import win32con
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


def Save_Log(filename, text):
	with open(filename,'a',encoding='utf-8') as f:
		f.write(text)

#获取链接:点击链接加入群聊【一带一路资料群】：https://jq.qq.com/?_wv=1027&k=5ui5cYI
#点击链接加入群聊【wap站长变现交流群】：https://jq.qq.com/?_wv=1027&k=5UtybQp
def GetUrl(url):
	ret = {"state":1}
	#url = "https://jq.qq.com/?_wv=1027&k=5ui5cYI"
	#url = "https://jq.qq.com/?_wv=1027&k=5UtybQp"
	#print(url)
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
			#print(iStart, iEnd,"群ID:", qunid)
			ret["state"] = 0
			ret["qunid"] = qunid
		else:
			print("获取群ID出错")


		#查找群链接:"var rawuin ="
		startflag = "tencent://groupwpa"
		endflag   = "\";"
		iStart	= txt.find(startflag)
		iEnd	  = txt.find(endflag,iStart)
		qunurl	= ""
		if(iEnd>iStart) and (iStart!=-1) and (iEnd!=-1):
			qunurl	= txt[iStart:iEnd]
			#print(iStart, iEnd,"群链接:", qunurl)
			ret["qunurl"] = qunurl
			if(ret["state"]!=0):
				ret["state"] = 2
			else:
				ret["state"] = 0
		else:
			print("获取群链接")



	except:
		pass
	return ret





 	




#打开qq群界面
def OepnQUN_ui(ret):
	if( "qunurl" in ret):
		#print("正在打开群:", ret["qunid"])
		webbrowser.open( ret["qunurl"],new=2,autoraise=True)
	else:
		webbrowser.open( ret,new=2,autoraise=True)
	time.sleep(3)

#输入文字
def inputText(text):
	setText(text)
	Key_Ctrl_v()



 

#读取配置
#点击链接加入群聊【海外大带宽站群服务器】：https://jq.qq.com/?_wv=1027&k=5aUMYPA,1
QunList = []
Adword  = []
Config = {}
Hellword= []
fileterarr = []
ServerUrl = "http://www.quntool.com/run_main"
ServerLogin = "http://www.quntool.com/login"

def Get_Login(ServerUrl,flag):
	ret = {"state":1}
	#print(ServerUrl)
	try:
		data = {"flag":flag}
		#print(ServerUrl)
		#print(data)
		r = requests.post(ServerUrl, data=data)
		txt = r.text
		#print(txt)
		b = json.loads(txt)
		if(b == None):
			print(txt)
			ret["msg"] = "数据解析错误：非法的json格式" 
			return ret
		if ("state" in b)== False:
			print(txt)
			ret["msg"] = "数据键值错误:无state" 
			return ret
		if b["state"] != "0":
			print(txt)
			ret["msg"] = b["msg"]
			return
		if ("qunlist" in b)== False:
			print(txt)
			ret["msg"] = "群列表找不到"
			return ret
		if(len(b["qunlist"])==0):
			print(txt)
			ret["msg"] = "群列表为空"
			return
		if ("adword" in b)== False:
			print(txt)
			ret["msg"] = "广告列表未找到"
			return ret
		if(len(b["adword"])==0):
			print(txt)
			ret["msg"] = "广告列表为空"
			return
		if ("runnum" in b)== False:
			print(txt)
			ret["msg"] = "运行次数找不到"
			return ret
		if(len(b["runnum"])==0):
			print(txt)
			ret["msg"] = "运行次数不能为空"
			return
		if ("nickflag" in b)== False:
			print(txt)
			ret["msg"] = "昵称标识找不到"
			return ret
		if(len(b["nickflag"])==0):
			print(txt)
			ret["msg"] = "昵称标识未设置"
			return

		#获取运行循环次数
		Config["runnum"] = int(b["runnum"]) #初始值

		#获取昵称标识
		Config["nickflag"] = b["nickflag"]  #获取昵称标识
			

		#清空群列表	
		QunList.clear()
		for x in b["qunlist"]:
			#print(x["id"], x["name"])
			if "id" in x and "name" in x and "url" in x:
				jsonstr = json.dumps(x)
				QunList.append(jsonstr) #增加广告记录
		
		#清空广告列表
		Adword.clear()
		for x in b["adword"]:
			#print(x["url"])
			obj = x["url"].replace("[\"", "")
			obj = obj.replace("\"]", "")
			#print(obj)
			Adword.append( obj ) #增加记录
		ret["state"] = 0
	except:
		pass
	return ret


def SendAdword(qunurl, adwordtext,noSendFlag):
	#print("正在打开群:")
	OepnQUN_ui(qunurl)
	r = copytext()
	if(r.find(noSendFlag) != -1):
		
		#print("关闭对话框:ALT+C")
		Key_Alt_c()
		Key_Alt_c()
		print("\n\n")
		print("x"*50)
		print("有我发得消息, 不发送")
		print("x"*50)
		print("\n\n")
		return

	#输入文字
	print("输入文字:", adwordtext)
	inputText(adwordtext)
	time.sleep(random.randint(1,3))

	#发送文字
	#print("发送文字:ALT+S")
	Key_Alt_s()
	time.sleep(random.randint(1,3))

	#关闭对话框
	#print("关闭对话框:ALT+C")
	Key_Alt_c()
	time.sleep(random.randint(1,3))
	Key_Alt_c()
	time.sleep(random.randint(1,3))
	print("\n\n")
	print("*"*50)
	#print("发送广告和文字")
	print("*"*50)
	print("\n\n")




def RegSoft(exepath):
	try:
		mepath = exepath#"d:\\p.exe"# sys.argv[0]
		print("\n开始注册")
		key = OpenKey(HKEY_CLASSES_ROOT, r"\\")
		if(key==0):
			print("\n注册失败",key)
			return
		print("\n注册",key)

		hand_shell = CreateKey(key, "webshell")
		if(hand_shell==0):
			print("\n创建hand_shell失败",hand_shell)
			return
		print("创建hand_shell:", hand_shell)

		SetValueEx(hand_shell,"",0,REG_SZ,"URL:Webshell Protocol Handler")
		#print("设置默认值:", hand_shell)

		key3 = SetValueEx(hand_shell,"URL Protocol",0,REG_SZ,"")
		#print("设置协议值:", hand_shell)

		hkey_shell = CreateKey(hand_shell, "DefaultIcon")
		if(hkey_shell==0):
			print("\n创建hkey_shell失败",hkey_shell)
			return
		#print("创建DefaultIcon:", hand_shell)
		
		key4 = SetValueEx(hkey_shell,"",0,REG_SZ,mepath)
		#print("设置DefaultIcon:",mepath)

		key_shell = CreateKey(hand_shell, "shell")
		open_key = CreateKey(key_shell, "open")
		hand_comm = CreateKey(open_key, "command")
		if(hand_comm==0):
			print("\n创建hand_comm失败",hand_comm)
			return
		key4 = SetValueEx(hand_comm,"",0,REG_SZ,"\""+mepath+"\" \"%1\"")
		#print("创建shell:", key3,open_key,hand_comm,key4)
		CloseKey(key)

		print("注册完成..\n")
		time.sleep(2)
	except:
		pass
	print("操作完成，如果失败了请使用管理员模运行\n")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def GetTopClass():
	ret = {"state":1,"title":"","class":""}
	try:
		handle = win32gui.GetForegroundWindow()
		if(handle>0):
			window_class = win32gui.GetClassName(handle)
			window_title = win32gui.GetWindowText(handle)
			ret["handle"] = handle
			ret["title"] = window_title
			ret["class"] = window_class
			ret["state"] = 0
	except:
		pass
	return ret

def ThreadFunc(argc):
	handle = win32gui.GetForegroundWindow()
	while True:
		window_title = win32gui.GetWindowText(handle)
		window_class = win32gui.GetClassName(handle)
		#print("句柄:", handle)
		#print("类名:", window_class)
		#print("标题:", window_title)
		#print("-" * 60)

		ret = GetTopClass()
		if(ret["handle"] == handle):
			print("自己是当前窗口")
		#开始菜单
		if(ret["state"]==0  and ret["class"] == "Windows.UI.Core.CoreWindow"):
			print("关闭开始菜单")
			win32api.keybd_event(91,0,0,0)
			time.sleep(0.1)
			win32api.keybd_event(91,0,win32con.KEYEVENTF_KEYUP,0)
			time.sleep(0.1)

		#如果出现添加群表示这个群已经把我删除了
		if(ret["state"]==0  and ret["title"] == "添加群"):
			print("关闭添加群对话框")
			win32api.keybd_event(18,0,0,0)#ALT
			time.sleep(0.1)
			win32api.keybd_event(115,0,0,0)#F4
			time.sleep(0.1)
			win32api.keybd_event(115,0,win32con.KEYEVENTF_KEYUP,0)
			time.sleep(0.1)
			win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)

		#如果出现添加群表示这个群已经把我删除了
		if(ret["state"]==0  and (ret["title"] == "关闭提示" or ret["title"]=="提示")):
			print("退出确认对话框")
			win32api.keybd_event(32,0,0,0)#F4
			time.sleep(0.1)
			win32api.keybd_event(32,0,win32con.KEYEVENTF_KEYUP,0)
			time.sleep(0.1)
			ret = GetTopClass()
			if(ret["state"]==0  and (ret["title"] == "关闭提示" or ret["title"]=="提示")):
				print("退出确认对话框")
				win32api.keybd_event(32,0,0,0)#F4
				time.sleep(0.1)
				win32api.keybd_event(32,0,win32con.KEYEVENTF_KEYUP,0)
				time.sleep(0.1)



		#print("类名:", ret["class"])
		#print("窗口:", ret["title"])
		#print("*" * 60)
		time.sleep(10)
def FuzhuThread():
	#threads = []
	t = threading.Thread(target=ThreadFunc,args=(u'爱情买卖',))
	t.setDaemon(True)
	t.start()
	#threads.append(t1)

def RunMain():

	FuzhuThread()
	#time.sleep(110000)
	#1.设置窗口宽度
	#os.system("cmd.exe/c mode con cols=56 lines=30")

	#2.输出注册信息
	print("*" * 50)
	print("软件使用注意事项:")
	print("1.最佳系统组合WIN10或者WIN2012")
	print("2.首次打开需要注册账户,充值才能用")
	print("3.点击软件打开需要登陆后台设置了之后才能用")
	print("4.如果发现无法运行，请使用管理员模式运行一次!")
	
	#3.导入注册表
	if is_admin():
		print("管理员模式运行")
		mepath = sys.argv[0]
		exname = mepath[len(mepath)-4:]
		exname = exname.upper()
		#print(exname)
		if(exname==".EXE"):
			RegSoft(mepath)
	else:
		if(len(sys.argv)==1):
			print("\n\n打开失败\n右击选择：以管理员身份运行一次\n")
			print("*" * 50)
			time.sleep(30)
			return

	#.4获取传入数据
	if(len(sys.argv)==1):
		print("\n\n你好,检测到你未登陆,请从后台登陆,然后打开\n")
		webbrowser.open(ServerLogin)
		print("*" * 50)
		time.sleep(30)
		return

	#5.判断参数是否合法
	flag=sys.argv[1]
	#print(flag)
	if(flag.find("webshell://") == -1):
		print("你好，请登陆后台从控制面板种点击启动按钮:-)")
		webbrowser.open(ServerLogin)
		print("*" * 50)
		time.sleep(30)
		return
	flag = flag[len("webshell://"):len("webshell://")+32]
	#print(flag)
	#6.请求数据	
	iStart = 0 #出错两次限制，第一次出错，需要登陆服务器，第二次出错程序自行再测试
	while True:
		ret = Get_Login(ServerUrl,flag)
		#print("ret",ret)
		time.sleep(5)

		#判断 如果出现异常如何处理
		if(ret["state"] != 0):
			if(iStart == 0):
				iStart = iStart + 1
				print(ret["msg"])
				webbrowser.open(ServerLogin)
				print("*" * 50)
				while True:
					print("请关闭本程序，然后新登陆后台点击开始")
					time.sleep(5)
				return
			else:
				print("你好，请重新登陆后台从控制面板种点击启动按钮:-)")
				print("*" * 50)
				time.sleep(50)
				continue
		
		#判断， 如果没有出现异常如何处理
		if(Config["runnum"] == 0):
			Config["runnum"] = 1
		print("运行次数:", Config["runnum"])
		print("群列表数量:", len(QunList))
		print("广告列表数量:", len(Adword))
		for i in range(0,Config["runnum"]):
			#群列表数量
			qunnum = len(QunList)
			if(qunnum == 0):
				print("你好，群列表为空:-)")
				print("*" * 50)
				time.sleep(50)
				continue

			#广告列表数量
			adnum = len(Adword)
			if(adnum == 0):
				print("你好，广告列表为空:-)")
				print("*" * 50)
				time.sleep(50)
				continue
			#进度统计
			iCount = 0

			#群发广告
			for x in QunList:
				iCount = iCount + 1
				js = json.loads(x)
				if ("id" in js) and ("name" in js) and ( "url" in js):
					index = random.randint(0, adnum-1)
					tmp = "群("+str(qunnum)+"/"+str(iCount)+"):"+js["id"]+":"+js["name"]+","
					tmp = tmp + "  广告("+str(adnum)+"/"+str(index)+"):\n" + Adword[index]
					print(tmp)
					#print("群(3/1):12212121:IDC广告群", "广告(3/1):xxxxxxxxxxxx",qunnum,iCount,js["id"],js["name"], adnum, index, Adword[index])
					SendAdword( js["url"], Adword[index],Config["nickflag"] )
		while True:
			print("任务完成！")
			print("*" * 50)
			time.sleep(50)






if __name__ == '__main__':
	RunMain()

def GetTopClass():
	ret = {"state":1,"title":"","class":""}
	try:
		handle = win32gui.GetForegroundWindow()
		if(handle>0):
			window_class = win32gui.GetClassName(handle)
			window_title = win32gui.GetWindowText(handle)
			ret["handle"] = handle
			ret["title"] = window_title
			ret["class"] = window_class
			ret["state"] = 0
	except Exception as e:
		pass
	return ret

def ClearOtherWindow():
	ret = GetTopClass()
	#开始菜单
	if(ret["state"]==0  and ret["class"] == "Windows.UI.Core.CoreWindow"):
		print("关闭开始菜单")
		win32api.keybd_event(91,0,0,0)
		time.sleep(0.1)
		win32api.keybd_event(91,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(0.1)

	#如果出现添加群表示这个群已经把我删除了
	if(ret["state"]==0  and ret["title"] == "添加群"):
		print("关闭添加群对话框")
		win32api.keybd_event(18,0,0,0)#ALT
		time.sleep(0.1)
		win32api.keybd_event(115,0,0,0)#F4
		time.sleep(0.1)
		win32api.keybd_event(115,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(0.1)
		win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)

	#如果出现添加群表示这个群已经把我删除了
	if(ret["state"]==0  and (ret["title"] == "关闭提示" or ret["title"]=="提示")):
		print("退出确认对话框")
		win32api.keybd_event(32,0,0,0)#F4
		time.sleep(0.1)
		win32api.keybd_event(32,0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(0.1)
		ret = GetTopClass()
		if(ret["state"]==0  and (ret["title"] == "关闭提示" or ret["title"]=="提示")):
			print("退出确认对话框")
			win32api.keybd_event(32,0,0,0)#F4
			time.sleep(0.1)
			win32api.keybd_event(32,0,win32con.KEYEVENTF_KEYUP,0)
			time.sleep(0.1)
	print("类名:", ret["class"])
	print("窗口:", ret["title"])
	print("*" * 60)


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

	ClearOtherWindow()
	OepnQUN_ui(ret)
	r = copytext()
	if(r.find("胡勇") != -1):
		ClearOtherWindow()
		print("关闭对话框:ALT+C")
		Key_Alt_c()
		Key_Alt_c()
		print("\n\n")
		print("x"*50)
		print("QUN:" + ret["qunid"] )
		print("QUNlink:" + ret["qunlink"] )
		print("有我发得消息, 不发送")
		print("x"*50)
		print("\n\n")
		return

	ClearOtherWindow()
	#输入文字
	print("输入文字:", ret["adword"])
	inputText(ret["adword"])
	#time.sleep(random.randint(1,8))

	ClearOtherWindow()
	#发送文字
	print("发送文字:ALT+S")
	Key_Alt_s()
	time.sleep(3)

	ClearOtherWindow()
	#关闭对话框
	print("关闭对话框:ALT+C")
	Key_Alt_c()
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



#if __name__ == '__main__':
	'''ReadQunList()
	ReadAdword()
	ReadHelloword()
	ReadFilter()
	#os.system("cmd.exe/c mode con cols=56 lines=30")
	while True:
		SendOnce()
		time.sleep(50)
	'''