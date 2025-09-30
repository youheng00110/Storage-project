counts=dict()
lines=input("请输入一段文字：")
words=lines.split()
for word in words:
    counts[word]=counts.get(word,0)+1
print("各单词出现的次数为：",counts)