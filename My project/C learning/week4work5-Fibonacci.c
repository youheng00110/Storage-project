#include <stdio.h>
#include <math.h>
int main(void){
    int i,a,b,c,temp;
    while(1){
        printf("输入你想结束的Fibonacci数列的项数（输入0退出）：");
        scanf("%d",&i);
        if(i==0){
            printf("已退出\n");
            break;
        }
        a=0,b=1;
        printf("Fibonacci数列的前%d项为：\n",i);
        for(c=1;c<=i;c++){
            temp=a+b;
            printf("%d\t",a);
            a=b;
            b=temp;
            if (c%5==0) {
                printf("\n");
            }
            
        }


    }
    return 0;
}