import psutil
import matplotlib.pyplot as plt
import GPUtil
import zipfile
import tkinter as tk
import tkinter.ttk as ttk
import random
import string
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import time
import subprocess
import sys
import requests
import json
import os
from pathlib import Path

# ------------------------------打包的类(I)------------------------------
def 获取性能占用():
  开始耗时 = time.time()
  CPU性能占用 = psutil.cpu_percent(interval=0.5)
  内存占用 = psutil.virtual_memory().percent
  gpus = GPUtil.getGPUs()  # 这里获取的就是所有GPU
  
  GPU数量 = len(GPUtil.getGPUs())
  GPU组 = []
  GPU显存组 = []
  for gpu in gpus:
    # 核心占用
    GPU组.append(f"{gpu.load*100:.1f}%")
    
    # 显存信息
    显存信息 = {
    "已用MB": gpu.memoryUsed,
    "总共MB": gpu.memoryTotal,
    "占用率": f"{gpu.memoryUtil*100:.1f}%"
    }
    GPU显存组.append(显存信息)
  结束耗时 = time.time()
  总耗时 = 结束耗时 - 开始耗时
  if GPU数量 != 0:
    数据 = {
      "计算耗时":f"{总耗时}",
      "CPU":f"{CPU性能占用}",
      "内存":f"{内存占用}",
      "独立显卡?": True,
      "GPUlen":f"{GPU数量}",
      "GPU_占用": GPU组,
      "GPU_显存占用": GPU显存组
    }
  else:
    数据 = {
      "计算耗时":f"{总耗时}",
      "CPU":f"{CPU性能占用}",
      "内存":f"{内存占用}",
      "独立显卡?": False, 
    }
  
  换行json_str = json.dumps(数据, ensure_ascii=False, indent=2)
  数据json_str = json.dumps(数据, ensure_ascii=False)
  print(f"获取系统占用信息:\n{换行json_str}")
  return 数据json_str

def 随机串(长度=3):
  """生成指定长度的随机字符串（包含字母和数字）"""
  # 随机选择字符
  字符集 = string.ascii_letters + string.digits  # 大小写字母+数字
  随机串 = ''.join(random.choice(字符集) for _ in range(长度))
  return 随机串

def 运行命令(命令):
  命令参数 = str(命令)
  try:
    subprocess.Popen(命令参数, shell=True)
    print(f"运行命令({命令参数})成功✅")
    return f"运行命令({命令参数})成功✅"
  except Exception as e:
    print(f"运行命令({命令参数})失败!❌")
    print(f"错误:{e}")
    return [f"运行命令({命令参数})失败!❌","错误:{e}"]
  
class 线程函数:     #线程函数(让别的函数跑在子线程)
  def 运行(self, 函数, 线程名字=None):
    if 线程名字 == None:
      线程名字 = f"未命名线程_{随机串(4)}"
    else:
      线程名字 = f"{线程名字}_{随机串(4)}"
    线程变量 = threading.Thread(target=函数, daemon=True, name=线程名字)
    线程变量.start()
    print(f"由{函数}启动的的线程'{线程名字}'开始运行")
线程 = 线程函数()

class 广播函数:    #广播函数
  def __init__(self):
    self.广播字典 = {}
  
  def 当收到广播(self, 广播名称, 要执行的函数):
    self.广播字典[广播名称] = 要执行的函数
  
  def 广播(self, 广播名称):
    if 广播名称 in self.广播字典:
      self.广播字典[广播名称]()
广播 = 广播函数()

所有实例 = []
class ws_dt:     # ws服务器函数
  def __init__(self, 端口=9000, 处理类=None):
    self.端口 = 端口
    self.处理类 = 处理类
    self.server = None
    self.所有实例 = []  # 存所有客户端实例

  def 客户端连接(self):
    """检测当前是否有客户端连接"""
    return len(self.所有实例) > 0
  
  def 客户端数量(self):
    """获取当前连接的客户端数量"""
    return len(self.所有实例)
  
  def 设置(self, 处理类, 端口=9000):
    """设置服务器参数"""
    self.端口 = 端口
    self.处理类 = 处理类
      
  def 开启(self):  # 改名open→开启
    """启动服务器"""
    # 动态创建处理类，能访问到ws_dt实例
    外层self = self  # 保存引用，供内部类使用
    
    class 自定义处理类(WebSocket):
      def handleConnected(客户端self):
        外层self.所有实例.append(客户端self)
        客户端self.sendMessage("连接成功！")
        print("有新客户端链接")

      def handleMessage(客户端self):
        # 分解客户端信息
        global 客户端指令, 客户端指令数据
        客户端消息 = 客户端self.data
        存1 = json.loads(客户端消息)
        客户端指令 = list(存1.keys())[0]
        客户端指令数据 = 存1[客户端指令]

        print(f"收到指令{客户端指令}!携带数据:{客户端指令数据}")  # 打印收到的消息
        广播.广播(客户端指令)  # 广播收到的消息
      
      def handleClose(客户端self):
          if 客户端self in 外层self.所有实例:
            外层self.所有实例.remove(客户端self)
          print("有客户端断开连接")
    
    self.server = SimpleWebSocketServer('localhost', self.端口, 自定义处理类)
    print(f"✅ 服务器启动在端口 {self.端口}")
    self.server.serveforever()
  
  def 说话(self, 内容):  # 改名say→说话
    """给所有客户端发消息"""
    for 实例 in self.所有实例:  # 用self.所有实例
      try:
        实例.sendMessage(str(内容))
      except:
        pass  # 发送失败就跳过
    print(f"广播给 {len(self.所有实例)} 个客户端: {内容}")
      
class 文件:     #管理和下载文件函数
  
  def 检查(路径):
    if os.path.exists(str(路径)):
      return True
    else:
      return False
  
  # 检查并创建文件夹
  def 创建文件夹(名称):
    os.makedirs(名称, exist_ok=True)
  
  # 写文件
  def 写(文件路径, 内容):
    """创建并写入文件（直接写入内容）"""
    父目录 = os.path.dirname(文件路径)
    if 父目录:
      os.makedirs(父目录, exist_ok=True)
    
    with open(文件路径, 'w', encoding='utf-8') as f:
      f.write(str(内容))

  # 读文件
  def 读(被读取的文件或路径):
    with open(file=被读取的文件或路径, mode="r", encoding="utf-8") as f:
      return f.read()
  # 下载文件
  def 下载_URL(url,path):
    r = requests.get(url, stream=True)
    with open(path, "wb") as f:
      for chunk in r.iter_content(8192):
        f.write(chunk)
# ------------------------------打包类(II)------------------------------
def 获取json(版本):
  URL链 = f"https://bmclapi2.bangbang93.com/version/{版本}/json"
  try:
    response = requests.get(URL链)
    if response.status_code == 200:
      总数据 = json.loads(response.text)
      发送 = 总数据["id"]
      print(f"获取我的世界JSON版本,请求成功\n{发送}")
      return 总数据
    else:
      print(f"获取我的世界JSON版本,请求失败")
  except Exception as e:
    print(f"获取我的世界JSON版本数据出错:{e}")

class 解析():
  def 生成启动参数(元组数据,设置参数):
    用户名 = 设置参数["用户名"]
    try:
      if 元组数据["minimumLauncherVersion"] >= 21:
        # 解析json
        json解析_启动参数配置 = 元组数据["arguments"]
        json解析_资源索引配置 = 元组数据["assetIndex"]
        json解析_核心文件下载配置 = 元组数据["downloads"]
        json解析_java版本要求配置 = 元组数据["javaVersion"]
        json解析_游戏依赖库配置 = 元组数据["libraries"]
        json解析_游戏主类配置 = 元组数据["mainClass"]
        json解析_最低启动器版本要求 = 元组数据["minimumLauncherVersion"]
        json解析_版本发布时间 = 元组数据["releaseTime"]
        json解析_版本发行版本 = 元组数据["type"]
        # 启动参数
        游戏启动参数配置 = json解析_启动参数配置["game"]
        print(f"抓取到游戏启动参数配置\n{游戏启动参数配置}")
        索引 = 游戏启动参数配置.index("${auth_player_name}")
        游戏启动参数配置[索引] = f"{用户名}"
        # 最终播报
        print("解析成功")
    except Exception as e:
      print(f"解析失败:{e}")
# ------------------------------主程序------------------------------
默认设置参数 = {
  "用户名":"测试",
  "游戏目录":"0",
  "资源目录":"0",
  "资源索引版本":"0",
  "用户UUID":"000000000-0000-0000-0000-000000000000",
  # 试玩版访问令牌,离线写0
  "访问令牌":"0",
  # 客户端令牌,离线写0
  "客户端令牌":"0",
  # Xbox账户ID,离线写0或者空字符""
  "XboxID":"0",
  # 用户类型,试玩版要写demo,离线是legacy或者mojang,真实账号写msa
  "用户类型":"legacy",
  # 版本类型,正式版的话要写release
  "版本类型":"release",
  "jvm虚拟机参数_java.exe路径":"",
  "jvm虚拟机参数_最大内存":"",
  "jvm虚拟机参数_标准内存":"",
  "jvm虚拟机参数_原生库路径":"",
  "jvm虚拟机参数_所有jar文件":"",
  }
解析.生成启动参数(获取json("1.21.8"), 默认设置参数)