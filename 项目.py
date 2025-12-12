# 本项目采用 2 空格缩进，此风格旨在提升代码紧凑性与可读性，符合现代较新 Python 解释器规范，不产生语法或运行错误。
import psutil
import GPUtil
import random
import string 
import threading
import time
import subprocess
import requests
import json
import os
# ------------------------------初始化------------------------------
默认路径 = "~"
# ------------------------------打包类(I)------------------------------
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
      for chunk in r.iter_content(1024 * 1024):
        f.write(chunk)

# ------------------------------打包类(II)------------------------------
def 获取json(版本):
  print(f"接收到任务:获取json版本信息{版本}")
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

def 初始化文件夹(路径):        
  global 分类文件夹_主文件夹,分类文件夹_游戏,分类文件夹_JDK,分类文件夹_游戏_实例,分类文件夹_游戏_材质,分类文件夹_游戏_Java库
  try:
    if 路径 == "~":
      分类文件夹_主文件夹 = os.path.join(os.path.expanduser(路径), "xinghui_mc")
    else:
      if 检测读写权限(路径) == True:
        分类文件夹_主文件夹 = os.path.join(路径, "xinghui_mc")
      else:
        print("ERROR!路径不合法!")
        return False
    print(f"成功合成主文件夹{分类文件夹_主文件夹}")
    
    分类文件夹_游戏 = os.path.join(分类文件夹_主文件夹, ".minecraft")
    print(f"成功合成游戏文件夹{分类文件夹_游戏}")
    
    分类文件夹_游戏_实例 = os.path.join(分类文件夹_游戏, "versions")
    print(f"成功合成游戏实例文件夹{分类文件夹_游戏_实例}")
    
    分类文件夹_游戏_材质 = os.path.join(分类文件夹_游戏, "assets")
    print(f"成功合成游戏材质文件夹{分类文件夹_游戏_材质}")
    
    分类文件夹_游戏_Java库 = os.path.join(分类文件夹_游戏, "libraries")
    print(f"成功合成游戏Java库文件夹{分类文件夹_游戏_Java库}")
    
    分类文件夹_JDK = os.path.join(分类文件夹_主文件夹, "JDK")
    print(f"成功合成JDK文件夹{分类文件夹_JDK}")
    
    os.makedirs(分类文件夹_主文件夹, exist_ok=True)
    os.makedirs(分类文件夹_游戏, exist_ok=True)
    os.makedirs(分类文件夹_游戏_实例, exist_ok=True)
    os.makedirs(分类文件夹_游戏_材质, exist_ok=True)
    os.makedirs(分类文件夹_游戏_Java库, exist_ok=True)
    os.makedirs(分类文件夹_JDK, exist_ok=True)
    print("所有文件夹创建或检测成功(yes)")
    return True
  except Exception as e:
    print("所有文件夹创建或检测失败(no)")
    return False

def 检测读写权限(路径):
    try:
        # 创建测试文件
        测试文件 = os.path.join(路径, "权限测试.tmp")
        with open(测试文件, "w") as f:
            f.write("test")
        
        # 读取测试文件
        with open(测试文件, "r") as f:
            f.read()
        
        # 删除测试文件
        os.remove(测试文件)
        return True
    except Exception as e:
        print(f"error!路径 {路径} 无读写权限: {e}")
        return False

class 解析():
  def 生成启动参数(字典数据,设置参数):
    # 游戏参数
    游戏名 = 设置参数["游戏名"]
    游戏目录 = 设置参数["游戏目录"]
    资源目录 = 设置参数["资源目录"]
    资源索引版本 = 设置参数["资源索引版本"]
    用户UUID = 设置参数["用户UUID"]
    访问令牌 = 设置参数["访问令牌"]
    客户端ID = 设置参数["客户端ID"]
    微软XboxID = 设置参数["XboxID"]
    用户类型 = 设置参数["用户类型"] 
    # JVM虚拟机参数
    JavaEXE路径 = 设置参数["jvm虚拟机参数_java.exe路径"]
    Java虚拟机最大内存 = "-Xmx" + 设置参数["jvm虚拟机参数_最大内存"]
    Java虚拟机最小内存 = "-Xms" + 设置参数["jvm虚拟机参数_标准内存"]
    try:
      if 字典数据["minimumLauncherVersion"] >= 21:
        # 解析json
        json解析_ID = 字典数据["id"]
        json解析_启动参数配置 = 字典数据["arguments"]
        json解析_资源索引配置 = 字典数据["assetIndex"]
        json解析_核心文件下载配置 = 字典数据["downloads"]
        json解析_java版本要求配置 = 字典数据["javaVersion"]
        json解析_游戏依赖库配置 = 字典数据["libraries"]
        json解析_游戏主类配置 = 字典数据["mainClass"]
        json解析_最低启动器版本要求 = 字典数据["minimumLauncherVersion"]
        json解析_版本发布时间 = 字典数据["releaseTime"]
        json解析_版本发行版本 = 字典数据["type"]
        # 启动参数
        # 过滤掉字典
        游戏启动参数列表 = []
        for 参数 in json解析_启动参数配置["game"]:
          if isinstance(参数, str):
              游戏启动参数列表.append(参数)  
        
        JVM参数列表 = [
          "java",    # 
          "-Xmx",    # 
          "-Xms",    #
          "-Xss1M",    # 线程栈大小1MB
          "-Xmn256m",    # 新生代内存256MB
          # 对于MC的优化
          "-Dlog4j.formatMsgNoLookups=true",    # 修复代码漏洞
          "-XX:+UseG1GC",    #使用G1垃圾回收器
          "-XX:-UseAdaptiveSizePolicy",    # 禁用自适应大小策略（稳定GC行为）
          "-XX:-OmitStackTraceInFastThrow",  # 保留完整堆栈跟踪（便于调试）
          "-Dfml.ignoreInvalidMinecraftCertificates=True",    # 忽略证书验证问题
          "-Dfml.ignorePatchDiscrepancies=True",    # 忽略版本补丁差异
          "-Dminecraft.launcher.brand=minecraft-launcher",    # 伪装成正版启动器
          "-Dminecraft.launcher.version=2.1.3674",    # 伪装启动器版本
          "-Dnarrator=false",     # 禁用旁白功能
          # 系统伪装
          '-Dos.name="Windows 10"',    #伪装系统
          "-Dos.version=10.0",    # 伪装系统版本
          "原生库路径",    #java原生库路径
          "-cp",    #
          "所有jar",    #所有jar文件
          "主类"    #游戏主类
          ]
        原生库路径 = "-Djava.library.path=" + "./natives"
        # 合并预设的JVM参数
        启动参数列表 = JVM参数列表 + 游戏启动参数列表
        
        print(f"抓取到游戏启动参数并合并jvm配置\n{启动参数列表}\n")
        字符串 = " ".join(启动参数列表)
        # 整理游戏参数配置
        字符串 = 字符串.replace("${auth_player_name}", f"{游戏名}")   #游戏名参数
        字符串 = 字符串.replace("${version_name}", f"{json解析_ID}")   #游戏版本参数
        字符串 = 字符串.replace("${game_directory}", f"{游戏目录}")   #游戏目录参数
        字符串 = 字符串.replace("${assets_root}", f"{资源目录}")   #游戏目录里面的资源目录参数
        字符串 = 字符串.replace("${assets_index_name}", f"{资源索引版本}")   #资源目录的索引版本
        字符串 = 字符串.replace("${auth_uuid}", f"{用户UUID}")   #顾名思义,写个UUID在里面
        字符串 = 字符串.replace("${auth_access_token}", f"{访问令牌}")    #访问令牌,离线写0
        字符串 = 字符串.replace("${clientid}", f"{客户端ID}")   #客户端ID,离线写0,有时也叫做客户端令牌但那是错的
        字符串 = 字符串.replace("${auth_xuid}", f"{微软XboxID}")    #XboxID,离线写0
        字符串 = 字符串.replace("${user_type}", f"{用户类型}")    #用户类型,试玩版要写demo,离线是legacy或者mojang,真实账号写msa
        字符串 = 字符串.replace("${version_type}", f"{json解析_版本发行版本}")   
        # 整理JVM虚拟机配置
        字符串 = 字符串.replace("java", f"{JavaEXE路径}")
        字符串 = 字符串.replace("-Xmx", f"{Java虚拟机最大内存}")
        字符串 = 字符串.replace("-Xms", f"{Java虚拟机最小内存}")
        字符串 = 字符串.replace("原生库路径", f"{原生库路径}")
        字符串 = 字符串.replace("主类", f"{json解析_游戏主类配置}")
        # 字符串 = 字符串.replace("", f"{}")
        # 最终播报
        print(f"解析成功:{字符串}")
    except Exception as e:
      print(f"解析失败:{e}")
  
  def 获取并下载所有文件(元组数据):
    try:
      if 元组数据["minimumLauncherVersion"] >= 21:
        # 解析json
        json解析_ID = 元组数据["id"]
        json解析_核心文件下载配置 = 元组数据["downloads"]
        核心文件下载 = 核心文件下载["client"]
        核心文件下载 = 核心文件下载["url"]
        json解析_java版本要求配置 = 元组数据["javaVersion"]
        json解析_游戏依赖库配置 = 元组数据["libraries"]
        文件.下载_URL()
    except Exception as e:
      print(f"解析失败:{e}")

def 初始化文件夹并读取配置():
  默认配置文件字典 = {
    "测试":"测试文本"
  }
  配置配置文件字符串 = json.dumps(默认配置文件字典, ensure_ascii=False)
  if 初始化文件夹(默认路径) == True:
    配置目录 = os.path.join(分类文件夹_主文件夹, "配置.json")
    if not 文件.检查(配置目录) == True:
      print("配置文件不存在,初始化中")
      文件.写(配置目录, 配置配置文件字符串)
      print("初始化完毕")
    配置 = 文件.读(配置目录)
    配置 = json.loads(配置)
    return 配置
# ------------------------------主程序------------------------------
配置 = 初始化文件夹并读取配置()
print(f"读取到配置文件:{配置}")
设置参数 = {
  "游戏名":"测试",
  "游戏目录":"0",
  "资源目录":"0",
  "资源索引版本":"0",
  "用户UUID":"000000000-0000-0000-0000-000000000000",
  # 试玩版访问令牌,离线写0
  "访问令牌":"0",
  # 客户端令牌,离线写0
  "客户端ID":"0",
  # Xbox账户ID,离线写0或者空字符""
  "XboxID":"0",
  # 用户类型,试玩版要写demo,离线是legacy或者mojang,真实账号写msa
  "用户类型":"legacy",
  "游戏目录":"0",
  "jvm虚拟机参数_java.exe路径":"0",
  "jvm虚拟机参数_最大内存":"0",
  "jvm虚拟机参数_标准内存":"0",
  "jvm虚拟机参数_所有jar文件":"0",
  }
解析.生成启动参数(获取json("1.21.8"), 设置参数)