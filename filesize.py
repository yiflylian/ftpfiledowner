filesize_sum =0
with open('./file_ftp06.txt','r') as f:
    for line in f.readlines():
        #line.strip().split(' ')[-1]
        filesize_sum += int(line.strip().split(' ')[-1])
print(filesize_sum)