<<<<<<< HEAD
#include <stdio.h>
int main(){
    int a[20]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,1,19};
    int i,index;
    index=1;
    for(i=0;i<20;i++){
        if(a[i]==index){
            printf("a[%d]=%d\n",i,a[i]);
            break;
        }
        else{
            printf("not found\n");
            break;
        }

    }
    for(i=19;i>=0;i--){
        if(a[i]==index){
            printf("a[%d]=%d\n",i,a[i]);
            break;
        }
        else{
            printf("not found\n");
            break;
        }

    }
    return 0;
=======
#include <stdio.h>
int main(){
    int a[20]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,1,19};
    int i,index;
    index=1;
    for(i=0;i<20;i++){
        if(a[i]==index){
            printf("a[%d]=%d\n",i,a[i]);
            break;
        }
        else{
            printf("not found\n");
            break;
        }

    }
    for(i=19;i>=0;i--){
        if(a[i]==index){
            printf("a[%d]=%d\n",i,a[i]);
            break;
        }
        else{
            printf("not found\n");
            break;
        }

    }
    return 0;
>>>>>>> 02297afcddcad879a453ccb4c6175697dc0edd72
}