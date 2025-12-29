<<<<<<< HEAD
count=0
average=0
summ=0
num=(input("请输入一个正整数进行累加,完成输入done:"))
while True:
        try:
            if num!="done":
                count+=1
                summ+=int(num)
                num=(input("请输入一个正整数进行累加,完成输入done:"))
            if num=="done":
                average=summ/count
                print("总个数为：",count)
                print("总和为:",summ)
                print("平均值为:",average)
                break
        except:
            print("请输入正确的数字")
            num = (input("请输入一个正整数进行累加,完成输入done:"))
            
            

  
=======
count=0
average=0
summ=0
num=(input("请输入一个正整数进行累加,完成输入done:"))
while True:
        try:
            if num!="done":
                count+=1
                summ+=int(num)
                num=(input("请输入一个正整数进行累加,完成输入done:"))
            if num=="done":
                average=summ/count
                print("总个数为：",count)
                print("总和为:",summ)
                print("平均值为:",average)
                break
        except:
            print("请输入正确的数字")
            num = (input("请输入一个正整数进行累加,完成输入done:"))
            
            

  
>>>>>>> 44a48492f18c5a7bca21911a42f08715eef71094
        