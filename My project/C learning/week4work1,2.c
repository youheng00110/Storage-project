#include <stdio.h>
#include <math.h>
int main(void){
    /*int a,i,c=0;
    printf("������һ��������");
    scanf("%d",&a);
    for (i=1;i<=a;i++){
        c=c+i;

    printf("��1��%d��:%d",a,c);
    return 0;*/
    int a,i;
    double c=1.0;
    printf("������һ������");
    scanf("%d",&a);
    for (i=1;i<=a;i++){
        c=c+(1.0/i)*pow(-1,i+1);
    }
    printf("��1��%d�Ľ�������Ϊ��%lf",a,c);
    return 0;
}