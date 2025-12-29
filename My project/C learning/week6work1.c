<<<<<<< HEAD
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
=======
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
>>>>>>> 02297afcddcad879a453ccb4c6175697dc0edd72
}