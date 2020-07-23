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
       for file in os.listdir(filepath):
           print("file:",filepath+"/"+file)
           if os.path.isfile(filepath+"/"+file):
              os.remove(filepath+"/"+file)

       return os.rmdir(filepath)
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

def GetFileName(filepath):
    return os.path.splitext(filepath)[0]


def MergFile(part_file_names,localPath,filesize,block_size,part_file_count,part_file_end,del_part_file_able,mult_file_name):
    '合并文件'

    if CheckFileExists(localPath):
        os.remove(localPath)

    with open(localPath,"ab") as  targetfile:
        for i in range(part_file_count):
            if i==part_file_end:
                block_size =filesize -i*block_size
            with open(part_file_names[i],"rb") as pf:
                targetfile.write(pf.read(block_size))

    if del_part_file_able:
        print(mult_file_name)
        DeleteFileDir(mult_file_name)

    pass

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





