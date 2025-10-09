#include <stdio.h>
int main(){

/*nt a=b=c=1;
    if (++a || ++b && ++c);
    printf (" %d %d %d" , a,b,c);*/
int a,b,c;
printf("请输入想要比较的两个整数");
scanf("%d %d", &b, &c);
a=(b>c)?b:c;
printf("最大数为：%d",a);


    return 0;
}

/*
int a = b = c = 1;
if (++a || ++b && ++c)  // 
    printf(" %d %d %d\n", a,b,c); // 
*/ 