'FileUtil 文件工具类'
import os
import  sys

'检查文件是否存在'
def CheckFileExists(filepath):
    return  os.path.exists(filepath)

'获取文件字节数'
def GetFileSize(filepath):
    if CheckFileExists(filepath):
        return  os.path.getsize(filepath)
    else: raise FileNotFoundError("未找到目标文件,请检查文件是否存在")

'创建文件夹'
def CreateFileDir(filepath):
    if CheckFileExists(filepath):
        raise FileExistsError("目标文件夹已存在")
    else:
        return os.mkdir(filepath)

'删除文件夹'
def DeleteFileDir(filepath):
   if CheckFileExists(filepath):
       return os.removedirs(filepath)
   else:
       raise FileNotFoundError("未找到目标文件夹,请检查文件夹是否存在")




############################################################
'test method'


'test  GetFileSize(filepath)'
def TestGetFileSize(filepath):
    print("TestGetFileSize")
    try:
        GetFileSize(filepath)
    except Exception as e:
       print(e)


if __name__ == '__main__':
   filepath ="123.txt"
   dirpath='test'


   print(sys.version)
   # DeleteFileDir(dirpath)
   #CreateFileDir(dirpath)
   #TestGetFileSize(filepath)





