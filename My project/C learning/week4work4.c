#include <stdio.h>
#include <math.h>
int main(void){
    int i,a;
    while(1) { 
        printf("�����������жϵ���������0�˳�����");
        scanf("%d",&i);
        
        if (i == 0) { 
            printf("���������\n");
            break;
        }
        
        if (i == 2 || i == 3) {
            printf("%d������\n",i);
        }
        else if (i < 2 || i%2==0||i%3==0){
            printf("%d��������\n",i);
        }
        else{
            int flag=1;
            for (a=5;a<=sqrt(i);a=a+6){
                if(i%a==0||i%(a+2)==0){
                    printf("%d��������\n",i);
                    flag=0;
                    break;
                }
            }
            if (flag) {
                printf("%d������\n",i);
            }
        }
        printf("------------------------\n");  
    }
    return 0;
}
