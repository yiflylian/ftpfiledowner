content =r'''
-r--r--r--   1 ftp      anonymous      861 Feb 13 17:10 Aspera_download_from_ftp.README
-r--r--r--   1 ftp      anonymous      683 Sep 11  2015 CHANGELOG
-r--r--r--   1 ftp      anonymous     3451 May  5 13:42 README.ftp_structure
-r--r--r--   1 ftp      anonymous     3070 Jul  1  2016 README.s3_structure
-r--r--r--   1 ftp      anonymous      205 Aug  2  2019 README_giab_URL_replacement2019.txt
-r--r--r--   1 ftp      anonymous 19392956 Apr 29 16:58 current.tree
-r--r--r--   1 ftp      anonymous 19207413 Apr 29 16:58 giab_s3_urls

dr-xr-xr-x 1073741824 ftp      anonymous        0 Jun 23 20:24 data
dr-xr-xr-x 1073741824 ftp      anonymous        0 Feb 21 19:58 data_indexes
dr-xr-xr-x 1073741824 ftp      anonymous        0 Sep 11  2015 changelog_details
dr-xr-xr-x 1073741824 ftp      anonymous        0 Mar 11 14:37 release
dr-xr-xr-x 1073741824 ftp      anonymous        0 Jun 23 20:24 technical
dr-xr-xr-x 1073741824 ftp      anonymous        0 Jan 15  2014 tools
dr-xr-xr-x 1073741824 ftp      anonymous        0 Jun 15  2019 use_cases'''
content_b =b'-r--r--r--   1 ftp      anonymous      861 Feb 13 17:10 Aspera_download_from_ftp.README\r\n-r--r--r--   1 ftp      anonymous      683 Sep 11  2015 CHANGELOG\r\n-r--r--r--   1 ftp      anonymous     3451 May  5 13:42 README.ftp_structure\r\n-r--r--r--   1 ftp      anonymous     3070 Jul  1  2016 README.s3_structure\r\n-r--r--r--   1 ftp      anonymous      205 Aug  2  2019 README_giab_URL_replacement2019.txt\r\ndr-xr-xr-x 1073741824 ftp      anonymous        0 Sep 11  2015 changelog_details\r\n-r--r--r--   1 ftp      anonymous 19392956 Apr 29 16:58 current.tree\r\ndr-xr-xr-x 1073741824 ftp      anonymous        0 Jun 23 20:57 data\r\ndr-xr-xr-x 1073741824 ftp      anonymous        0 Feb 21 19:58 data_indexes\r\n-r--r--r--   1 ftp      anonymous 19207413 Apr 29 16:58 giab_s3_urls\r\ndr-xr-xr-x 1073741824 ftp      anonymous        0 Mar 11 14:37 release\r\ndr-xr-xr-x 1073741824 ftp      anonymous        0 Jun 23 20:57 technical\r\ndr-xr-xr-x 1073741824 ftp      anonymous        0 Jan 15  2014 tools\r\ndr-xr-xr-x 1073741824 ftp      anonymous        0 Jun 15  2019 use_cases\r\n'


def not_empty(s):
    return s and s.strip()

#data=str.split(content_b.decode('utf-8'),'\r\n')
# print(len(data))
#for i in range(len(data)-1):
       #  item_str = data[i]
         # print(i,item_str)
         # print(len(item_str.split(' ')),item_str.split(' '))
      #   item_list = list(filter(not_empty, item_str.split(' ')))
       #  print(len(item_list), item_list)
       #  name =(item_list[-1])

        # if item_str.startswith('d'):  # 文件夹处理
         #    pass
          # print("%s是文件夹" % name)
                # size =getfilediesize(url+'/'+item_pre)
          # print(len(item_str.split(' ')),item_str.split(' '))
        # else:  # 文件处理
            # print("%s是文件" % name)
            # item_list=list(filter(not_empty,item_str.split(' ')))
            # print(len(item_list), item_list)
          #  item_time = item_list[5:8]
         #   print(item_time)
                # time_index = item_text.index(':') + 3
                # item_time = item_text[:time_index]
                # item_filesize = item_text[time_index:]
       #          print(i, item_pre, item_time, item_filesize)
       #          size = int(re.findall(r'\b\d+\b', item_filesize)[0])
       #          with open("file.txt", "a") as f:
       #              f.write('%d %s %s %d\n' % (i, item_pre, item_time, size))
       #
       #      filesize += size
from  requestjsondata    import getftphtmlcontent
from datetime import datetime
import  os
import  json
if __name__ == '__main__':
# print(os.path.curdir)
# print('end')
    print(os.path.exists('end.txt'))
    with open('end.txt','r',encoding='utf-8') as f:
        for line in f.readlines():
            res = line.strip().split(":")
            if len(res) ==3:
                lurl = res[0] + ":" + res[1]
                size = int(res[2])
                with open('02_enddir.json','a',encoding='utf-8') as tf:
                    data = json.dumps(dict(url=lurl, size=size)).strip()
                    tf.write(data+",")



    # url ='ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG003_NA24149_father/UCSC_Ultralong_OxfordNanopore_Promethion'
    # ftp_str=getftphtmlcontent(url)
    # data = str.split(ftp_str, '\r\n')
    # print(data)
    # print( '该文件目下文件数量：', len(data))
    # for i in range(len(data) - 1):
    #     item_str = data[i]
    #     item_list = list(filter(not_empty, item_str.split(' ')))
    #     print(datetime.now(), 'item 数据', len(item_list), item_list)
    #     name = (item_list[-1])
    #     if item_str.startswith('d'):  # 文件夹处理
    #         print(datetime.now(), "%s是文件夹" % name, "%s/%s" % (url, name))
    #
    #
    #     else:  # 文件处理
    #
    #         item_time = item_list[5:8]
    #         size = int(item_list[4])
    #         print(datetime.now(), "%s是文件" % name, "%s/%s" % (url, name))
    #         with open("./file_ftp07.txt", 'a',encoding='utf-8') as f:
    #                 content = '%d %s %s %s/%s %d\n' % (i, name, item_time, url, name, size)
    #                 print(datetime.now(), '写入内容：', content)
    #                 f.write(content)