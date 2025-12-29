<<<<<<< HEAD
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* creatlist(int n) {
    struct Node* head = NULL;
    struct Node* tail = NULL;
    struct Node* newchain=NULL;
    int i;
    for (i = 0; i < n; i++) {
        newchain=(struct Node*)malloc(sizeof(struct Node));
        newchain->data=i+1;
        newchain->next=NULL;
        if(head==NULL){
            head=newchain;
            tail=newchain;
        }
        else{
            tail->next=newchain;
            tail=newchain;
        }
    }
    return head;
}

void printlist(struct Node*head){
    struct Node* p=head;
    while(p!=NULL){
        printf("%d\n",p->data);
        p=p->next;
    }
}

struct Node* reverselist(struct Node* head) {
    struct Node* prev = NULL;
    struct Node* current = head;
    struct Node* next = NULL;
    while (current != NULL) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    return prev;    
}

void freelist(struct Node* head) {
    struct Node* temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
}
struct Node* sortlist(struct Node*head) {
    //
    struct Node* p =head;
    struct Node*sorted=NULL;
    struct Node*next=NULL;
    while(p!=NULL){
        next=p->next;
        if(sorted==NULL||p->data<sorted->data){
            p->next=sorted;
            sorted=p;
        }
        else{
            struct Node* q=sorted;
            while(q->next!=NULL&&q->next->data<p->data){
                q=q->next;
            }
            p->next=q->next;
            q->next=p;
        }
        p=next;
    }   
    return sorted;
}

int main() {
    struct Node* head = NULL;
    int n;

    printf("input the number of nodes:\n");
    scanf("%d", &n);

    head = creatlist(n);

    printf("Original list:\n");
    printlist(head);

    head = reverselist(head);

    printf("Reversed list:\n");
    printlist(head);
    head = sortlist(head);
    printf("Sorted list:\n");
    printlist(head);

    freelist(head);

    return 0;
}
=======
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* creatlist(int n) {
    struct Node* head = NULL;
    struct Node* tail = NULL;
    struct Node* newchain=NULL;
    int i;
    for (i = 0; i < n; i++) {
        newchain=(struct Node*)malloc(sizeof(struct Node));
        newchain->data=i+1;
        newchain->next=NULL;
        if(head==NULL){
            head=newchain;
            tail=newchain;
        }
        else{
            tail->next=newchain;
            tail=newchain;
        }
    }
    return head;
}

void printlist(struct Node*head){
    struct Node* p=head;
    while(p!=NULL){
        printf("%d\n",p->data);
        p=p->next;
    }
}

struct Node* reverselist(struct Node* head) {
    struct Node* prev = NULL;
    struct Node* current = head;
    struct Node* next = NULL;
    while (current != NULL) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    return prev;    
}

void freelist(struct Node* head) {
    struct Node* temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
}
struct Node* sortlist(struct Node*head) {
    //一个比较表元并重新排序的函数
    struct Node* p =head;
    struct Node*sorted=NULL;
    struct Node*next=NULL;
    while(p!=NULL){
        next=p->next;
        if(sorted==NULL||p->data<sorted->data){
            p->next=sorted;
            sorted=p;
        }
        else{
            struct Node* q=sorted;
            while(q->next!=NULL&&q->next->data<p->data){
                q=q->next;
            }
            p->next=q->next;
            q->next=p;
        }
        p=next;
    }   
    return sorted;
}

int main() {
    struct Node* head = NULL;
    int n;

    printf("请输入节点个数：");
    scanf("%d", &n);

    head = creatlist(n);

    printf("原链表：\n");
    printlist(head);

    head = reverselist(head);

    printf("转置后的链表：\n");
    printlist(head);
    head = sortlist(head);
    printf("排序后的链表：\n");
    printlist(head);

    freelist(head);

    return 0;
}
>>>>>>> 2a2a897780e0998a25d94e5a9900ae74fb3cc3cd
