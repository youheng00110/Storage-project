#include <stdio.h>
int main(){
    char a[10];
    int i;
    for (i=0;i<10;i++){
        a[i]='j';
    }
    for (i=0;i<10;i++){
        a[i]=a[i]-32;
        printf("%c \n",a[i]);
    }
    return 0;
}