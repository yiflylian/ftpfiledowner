#encoding=utf-8
'''
Created on 2012-3-14

@author: cooler
'''
from ftplib import FTP
import sys
import os.path
import time
from uploadtask.main import UploadFile
import math
import  FileUtils
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor #携程 线程池


class MyFTP(FTP):
    '''''
    conncet to FTP Server
    '''
    def __init__(self):
        print ('make a object')
    def ConnectFTP(self,remoteHost,remoteport,loginname,loginpassword):
        ftp=FTP()
        try:
            ftp.connect(remoteHost,remoteport,600,source_address=None)
            print('success')
        except Exception as e:
            print("conncet failed1",e)
            return (0,'conncet failed')
        else:
            try:
                ftp.login(loginname,loginpassword)
                print ('login success')
            except:
                print ('login failed')
                return (0,'login failed')
            else:
                print ('return 1')
                return (1,ftp)
    #断点续传
    def download(self,remoteHost,remoteport,loginname,loginpassword,remotePath,localPath):
        #connect to the FTP Server and check the return
        res = self.ConnectFTP(remoteHost,remoteport,loginname,loginpassword)
        if(res[0]!=1):
            print (res[1] )
            sys.exit()

        #change the remote directory and get the remote file size
        ftp=res[1]
        ftp.set_pasv(0)
        dires = self.splitpath(remotePath)
        print('dires',dires)
        if dires[0]:
            ftp.cwd(dires[0])
        remotefile=dires[1]
        print (dires[0]+' '+ dires[1]  )
        fsize=ftp.size(remotefile)

        print('fsize  is ',fsize)
        # return

        if fsize==0 :
            return

        #check local file isn't exists and get the local file size
        lsize=0
        if os.path.exists(localPath):
            lsize=os.stat(localPath).st_size

        if lsize >= fsize:
            print('local file is bigger or equal remote file' )

            return
        blocksize=1024
        cmpsize=lsize
        ftp.voidcmd('TYPE I')
        conn = ftp.transfercmd('RETR '+remotefile,lsize)
        lwrite=open(localPath,'ab')
        while True:
          try:
            data=conn.recv(blocksize)
            if not data:
                break
            lwrite.write(data)
            cmpsize+=len(data)
            print ('\b'*30,'download process:%.2f%%'%(float(cmpsize)/fsize*100), )
          except Exception as e:
              print('erro:',e)
        lwrite.close()
        ftp.voidcmd('NOOP')
        ftp.voidresp()
        conn.close()
        ftp.quit()
    def downloadbymulti_thread(self,remoteHost,remoteport,loginname,loginpassword,remotePath,localPath,start_size,filesize):
        print(localPath,"start")
        #connect to the FTP Server and check the return
        res = self.ConnectFTP(remoteHost,remoteport,loginname,loginpassword)
        if(res[0]!=1):
            print (datetime.now(),localPath,res[1] ,'登陆ftp失败')
            return
            # sys.exit()

        #change the remote directory and get the remote file size
        ftp=res[1]
        ftp.set_pasv(0)
        dires = self.splitpath(remotePath)
        print('dires',dires)
        if dires[0]:
            while True:
             try:
              ftp.cwd(dires[0])
              break
             except Exception as e:
                print(datetime.now(),localPath,'erro:',e)
                print(datetime.now(),localPath,"请检查网络路径是否存在")
                return


        remotefile=dires[1]
        print (dires[0]+' '+ dires[1]  )
        fsize=ftp.size(remotefile)

        print('fsize  is ',fsize)
        # return

        if fsize==0:
            print("文件size 为 0")
            return

        #check local file isn't exists and get the local file size
        lsize=0
        if os.path.exists(localPath):
            lsize=os.stat(localPath).st_size
            start_size=+lsize
            print(datetime.now(),localPath,'start_size',start_size)

        if lsize >= filesize:
            print(datetime.now(),localPath,'local file is bigger or equal remote file' )
            print(datetime.now(),localPath,localPath,'本地文件已存在')
            return
        # lblocksize=100
        lblocksize = 1024 * 1024
        cmpsize=lsize
        ftp.voidcmd('TYPE I')
        conn = ftp.transfercmd('RETR '+remotefile,start_size)
        lwrite=open(localPath,'ab')
        while True:
          try:
            print(datetime.now(),localPath,'cmpsize',cmpsize)
            if cmpsize>=filesize:
                print(datetime.now(),localPath,'data', "block_size end", not data)
                break
            fsize=filesize - cmpsize
            if fsize<lblocksize:
                lblocksize = fsize
            data=conn.recv(lblocksize)
            if not data:
                print(datetime.now(),localPath,'data',"not data :",not data)
                break
            lwrite.write(data)
            lwrite.flush()
            cmpsize+=len(data)
            print (datetime.now(),localPath,'\b'*30,'download process:%.2f%%'%(float(cmpsize)/filesize*100), )
            # print ('\b'*30,'download process:%.2f%%'%(float(cmpsize)/fsize*100), )
          except Exception as e:
              print(datetime.now(),localPath,'erro:',e)
        lwrite.close()
        ftp.voidcmd('NOOP')
        ftp.voidresp()
        conn.close()
        ftp.quit()
    def upload(self,remotehost,remoteport,loginname,loginpassword,remotepath,localpath,callback=None):
        if not os.path.exists(localpath):
            print ("Local file doesn't exists" )
            return
        self.set_debuglevel(2)
        res=self.ConnectFTP(remotehost,remoteport,loginname,loginpassword)
        if res[0]!=1:
            print (res[1]  )
            sys.exit()
        ftp=res[1]
        remote=self.splitpath(remotepath)
        ftp.cwd(remote[0])
        rsize=0
        try:
            rsize=ftp.size(remote[1])
        except:
            pass
        if (rsize==None):
            rsize=0
        lsize=os.stat(localpath).st_size
        if (rsize==lsize):
            print ('remote filesize is equal with local' )
            return
        if (rsize<lsize):
            localf=open(localpath,'rb')
            localf.seek(rsize)
            ftp.voidcmd('TYPE I')
            datasock,esize=ftp.ntransfercmd("STOR "+remote[1],rsize)
            cmpsize=rsize
            while True:
                buf=localf.read(1024)
                if not len(buf):
                    print ('\rno data break')
                    break
                datasock.sendall(buf)
                if callback:
                    callback(buf)
                cmpsize+=len(buf)
                print ('\b'*30,'uploading %.2f%%'%(float(cmpsize)/lsize*100), )
                if cmpsize==lsize:
                    print ('\rfile size equal break' )
                    break
            datasock.close()
            print ('close data handle')
            localf.close()
            print ( 'close local file handle' )
            ftp.voidcmd('NOOP')
            print ('keep alive cmd success')
            ftp.voidresp()
            print ('No loop cmd'  )
            ftp.quit()
    def splitpath(self,remotepath):
        position=remotepath.rfind('/')
        return (remotepath[:position+1],remotepath[position+1:])
    def downmultfile(self,remoteHost,remoteport,loginname,loginpassword,remotePath,localPath,filename,filesize,block_size ,del_part_file_able,mult_taskcount=None):
        mult_file_name = FileUtils.GetFileName(localPath)
        print(mult_file_name,)
        FileUtils.Mkdirs(mult_file_name + "/")

        part_file_count = math.ceil(float(filesize) / block_size)  # 分片文件数
        part_file_end = part_file_count - 1
        part_file_names = list()
        if mult_taskcount == None:
            mult_taskcount =  part_file_count
        mult_threadPool = ThreadPoolExecutor(max_workers=mult_taskcount, thread_name_prefix="mult_ftp_down_task_")
        for i in range(part_file_count):
            part_file_name = mult_file_name + "/" + filename + "_part" + str(i)
            part_file_names.append(part_file_name)
            part_file_start_size = i * block_size
            part_file_size = block_size

            if i == part_file_end:
                part_filesize = filesize - part_file_start_size

            mult_threadPool.submit(MyFTP().downloadbymulti_thread, remoteHost, remoteport, loginname,
                                   loginpassword, remotePath, part_file_name, part_file_start_size, part_file_size)

        mult_threadPool.shutdown(wait=True)
        print(datetime.now(), filename, "part文件全部下载完毕")
        #
        print(datetime.now(), filename, "开始合并")

        FileUtils.MergFile(part_file_names, localPath, filesize, block_size, part_file_count, part_file_end,
                           del_part_file_able, mult_file_name)  # del
        #开始上传文件
        print(datetime.now(), filename, "开始上传")
        UploadFile(filename,filesize,localPath,localPath)

if __name__=='__main__':
    # url = 'ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.chr22_GRCh38_sites.20170504.vcf.gz'  # 2m
    # url  ='ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/README_chrMT_phase3_callmom.md'
    # name = 'test.gz'
    # lf = MyFTP()
    # # # lf.ConnectFTP(remoteip="ftp.1000genomes.ebi.ac.uk",remoteport=21,loginname="anonymous",loginpassword='')
    # lf.download(remoteHost="ftp.1000genomes.ebi.ac.uk",remoteport=21,loginname="anonymous",loginpassword='',remotePath='./vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.chr22_GRCh38_sites.20170504.vcf.gz',localPath='target.gz')
    # sys.exit(0)
    # remoteHost = "ftp.1000genomes.ebi.ac.uk"
    # remoteHost = "ftp-trace.ncbi.nlm.nih.gov" #ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/changelog_details/
    # remotePath = '/vol1/ftp/release/20130502/README_chrMT_phase3_callmom.md'  # 2m 847 /vol1/ftp/release/20130502/README_chrMT_phase3_callmom.md
    # remotePath = 'vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.chr22_GRCh38_sites.20170504.vcf.gz'  # 2m
    # remotePath = 'giab/ftp/changelog_details/20150716_new'  # 5.8m  6031416
    # lf = MyFTP()
    # # lf.ConnectFTP(remoteip="ftp.1000genomes.ebi.ac.uk",remoteport=21,loginname="anonymous",loginpassword='')
    # lf.download(remoteHost=remoteHost, remoteport=21, loginname="anonymous", loginpassword='', remotePath=remotePath,localPath=localPath)
    # sys.exit(0)
    # 'ftp://download.big.ac.cn/Genome/Plants/Actinidia_chinensis/Kiwifruit_v1/Actinidia_chinensis.Protein.faa.gz'#

    # math.ceil()

    # filesie =float(cmpsize)

    remoteHost = "download.big.ac.cn" #ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/changelog_details/
    remoteport = 21
    loginname = "anonymous"
    loginpassword = ''

    remotePath = 'Genome/Plants/Actinidia_chinensis/Kiwifruit_v1/Actinidia_chinensis.Protein.faa.gz'  # 5.8m  6031416
    localPath = 'target11.gz'

    block_size= 1024**2
    taskcount = 5
    threadPool = ThreadPoolExecutor(max_workers=taskcount, thread_name_prefix="multi_task")
    mfilesize =3987616
    count =math.ceil(float(mfilesize)/block_size)
    print('count',count)
    # print(block_size,)
    # sys.exit(0)


    #以2m为一个文件分片下载
    end = count-1
    print('end  ',end)
    for i in range(count):
        print(i,str(i)+"-"+localPath)
        lp =str(i)+ "_" +localPath
        start_size =i*block_size
        # MyFTP().downloadbydeststart(remoteHost=remoteHost,remoteport=remoteport,loginname=loginname,loginpassword=loginpassword,remotePath=remotePath,localPath=lp,start_size=start_size)
        filesize = block_size
        if i==end:
            filesize=mfilesize-start_size

        threadPool.submit(MyFTP().downloadbymulti_thread,remoteHost,remoteport,loginname,loginpassword,remotePath,lp,start_size,filesize)
    threadPool.shutdown(wait=True)
    print('download  end')

    #合并 分片文件
    #
    # count =0
    print('Actinidia_chinensis.Protein.faa.gz size is :',os.path.getsize('Actinidia_chinensis.Protein.faa.gz'))
    print("a.gz exists ",os.path.exists("a.gz"))
    if os.path.exists("a.gz"):
        os.remove('a.gz')
    print("a.gz exists ",os.path.exists("a.gz"))


    # sys.exit(0)


    with open('a.gz', 'ab',) as f:
       for i  in range(count):
         filename=str(i)+ "_" +localPath
         print(filename)
         with open(filename,'rb',) as lf:
               lf.seek(0)
               print('count', count)
               print('i', i)
               print('count-1', count-1)
               print('i==(count-1)', i==(count-1))
               if i==1:
                  lsize =3987616-i*block_size
                  print("lsize ",lsize)
                  ldata = lf.read(lsize)
                  count+=len(ldata)
                  print(datetime.now(), i, 'data size', len(ldata))
               else:
                  ldata= lf.read(block_size)
                  count += len(ldata)
                  print(datetime.now(),i,'data size',len(ldata))
               f.write(ldata)
               f.flush()

    print('文件合并完成')
    import hashlib



    with open('a.gz', 'rb',) as lf:
        lf.seek(0)
        data =lf.read()
        lmd5 = hashlib.md5()
        lmd5.update(data)
        print(datetime.now(), "file a.gz  md5", lmd5.hexdigest())
        print(datetime.now(),"a.gz   count",len(data))
    with open('/Users/simple/Downloads/Actinidia_chinensis.Protein.faa.gz', 'rb') as f:

            f.seek(0)
            data = f.read()
            md5 = hashlib.md5()
            md5.update(data)
            print(datetime.now(), "sfile Actinidia_chinensis   count", len(data))
            print(datetime.now(), "sfile 20150716_new   md5", md5.hexdigest())

    # print(datetime.now(),"file  count",count)
    # print(datetime.now(),"sfile  count",6031416)



    # lf = MyFTP()
    # lf.ConnectFTP("192.168.100.237","21","cooler","123123")
    # lf.download("192.168.100.237","21","cooler","123123","/tmp/cooler/boke.rar","./cooler/boke.rar")
    # lf.upload("192.168.100.237","21","cooler","123123","/tmp/cooler/boke1.rar","./cooler/boke.rar")
# ————————————————

# 版权声明：本文为CSDN博主「cooler00100」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/cooler00100/java/article/details/84168240