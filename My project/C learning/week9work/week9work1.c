#include<stdio.h>
#include<string.h>
#include<stdlib.h>
    struct date{
        int year;
        int month;
        int day;
    };
    struct stuinfo{
        char name[20];
        int id;
        struct date birthday;
    };
    int i;
void init(struct stuinfo* p){
    for( i=0;i<10;i++){
        strcpy((p+i)->name,"小红");
}
}
void printmenu(){

    printf("---------------------------------------------------------\n");
    printf("欢迎来到学生信息管理系统，请按系统提示操作：\n");
    printf("1. 输入学生信息 (press '1')\n");
    printf("2. 查找学生信息 (press '2')\n");
    printf("3. 退出当前系统 (press '3')\n");
    printf("---------------------------------------------------------\n");
}
void input(struct stuinfo* p){
    for( i=0;i<10;i++){
        printf("请输入第%d个学生的信息\n",i+1);
        printf("姓名:");
        scanf("%s",(p+i)->name);
        printf("学号:");
        scanf("%d",&(p+i)->id);
        printf("出生日期(年 月 日):");
        scanf("%d %d %d",&(p+i)->birthday.year,&(p+i)->birthday.month,&(p+i)->birthday.day);
    }
}
void delve(struct stuinfo*p){
    int searchid,flag=1;
    printf("请输入要查找的学生学号:");
    scanf("%d",&searchid);
    for(i=0;i<10;i++){
        if((p+i)->id==searchid){
            printf("姓名:%s\n", (p+i)->name);
            printf("学号:%d\n", (p+i)->id);
            printf("出生日期:%d-%d-%d\n", (p+i)->birthday.year, (p+i)->birthday.month, (p+i)->birthday.day);
            flag=0;
            break;
        }

        }
    if(flag){
        printf("未找到该学生信息！\n");
    }
}
int main(){
    int k;
    struct stuinfo* pt = (struct stuinfo*)malloc(10 * sizeof(struct stuinfo));
    init(pt);
    
    while(1){
    printmenu();
    scanf("%d",&k);
    if(k==3){
        break;
    }
    switch (k){
    case 1:
        input(pt);
        break;
    case 2:
        delve(pt);
        break;
    default:
        break;
    }
}
    free(pt);
    return 0;
    
}