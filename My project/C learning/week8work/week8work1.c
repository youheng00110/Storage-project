# include<stdio.h>
int findmax(int a,int b,int*min,int*max){
    if(a>b){
        *max=a;
        *min=b;
        printf("max=%d\tmin=%d\n",*max,*min);
        return 1;
    }
    else{
        *max=b;
        *min=a;
        printf("max=%d\tmin=%d\n",*max,*min);
        return 0;
    }
}
int main(){
    int a=10;
    int b=39;
    int min,max;
    findmax(a,b,&min,&max);
    return 0;
}