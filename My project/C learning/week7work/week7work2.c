#include <stdio.h>
int bidelve(int high,int low,int key){
    if(low>high) return -1;   // 没找到
    int mid;
    mid=(high+low)/2;
    if(mid==key){return mid;}
    else if(mid>key){return bidelve(mid-1,low,key);}
    else if(mid<key){return bidelve(high,mid+1,key);}
}
int main(){
    int high=100,low=1,key,result;
    printf("input key:\n");
    scanf("%d",&key);
    result=bidelve(high,low,key);
    printf("result%d\n", result);
}