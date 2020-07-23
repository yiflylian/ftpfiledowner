'''main 调用py '''

import json#json库
import FileUtils
from uploadtask.SaturnCloudAPI import *
from datetime import datetime
import threading,time
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}


#<editor-fold desc="上传文件夹">
def UploadDir(upload_dir):
    # 判断上传文件夹是否存在
    if FileUtils.CheckFileExists(upload_dir):
        files = FileUtils.Listfile(upload_dir)
        print(datetime.now(), "files", files)
        for file in files:
            if FileUtils.CheckIsFile(upload_dir + file):  # 文件 上传
                print(datetime.now(), upload_dir + file, "is file")
                UploadFile(upload_dir + file)
            else:  # 文件夹
               UploadDir(upload_dir + file+"/")
#</editor-fold>

#<editor-fold desc="上传文件夹">
def UploadFile(filename,filesize,localPath,upload_path):
    print(datetime.now(), "filename", filename)
    print(datetime.now(), "filesize", filesize)
    print(datetime.now(), "localPath", localPath)
    print(datetime.now(), "upload_path", upload_path)
    #1.检查文件路径是否超过10级


    #1.检查 时候有容量可以上传
    # file_upload
    global  headers
    global  UserInfo
    params= dict()
    # put("user_id", USER_ID)
    #put("file_size",destfile.length())
    params["user_id"]=UserInfo["user_id"]
    params["file_size"]=filesize
    data_json= json.loads(params)
    result = PostForNet(URL_FILE_UPLOADABLE,data_json,headers)
    if not  result==None:
        pass
        #2. TODO 检查文夹夹是否存在 IPFS 是否启动
        # TODO GetFilePid()
            #3.ipfsPack
    #AESKEY
    AesKey=GetForNet(URL_GET_AES_KEY,False)
    if  not AesKey ==None:
        pass
    # TODO 判断MD5 如果为空就进行md5加密

    #PACK
    params = dict()
    # put("user_id", USER_ID)
    # put("file_size",destfile.length())

    # .params("flag", JSONObject().apply
    # {
    #     put("MetaHash", uptask.file_MD5)
    # put("MetaSize", uptask.file_size)
    # put("Gzip", false)
    # put("Aes", true)
    # put("AesKey", uptask.Aes_key)
    # put("RS", false)
    # put("Feed", false)
    # }.toString())
    # .params("file", uptask.dest_file)
    params["MetaHash"] =AesKey[:32]
    print(datetime.now(),"MetaHash:",AesKey[:32])
    params["MetaSize"] = filesize
    params["Gzip"] = filesize
    params["Aes"] = filesize
    params["AesKey"] = filesize
    params["RS"] = filesize
    params["Feed"] = filesize
    params["AesKey"] = filesize
    data_json=json.loads(params)
    file =  {'file': open(localPath, 'rb')}
    # from_data上传文件，注意参数名propertyMessageXml
    # data = (fields={'propertyMessageXml': ('filename', open('D:/123.xml', 'rb'), 'text/xml')})

    data_json = json.loads(params)
    PostForNet(URL_FILE_PACK,data_json=data_json,files=file)






    pass
#</editor-fold>

#<editor-fold desc="">

UserInfo=None

def UserLogin(config_filePath):
    global  UserInfo
    UserInfo= GetToken(config_filePath=config_filePath)
    if UserInfo==None:
        print(datetime.now(), "登陆失败", )
    else:
        print(datetime.now(),"登陆成功","用户信息：",UserInfo)
        global headers
        headers["Authorization"] =UserInfo["access_token"]
        StartRefrenTokenTask()


def LogUserInfo():
    global UserInfo
    print(datetime.now(),"LogUserInfo",UserInfo)
    print(datetime.now(),"headers",headers)


def RefrenTokenTask():
    while True:
        print(datetime.now(), "RefrenTokenTask","B")
        time.sleep(10*60)
        print(datetime.now(), "RefrenTokenTask","A")
        global headers
        print(datetime.now(),"headers",headers)
        # PutForNet(URL_REFREN_TOKEN_TIME,headers=headers)



def  StartRefrenTokenTask():
    task=threading.Thread(target=RefrenTokenTask,name="StartRefrenTokenTask")
    task.start()
    # task.join()
    print(datetime.now(),"StartRefrenTokenTask","thread %s ended."% threading.current_thread().name)


#</editor-fold>






#运行方法
if __name__ == '__main__':
     aeskey =GetForNet(URL_GET_AES_KEY,False)
     print(aeskey)
