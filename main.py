from  requestjsondata import gethtmlcontent #url请求网络
from  requestjsondata import getftphtmlcontent #ftp请求网络
import  time
import  os
import re
from  datetime import  datetime
from lxml import  etree


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


filecount =0
savecount =-1
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

print("hello python")
start_time =datetime.now()
print("请求开始",start_time)
# ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp
urls=['http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502',
      'ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp',
      'ftp://download.big.ac.cn/Genome/Viruses/Coronaviridae'
      ]

# dirsize =getfilediesize(urls[0])
dirsize = getfilediesize02(urls[1])
end_time =datetime.now()
times =end_time-start_time
print(end_time,"执行结束",'filesize=',dirsize,'耗时：',times)