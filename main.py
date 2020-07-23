from  requestjsondata import gethtmlcontent #url请求网络
from  requestjsondata import getftphtmlcontent #ftp请求网络
import  time
import  os
import re
from  datetime import  datetime
from lxml import  etree
import  ast
from concurrent.futures import ThreadPoolExecutor #携程 线程池
from FTPClient  import  MyFTP
from urllib.parse import urlsplit  #splittype
import  FileUtils
from uploadtask.main import UserLogin,LogUserInfo

import math
# from urllib.parse import (urlparse, urlsplit, urljoin, unwrap, quote, unquote,splittype, splithost, splitport, splituser, splitpasswd,splitattr, splitquery, splitvalue, splittag, to_bytes,unquote_to_bytes, urlunparse)

def not_empty(s):
    return s and s.strip()

def getfilediesize(url):
    filesize = 0  # 单位B
    html_str = gethtmlcontent(url)  # 获取html 数据
    if html_str != None:
        html = etree.HTML(html_str)
        pre = html.xpath('/html/body/pre/*')  # 节点
        contents = html.xpath('/html/body/pre/text()')  # text
        for i in range(1, len(pre)):
            item_pre = pre[i].xpath('./@href')[0]
            item_text = str.replace(contents[i], ' ', '')

            if item_pre.endswith('/'):  # 文件夹处理
                print("%s是文件夹" % item_pre)
                size =getfilediesize(url+'/'+item_pre)
            else:  # 文件处理
                time_index = item_text.index(':') + 3
                item_time = item_text[:time_index]
                item_filesize = item_text[time_index:]
                print(i, item_pre, item_time, item_filesize)
                size = int(re.findall(r'\b\d+\b', item_filesize)[0])
                with open("file.txt", "a") as f:
                    f.write('%d %s %s %d\n' % (i, item_pre, item_time, size))

            filesize += size
    else: print('获取失败')
    return  filesize

def checkurlisloaed(url):
    with open("end.txt",'r',encoding='utf-8') as f:
       for line in f.readlines():
           res=line.strip().split(":")
           #print('res .len',len(res))
           print(res)
           lurl=res[0]+':'+res[1]
           print('lurl',lurl)
           size = res[2]
           if lurl==url:
               return  True,int(size)
    return  False,0

def getfilediesize02(url):
    filesize = 0  # 单位B
    global  filecount
    global  savecount
    if os.path.exists('end.txt'):
        res=checkurlisloaed(url)
        if res[0]:
            return res[1]
    while True:
       ftp_str = getftphtmlcontent(url)  # 获取html 数据
       if ftp_str!=None:
         break
       time.sleep(1)

    if ftp_str=='':
        return  filesize

    if ftp_str != None:
       data=str.split(ftp_str,'\r\n')
       print(datetime.now(),'该文件目下文件数量：',len(data))
       for i in range(len(data)-1):
         item_str = data[i]
         # print(i,item_str)
         item_list = list(filter(not_empty, item_str.split(' ')))
         print(datetime.now(),'item 数据',len(item_list), item_list)
         name = (item_list[-1])
         if item_str.startswith('d'):  # 文件夹处理
             print(datetime.now(),"%s是文件夹" % name,"%s%s"%(url,name))
             size =getfilediesize02(url+'/'+name)
             print(datetime.now(),"文件夹%s"%name,"size is %d"%size)

         else:  # 文件处理
          filecount+=1
          item_time=item_list[5:8]
          size = int(item_list[4])
          print(datetime.now(), "%s是文件" % name, "%s/%s" % (url, name))
          if filecount>savecount:
           with open("./file_ftp09.txt", "a",encoding='utf-8') as f:
               content='%d %s %s %s/%s %d\n' % (i, name, item_time, url, name, size)
               print(datetime.now(),'写入内容：',content)
               f.write(content)

         filesize += size
    else:
     print(url,'获取失败')
    print('')
    # wit 记录已经完成文件夹
    with open('end.txt','a',encoding='utf-8') as f:
        f.write(url+":"+str(filesize)+'\n')
    return  filesize

def parsefileinfo(fileinfo):
    line = fileinfo.replace('\n', '')
    iteminfo = line.split(" ")
    if len(iteminfo)<7:
        return False
    filesize = iteminfo[-1]
    filename = iteminfo[1]
    fileurl  = iteminfo[-2]

    datelist = ast.literal_eval(iteminfo[2] + iteminfo[3] + iteminfo[4])
    filedate = " ".join(datelist)
    print(line, filename, filedate, filesize, len(iteminfo))
    return  True,filename,filedate,filesize,fileurl

if __name__ == '__main__':
    config_filePath="uploadtask/config.json"

    UserLogin(config_filePath)
    LogUserInfo()
    # import sys
    # sys.exit(0)


    taskcount =100
    mult_taskcount =taskcount
    threadPool = ThreadPoolExecutor(max_workers=taskcount, thread_name_prefix="ftp_down_task_")
    print("hello python")
    filecount = 0
    savecount = -1
    dirsize =0
    start_time =datetime.now()
    print("请求开始",start_time)
    # ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp
    urls=['ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502',
          'ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp',
          'ftp://download.big.ac.cn/Genome/Viruses/Coronaviridae'
          ]

    # dirsize =getfilediesize(urls[0])
    # dirsize = getfilediesize02(urls[1])

    #<editor-fold dec="config">
    remoteport = 21
    loginname = "anonymous"
    loginpassword = '' #ftp 匿名登陆密码
    block_size=200#1024**3 #1G part_file_size
    del_part_file_able=True #是否删除part文件
    #</editor-fold>


    with open('file_ftp08.txt','r',encoding='utf-8') as  f:
        for line in f.readlines():
            lineinfo= parsefileinfo(line)
            if lineinfo[0]:
               filename=lineinfo[1]
               filedate=lineinfo[2]
               filesize=int(lineinfo[3])
               fileurl =lineinfo[4]
               print(datetime.now(),filename,filedate,filesize,fileurl)

               # 截取ftp url
               v = urlsplit(fileurl)
               print("scheme", v.scheme)
               print("netloc", v.netloc)
               print("port", v.port)
               remoteHost =v.netloc
               remotePath=v.path#[1:]
               print("remotePath",remotePath)
               localPath=v.netloc + v.path


               if  filesize< block_size:
                   FileUtils.Mkdirs(localPath)
                   print(datetime.now(),"file size is",filesize,'普通断点续传文件')
                   # (remoteHost =remoteHost, remoteport=21, loginname="anonymous", loginpassword='', remotePath=remotePath, localPath=localPath)
                   threadPool.submit(MyFTP().download,remoteHost,remoteport,loginname,loginpassword,remotePath,localPath)
               else :
                   print(datetime.now(),"file size is",filesize,'需要分片断点续传文件')
                   # remoteHost, remoteport, loginname, loginpassword, remotePath, localPath, filename, filesize, block_size, del_part_file_able, mult_taskcount = None
                   threadPool.submit(MyFTP().downmultfile, remoteHost, remoteport, loginname, loginpassword, remotePath,
                                     localPath,filename,filesize,block_size,del_part_file_able)
                                     # localPath,filename,filesize,block_size,del_part_file_able,mult_taskcount=mult_taskcount)



            break
    threadPool.shutdown(wait=True)



    # print("scheme",v.scheme)
    end_time =datetime.now()
    times =end_time-start_time
    print(end_time,"执行结束",'filesize=',dirsize,'耗时：',times)