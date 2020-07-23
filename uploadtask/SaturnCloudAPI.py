'''saturncloud API'''

# <editor-fold desc=" saturncloud API  ">
ACCESS_PORT = 6016
# val Get_Token_Port = 6019 #开发
Get_Token_Port = 6018  # 测试
VERSION_CHECK_Port = 6012  # 测试
# HOST = "10.0.130.172"   #本地
# HOST = "39.106.216.189" #开发
HOST = "47.95.145.45"  # 测试
BASE_HOST = "http://" + HOST + ":"  # 测试

# BASE_URL="${BASE_HOST+ACCESS_PORT}/api/cloud/v1/"
BASE_URL = BASE_HOST + str(ACCESS_PORT)+"/api/cloud/v1/"
Login_URL = BASE_HOST + str(Get_Token_Port)

# <editor-fold desc=" 请求 REQUEST_CODE   ">
REQUEST_SUCESS_CODE = 200  # 请求成功 code

# </editor-fold>
# val URLS_GET_VERSION_CHECK = "${BASE_HOST+VERSION_CHECK_Port}version/code/"//版本检测:code
URLS_GET_VERSION_CHECK = BASE_HOST+str(VERSION_CHECK_Port)+"/api/v1/check_version"  # 版本检测:code

# <editor-fold desc="用户">
URL_LOGIN = Login_URL + "/api/cloud/v1/login"
URL_REGISTER_COMPANY = BASE_URL + "register_company"  # 企业注册
URL_RESERT_PASS_MESSAGE = BASE_URL + "$reset_pass/message"  # 发送重置密码短信
URL_RESERT_PASS_VERIFY = BASE_URL + "reset_pass/verify"  # 验证重置密码短信
URL_RESERT_PASSWORD = BASE_URL + "reset_pass"  # 重置密码
URL_GET_USER_INFO = BASE_URL + "member_info/"  # 获取个人信息
URL_POST_USER_INFO_MODIFY = BASE_URL + "member_info/modify"  # 修改个人信息
URL_REFREN_TOKEN_TIME = BASE_URL+"combo/123"#保持token有效
URL_FILE_UPLOADABLE =BASE_URL+"file_upload"#
# </editor-fold>

#<editor-fold desc="ipfs">
URL_GET_AES_KEY="http://127.0.0.1:9984/api/v0/aes/key/random"
URL_FILE_PACK="http://127.0.0.1:9984/api/v0/pack"

# </editor-fold>

# </editor-fold>


'''Mehtod '''

import requests  # url网络请求
import json
import logging
from datetime import datetime
from uploadtask.MD5Endcoder import MD5endcoder
from uploadtask.User import SaveUserInfo,GetUserInfo
import FileUtils
#*********************************************************

#<editor-fold desc='请求方法'>
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}


#<editor-fold desc="GET请求方法">

def GetForNet(url,retunjson=True,headers=headers):
    requestloginfo(url, "GET", headers)
    try:
        with requests.get(url,headers=headers) as r:
           return request_data_parse(r, url,retunjson)
    except Exception as e:
         HttpExceptionInfo(url, e)
         return None

#</editor-fold>

#<editor-fold desc="POST请求方法">

def PostForNet(url, data_json,headers=headers,files=None):
    requestloginfo(url,"POST",headers,data_json)
    try:
       if not files:
          with requests.post(url, data=data_json, headers=headers,files=files) as r:
              return request_data_parse(r, url)
       else:
           with requests.post(url, data=data_json, headers=headers) as r:
               return request_data_parse(r, url)

    except Exception as e:
         HttpExceptionInfo(url, e)
         return None

#</editor-fold>

#<editor-fold desc="PUT请求方法">

def PutForNet(url,headers=headers):
    requestloginfo(url, "PUT", headers)
    try:
        with requests.put(url,headers=headers) as r:
           return request_data_parse(r, url)
    except Exception as e:
         HttpExceptionInfo(url, e)
         return None

#</editor-fold>

#<editor-fold desc="请求返回数据解析方法">

def request_data_parse(r,url="",retunjson=True):
    status_code = r.status_code
    print(datetime.now(), "HTPP返回状态吗：", status_code)
    if status_code == REQUEST_SUCESS_CODE:
        if retunjson==False:
            return r.content.decode("utf-8")
        # 请求成功
        data = r.json()
        code= data["code"]
        if code == REQUEST_SUCESS_CODE:
            print(datetime.now(), '返回数据：', data)
            return data
        else:
            ServieceErroInfo(url,code,data["message"])
            return None
    else:  # http 错误码处理 #
        HttpCodeErro(status_code, url)

#</editor-fold>



#<editor-fold desc="Http 错误">

#<editor-fold desc="Service 错误">
def ServieceErroInfo(url,code,message):
    print(datetime.now(),"Servie Erro","url:",url)
    print(datetime.now(),"服务器返回错误：",message,"code:",code)
#</editor-fold>

#<editor-fold desc="HttpCodeErro  Http Code">
def HttpCodeErro(status_code,url):
    print(datetime.now(), "未请求成功url", url)
    print(datetime.now(), "Http错误状态吗：", status_code)

#</editor-fold>

#<editor-fold desc="Http请求异常打印   系统">
def HttpExceptionInfo(url,e):
    print(datetime.now(), "未执行url", url)
    print(datetime.now(), "原因：", e)
#</editor-fold>

#</editor-fold>

#<editor-fold desc="requestloginfo">
def requestloginfo(url,method,headers=headers,params_json=None):
    print(datetime.now(), "**********"+method+"**********")
    print(datetime.now(), "url:", url)
    print(datetime.now(), "mehtod:", method)
    print(datetime.now(), "headers:", headers)
    if method == "POST":
       print(datetime.now(), "data:", params_json)

#</editor-fold>

#</editor-fold>

#***************************http 业务方法*********************************************************

#<editor-fold desc="登陆方法">

def login(mobile, password):
    pwd = MD5endcoder(password)
    params = dict(mobile=mobile, password=pwd)
    data = PostForNet(URL_LOGIN, json.dumps(params))
    if not data==None:
        access_token = data["data"]["access_token"]
        refresh_token = data["data"]["refresh_token"]
        user_id = data["data"]["user_id"]
        app_id = data["data"]["app_id"]
        clienttype = data["data"]["clienttype"]
        company_id = data["data"]["company_id"]
        rootuser = user_id == company_id
        #保存userinfo
        data["username"]=mobile
        data["password"]=password
        data["rootuser"]=rootuser
        SaveUserInfo(mobile,data)
        print("data is ",data)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user_id,
            'app_id': app_id,
            'clienttype': clienttype,
            'company_id': company_id,
            'rootuser': rootuser
        }
    else: return  None

#</editor-fold>



#<editor-fold desc="GetToken">
def GetToken(chekloacl=False,config_filePath=None):
    if config_filePath==None:
       config_filePath='config.json'
    if FileUtils.CheckFileExists(config_filePath):
        # print(headers)
        with open(config_filePath) as f:
            config = json.load(f)
        print(config)
        mobile = config["userinfo"]["username"]
        password = config["userinfo"]["password"]
        if chekloacl:
           if FileUtils.CheckFileExists("/userinfo/"+mobile):
               return  GetUserInfo(mobile)
        userinfo = login(mobile, password)
        if  userinfo == None:
            return None
        else:
            print(userinfo)
            print(userinfo["access_token"])
            return userinfo
    else:
        print(datetime.now(),"未找到配置文件")
        return None

#</editor-fold>

if __name__ == '__main__':
    GetToken()

