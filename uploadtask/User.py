'''用户'''

import FileUtils
import json

USERINFO_SAVE_DIR='./userinfo/' #保存用户信息的文件夹path

#<editor-fold desc="保存用户信息">

def SaveUserInfo(mobile,data):
    '''保存用户信息 /userinfo/mobile'''
    if not FileUtils.CheckFileExists(USERINFO_SAVE_DIR):
        FileUtils.CreateFileDir(USERINFO_SAVE_DIR)
    with open(USERINFO_SAVE_DIR+mobile+".json","w",encoding="utf-8") as f:
        json.dump(data,fp=f)

#</editor-fold>

#<editor-fold desc="获取用户信息">

def GetUserInfo(mobile):
    '''保存用户信息 /userinfo/mobile'''
    with open(USERINFO_SAVE_DIR+mobile+".json","r",encoding="utf-8") as f:
        return json.load(fp=f)

#</editor-fold>