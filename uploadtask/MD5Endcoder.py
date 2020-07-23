'''md5加密'''
Salt="#$^^xsAd.." #盐



def MD5endcoder(md5_str):
    from hashlib import md5
    md5 = md5()
    data=md5_str + Salt
    md5.update(data.encode('utf-8'))
    result=md5.hexdigest()
    print(result)
    return  result


if __name__ == '__main__':
    MD5endcoder()
