#include <stdio.h>
/*int main(){
    int i;
    while(1){
    printf("input a number(-1break):\n");
    scanf("%d",&i);
    if(i<0){
        break;
    }
    if(i%2==0){
        if(i%3==0){
            if(i%5==0){
                printf("Divisible by 2, 3, and 5\n");
            }
            else{
                printf("Divisible by 2 and 3\n");
            }
        }
        else if(i%5==0){
            printf("Divisible by 2 and 5\n");
        }
        else{
            printf("Divisible by 2\n");
        }
    }
    else if(i%3==0){
        if(i%5==0){
            printf("Divisible by 3 and 5\n");
        }
        else{
            printf("Divisible by 3\n");
        }
    }
    else if(i%5==0){
        printf("Divisible by 5\n");
    }
    else{
        printf("Not divisible by 2, 3, or 5\n");
    }
   
}
return 0;
}
*/
/*
int main(){
    int i,j,a,sum=0,mult=1,aver=0,temp=0;
    printf("Input a number:\n");
    scanf("%d",&a);
    for(i=1;i<=a;i+=2){
        sum+=i;
    }
    for(j=3;j<=a;j+=3){
        mult*=j;
    }
    for(i=0;i<=a;i+=2){
        aver+=i;
        temp++;
    }
    printf("\nSum=%d\n",sum);
    printf("Product=%d\n",mult);
    printf("Average=%d\n",aver/temp);
    return 0;
}
*/

