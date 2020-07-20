import requests #url网络请求
import requests_ftp#ftp网络请求
# import requests-ftp #ftp网络请求
from retrying import retry #重试
from urllib.request import urlretrieve #下载图片
import  time
import datetime
import  logging
import  json
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}

@retry(stop_max_attempt_number=3)
def getjsondata(url,headers=headers,isfirst=False):
    with requests.get(url) as r:
        # print(r.status_code)
        if r.status_code == 200:
            if isfirst:
                Link =""
                link=r.headers.get('Link')
                # print(link)
                Link+=link

                return  r.json()
            else: return  r.json()
        else: return None



@retry(stop_max_attempt_number=3)
def gethtmlcontent(url,headers=headers):
       with requests.get(url) as r:
        # print(r.status_code)
        if r.status_code == 200:
            return r.content.decode()
        else:return  None


@retry(stop_max_attempt_number=3)
def getftphtmlcontent(url):
     try:
        requests_ftp.monkeypatch_session()
        s= requests.Session()
        with s.list(url) as r:
         print(datetime.datetime.now(),'网络返回code：',r.status_code)
         if r.status_code == 226:
           content =r.content.decode(encoding = 'utf-8')
           print(datetime.datetime.now(),"content ",content)
           with open('requeste_data.txt','a',encoding='utf-8') as f:
               data= json.dumps(dict(url=url,content=content)).strip()
               f.write(data+',')
           if content ==None:
               content=''
           return  content
         else:return  None
     except Exception as e:
         logging.exception(e)
         print('erro:',e)
         return None

def cbk(a,b,c):
    '''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per=100.0*a*b/c
    if per>100:
        per=100
    print('%.2f%%' % per)

@retry(stop_max_attempt_number=3)
def ftpfiledown(url,name):
    time.sleep(1)
    start_time =datetime.datetime.now()
    print('%s开始下载时间 '%name,start_time)
    urlretrieve(url,name )
    # urlretrieve(url,name ,cbk)
    # print('下载完成')
    end_time = datetime.datetime.now()
    print('%s下载完成时间 ' % name, end_time,'耗时：',end_time-start_time)
    return








