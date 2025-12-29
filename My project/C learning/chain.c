#include<stdio.h>
#include<math.h>
#include<stdlib.h>
struct innode{
    int data;
    struct innode *next;
};
int main(){
struct innode* head = NULL; //定义头指针
struct innode* p = NULL; //定义尾指针
int i;
int a[]={10,20,30,40,50};
for(i=0;i<5;i++){
    struct innode* newpot=(struct innode*)malloc(sizeof(struct innode));
    newpot->data=a[i];
    newpot->next=NULL;
    if(head==NULL){
        head=newpot;
        p=newpot;
    }
    else{
        p->next=newpot;
        p=newpot;
    }
}
struct innode* q=head;
while(q!=NULL){
    printf("%d\n",q->data);
    q=q->next;
}
printf("finish null\n");
//删除头节点：
struct innode* del=head;
head=head->next;
free(del);
//删除尾节点
struct innode* r=head;
while(r->next->next=NULL){
    struct innode*temp=r->next;
    r->next=NULL;
    free(temp);
}



return 0;
}