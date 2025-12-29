str=("X-DSPAM-Confidence: 0.8475") 
ipos=str.find(":")
floatnum=str[ipos+1:].lstrip()
print("其中的数字为：",float(floatnum))