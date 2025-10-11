#include <stdio.h>
#include <math.h>
int main(void){
    /*int a,i,c=0;
    printf("请输入一个整数：");
    scanf("%d",&a);
    for (i=1;i<=a;i++){
        c=c+i;

    printf("从1到%d和:%d",a,c);
    return 0;*/
    int a,i;
    double c=1.0;
    printf("请输入一个整数");
    scanf("%d",&a);
    for (i=1;i<=a;i++){
        c=c+(1.0/i)*pow(-1,i+1);
    }
    printf("从1到%d的交错倒数和为：%lf",a,c);
    return 0;
}