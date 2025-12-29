#include <stdio.h>

int main(void){
/*
    int a[10],sum=0,i;
    printf("Enter 10 integers:\n");
    for(i=0;i<10;i++){
        scanf("%d",&a[i]);
        sum+=a[i];

    }
   printf("The sum is: %d\n", sum);
    */
    /*
    int a[]={51,9,62,6,15,17,32,21,51,65,2},i,j,k,t;
    for(i=0;i<9;i++){
        for (j=0;j<9-i;j++){
            if(a[j]>a[j+1]){
                k=a[j];
                a[j]=a[j+1];
                a[j+1]=k;

            }

        }
    }
    for(t=0;t<10;t++)
    printf("The sorted array is:%d\n",a[t]);
    */

    /*int a[10],i,index,address=0;
    printf("Enter 10 integers:\n");
    for (i = 0; i < 10; i++){
        scanf("%d", &a[i]);
    }
    index=a[0];
    for(i = 1; i < 10; i++){
        if (a[i]>index){
            index=a[i];
            address=i;
        }
    }
    printf("The max is:%d\n",index);
    printf("The address is:%d\n",address);*/
int a[100];
printf("输入一系列数字并用空格分开，最后输入-1结束：\n");

    int i,temp,total;
    for (i=0;i<100;i++){
        scanf("%d",&a[i]);  
        total=i;
        if(a[i]==-1) break;
    }
    for(i=0;i<total/2;i++){
        temp=a[i];
        a[i]=a[total-i-1];
        a[total-i-1]=temp;
    }
    printf("反转后的数组为：\n");
    for(i=0;i<total-1;i++){
        printf("%d ",a[i]);
    }
    printf("%d\n",a[total-1]);

     return 0;


}
