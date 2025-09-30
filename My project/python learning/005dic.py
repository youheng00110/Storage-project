file=input("请输入文件名：")
handle=open(file)
counts=dict()
for lines in handle:
    words=lines.lstrip().split()
    for word in words:
        counts[word]=counts.get(word,0)+1
bigword=None
bigcount=None
for word,count in counts.items():
    if bigcount is None or count>bigcount:
        bigcount=count
        bigword=word
print("各单词出现的次数为：",counts,"\n","最多的单词是：",bigword,"\n出现",bigcount,"次")