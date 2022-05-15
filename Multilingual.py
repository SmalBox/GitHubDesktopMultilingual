# GitHubDesktop 多语言切换
# Main file
# Author: SmalBox
# Version: V1.0.0

import csv
import os
import sys
import WinGetAppPath

# 替换配置文件
dicFileName = "./GitHubDesktopReplaceDic.csv"
# 替换目录
replaceFilePath = WinGetAppPath.GetConfigPath()
# 替换文件列表
replaceFileNameList = ["main.js", "renderer.js"]
# 源语言
originLanguage = "English"
# 目标语言
targetLanguage = ""


def ReplaceConfig() -> bool:
    convertTable = []
    originIndex = 0
    targetIndex = 0
    global targetLanguage

    try:
        with open(dicFileName, encoding="utf8") as f:
            render = csv.reader(f)
            headerRow = next(render)
            try:
                originIndex = headerRow.index(originLanguage)
                for header in headerRow:
                    if (len(header.split('@')) > 1):
                        header.split('@')[1].upper() == "SMALBOX"
                        targetLanguage = header
                        break
                if (targetLanguage == ""):
                    print("配置文件中未发现配置的目标语言,请在目标语言的title后加上@SmalBox来标记目标语言.\n例如:简体中文@SmalBox")
                    return False
                else:
                    print("目标语言：" + targetLanguage)
                    targetIndex = headerRow.index(targetLanguage)
            except:
                print("设置目标语言异常:" + sys.exc_info())
                return False
            for line in render:
                if ((line[originIndex] != "") & (line[targetIndex] != "")):
                    convertTable.append((line[originIndex], line[targetIndex]))

        for fileName in replaceFileNameList:
            if (replaceFilePath == ""):
                return False
            fileAllName = os.path.join(replaceFilePath, fileName)
            data = ""
            with open(fileAllName, mode="r", encoding="utf8") as f:
                data = f.read()
                for item in convertTable:
                    data = data.replace(item[0], item[1])
            with open(fileAllName, mode="w", encoding="utf8") as f:
                f.write(data)
        return True
    except:
        print(sys.exc_info())
        return False

# 替换流程：1.备份配置文件 2.根据替换字典替换文件
# 恢复流程：1.获取备份文件 2.复制备份文件到配置目录
def main():
    title = "GitHub Desktop 多语言切换(Switch Multilingual)"
    authorInfo = "Power By SmalBox"
    print("{:■^50}".format(title))
    print("▶简体中文 菜单◀")
    print("▶[1] 多语言切换(自动备份到当前目录下Backup目录中)")
    print("▶[2] 从备份恢复")
    print("▶English Menu◀")
    print("▶[1] Switch Multilingual(Automatically backup to folder Backup of the current directory)")
    print("▶[2] Restore from the Backup")
    print("{:■>50}\n".format(authorInfo))
    inputNum = eval(input("▶请输入功能序号(Please enter function number):"))

    if (inputNum == 1):
        # 备份阶段
        content = "1/2.开始备份."
        print("▶{}◀".format(content))
        if (WinGetAppPath.BackupConfig(\
                WinGetAppPath.GetConfigPath(),\
                WinGetAppPath.GetBackupPath(),\
                replaceFileNameList) == True):
            content = "1/2.备份完成,配置文件已备份到当前目录的Backup中."
            print("▶{}◀".format(content))
        else:
            content = "1/2.备份失败"
            print("▶{}◀".format(content))
            return

        # 语言切换阶段
        content = "2/2.开始多语言切换."
        print("▶{}◀".format(content))
        if (ReplaceConfig() == True):
            content = "2/2.多语言切换完成，请重启 GitHub Desktop 完成生效."
            print("▶{}◀".format(content))
        else:
            content = "2/2.多语言切换失败"
            print("▶{}◀".format(content))
            return
    elif (inputNum == 2):
        content = "1/1.开始恢复备份."
        print("▶{}◀".format(content))
        if (WinGetAppPath.RestoreConfig(\
                WinGetAppPath.GetConfigPath(),\
                WinGetAppPath.GetBackupPath(),\
                replaceFileNameList) == True):
            content = "1/1.备份恢复完成."
            print("▶{}◀".format(content))
        else:
            content = "1/1.备份恢复失败."
            print("▶{}◀".format(content))
    else:
        print("需要输入有效的功能序号.")


if __name__ == '__main__':
    main()
    print("\n▶Power by SmalBox. See you next time~◀\n")
    input("按任意键退出……")