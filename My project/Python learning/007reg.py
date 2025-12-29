import re
with open('test1.txt', 'r', encoding='utf-8') as hand:
    for line in hand:
        if re.findall(r"^\s*From:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",line):
            print(line)