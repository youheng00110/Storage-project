#include <stdio.h>
#include <math.h>
int main(void){
    int i,a,b,c,temp;
    while(1){
        printf("�������������Fibonacci���е�����������0�˳�����");
        scanf("%d",&i);
        if(i==0){
            printf("���˳�\n");
            break;
        }
        a=0,b=1;
        printf("Fibonacci���е�ǰ%d��Ϊ��\n",i);
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