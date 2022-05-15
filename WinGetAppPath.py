# 辅助文件
# Author: SmalBox
# Version: V1.0.0

import shutil
import sys
import re
import win32con, win32api
import os
 
def GetAppPath(appNameWithSuffix) -> str: 
    upper_keyword = appNameWithSuffix.upper()
    path = ""
    sub_key = r'Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, sub_key, 0, win32con.KEY_READ) 
    info = win32api.RegQueryInfoKey(key) 
    for i in range(0, info[1]):  
     value = win32api.RegEnumValue(key, i)  
     if value[0].upper().endswith(upper_keyword):
      path = value[0]   
      break
    win32api.RegCloseKey(key) 
    return path

def GetAppDirPath(appNameWithSuffix) -> str:
    appPath = GetAppPath(appNameWithSuffix)
    if (appPath == ""):
        return ""
    else:
        return os.path.dirname(appPath)

def GetBackupPath() -> str:
    currPath = os.getcwd()
    backupPath = os.path.join(currPath, "Backup")
    return backupPath

def GetConfigPath() -> str:
    appDirPath = GetAppDirPath("GitHubDesktop.exe")
    if (appDirPath == ""):
        print("未获取到软件路径.(请检查 GitHub Desktop 是否安装 并 主动启动过一次。)")
        input("按任意键退出……")
        return ""
    appVersionPath = ""
    for item in os.listdir(appDirPath):
        if (re.match(r"app-+", item) != None):
            appVersionPath = item
            break
    configDirPath = os.path.join(appDirPath, appVersionPath, "resources", "app")
    return configDirPath


def BackupConfig(configPath: str, backupPath: str, configFileNameList: str) -> bool:
    if (os.path.exists(backupPath) == False):
        os.makedirs(backupPath)
    needBackup = False
    for fileName in configFileNameList:
        if (os.path.exists(os.path.join(backupPath, fileName)) == False):
            needBackup = True
            break
    if (needBackup):
        try:
            for fileName in configFileNameList:
                shutil.copy(os.path.join(configPath, fileName), backupPath)
                print("备份:" + fileName + ", 到:" + backupPath)
            return True
        except IOError as e:
            print("无法复制文件. %s" % e)
            return False
        except:
            print("异常错误:", sys.exc_info())
            return False
    return True

def RestoreConfig(configPath: str, backupPath: str, configFileNameList: str) -> bool:
    if (os.path.exists(backupPath) == False):
        print("备份目录Backup不存在")
        return False
    for fileName in configFileNameList:
        if (os.path.exists(os.path.join(configPath, fileName)) == False):
            print("备份文件" + fileName + "不存在")
            return False
    try:
        for fileName in configFileNameList:
            shutil.copy(os.path.join(backupPath, fileName), configPath)
            print("恢复:" + fileName + ", 到:" + os.path.join(configPath, fileName))
        return True
    except IOError as e:
        print("无法复制文件. %s" % e)
        return False
    except:
        print("异常错误:", sys.exc_info())
        return False