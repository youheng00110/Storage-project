file=input("请输入文件名：")
handle=open(file)
counts=dict()
for lines in handle:
    words=lines.lstrip().split()
    for word in words:
        counts[word]=counts.get(word,0)+1
lst2=list()
bigword=None
bigcount=None
for word,count in counts.items():
    if bigcount is None or count>bigcount:
        bigcount=count
        bigword=word
for word,count in counts.items():
    newtuple=(count,word)
    lst2.append(newtuple)
lst2=sorted(lst2,reverse=True)
for count,word in lst2[:5]:
    print("排名前五的单词分别为：",word,count)
print("最多的单词是：",bigword,"\n出现",bigcount,"次\n""各单词出现的次数为：",counts)