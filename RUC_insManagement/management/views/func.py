import datetime
# 用来定义一些其他地方用得到的函数
def str2time(strs):
    time=''
    for i in range(24):
        if strs[i] == '1':
            time += str(i)+':00~' +str(i+1)+':00 ; '  
    return time
def date2str(d):
    return d.strftime('%Y-%m-%d')
def str2date(s):
    return datetime.datetime.strptime(s,'%Y-%m-%d')
