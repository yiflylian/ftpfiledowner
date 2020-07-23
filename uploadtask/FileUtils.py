'FileUtil 文件工具类'
import os
import  sys
import shutil
from datetime import  datetime

def CheckFileExists(filepath):
    '检查文件是否存在'
    return  os.path.exists(filepath)


def GetFileSize(filepath):
    '获取文件字节数'
    if CheckFileExists(filepath):
        return  os.path.getsize(filepath)
    else: raise FileNotFoundError("未找到目标文件,请检查文件是否存在")


def CreateFileDir(filepath):
    '创建文件夹'
    if CheckFileExists(filepath):
        raise FileExistsError("目标文件夹已存在")
    else:
        return os.mkdir(filepath)


def DeleteFileDir(filepath):
   '删除文件夹'
   if CheckFileExists(filepath):
       return os.remdir(filepath)
   else:
       raise FileNotFoundError("未找到目标文件夹,请检查文件夹是否存在")

def Mkdirs(filepath):
    '如果path中的文件夹不存在，择创建'
    dirs = os.path.split(filepath)[0].split('/')
    dir = ''
    for i in range(len(dirs)):
        dir = dir + dirs[i] + "/"
        print('dir is ', dir)
        if not CheckFileExists(dir):
           CreateFileDir(dir)

def Listfile(filepath):
    '返回path文件中的所有文件'
    return os.listdir(filepath)

def CheckIsFile(filepath):
    'filepath  是否为文件'
    return os.path.isfile(filepath)

############################################################
'test method'


'test  GetFileSize(filepath)'
def TestGetFileSize(filepath):
    print("TestGetFileSize")
    try:
        GetFileSize(filepath)
    except Exception as e:
       print(datetime.now(),"erro:",e)


if __name__ == '__main__':
   filepath ="123.txt"
   dirpath='test'





   # print(sys.version)
   # DeleteFileDir(dirpath)
   #CreateFileDir(dirpath)
   TestGetFileSize(filepath)





