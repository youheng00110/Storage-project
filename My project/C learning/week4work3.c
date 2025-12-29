#include <stdio.h>
int main(void){
<<<<<<< HEAD
    int i,j;
    for(i=1;i<=9;i++){
        for(j=1;j<=i;j++){
            printf("%d*%d=%-2d\t ",j,i,i*j);
        }
        printf("\n");
    
    }
 
=======
    int i;
    for(i=1;i<=9;i++){
        int j;
        for (j=1;j<=i;j++){
        printf("%d*%d=%-2d\t",i,j,i*j);
        }
        printf("\n");
    }
>>>>>>> 2a2a897780e0998a25d94e5a9900ae74fb3cc3cd
    return 0;
}