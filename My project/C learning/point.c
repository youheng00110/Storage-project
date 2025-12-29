#include<stdio.h>
#include<stdlib.h>
/*
int main(){
    int **a;
    a=(int**)malloc(5*sizeof(int*));
    for(int i=0;i<5;i++){
        a[i]=(int*)malloc((i+1)*sizeof(int));
    }
}*/
int my_strlen(char* s){
    int n=0;
    while(*s!='\0'){
        n++;
        s++;
    }
    printf("%d\n",n);
    return n;
}
int swap(int*a,int*b){
    int t;
    t=*a;
    *a=*b;
    *b=t;
    printf("%d\t%d\n",*a,*b);
    return 0;
}
int main(){
    int x=10;
    int y=20;
    swap(&x,&y);
    char *s={"helloworld!"};
    my_strlen(s);
    return 0;

}