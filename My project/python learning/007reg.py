import re
with open('test1.txt', 'r', encoding='utf-8') as hand:
    for line in hand:
        line=line.rstrip()
        if re.search(r"^\s*Middle English",line):
            print(line)