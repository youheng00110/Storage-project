#include <stdio.h>
#include <math.h>
int *bubble_sort(int arr[],int n){
    //冒泡
    int i,j,temp;
    // 外面的循环控制我们需要冒多少次泡泡，每冒一次，最大的那个数就归位了
    for(i=0;i<=n-1;i++){
        // 里面的循环负责把最大的泡泡往后推
        for(j=0;j<=n-1-i;j++){
            // 如果前面的数比后面的数大，它们就交换位置，就像大个子要站到后面去一样
            if(arr[j]>arr[j+1]){
                temp=arr[j];      // 先把前面的数暂时存起来
                arr[j]=arr[j+1];  // 把后面的数放到前面
                arr[j+1]=temp;    // 把刚才存起来的数放到后面
            }
        }
    }
    return arr; // 排好序啦，把结果送回去
}
// 这是一个选择排序函数，就像在挑苹果，每次都从剩下的苹果里挑一个最小的放好
// left min to max (从左到右，从小到大)
int* choose_sort(int arr[],int n){
    int i,j,min,temp;
    // i 代表我们当前要确定的那个位置，比如第1个、第2个...
    for (i=0;i<n-1;i++){
        min=i; // 先假设当前这个位置的数就是最小的
        // 然后往后看，看看有没有比它更小的
        for(j=i+1;j<n;j++){
            // 如果发现后面有个数比我们记录的“最小数”还小
            if(arr[j]<arr[min]){
            min=j;   // 那就记住这个更小的数的位置
            }   
        }
        // 找到这一轮最小的数后，把它和当前位置的数交换
        temp=arr[i];
        arr[i]=arr[min];
        arr[min]=temp;
    }
return arr; // 挑完啦，把排好序的数组送回去
}
// 有辅助表元的链表的插入排序
// 这是一个链表节点，就像一节火车车厢
typedef struct Node{
    int data;           // 车厢里装的货物（数字）
    struct Node* next;  // 连接下一节车厢的钩子
};

// 这是一个链表插入排序函数，就像整理手里的扑克牌，一张张插到正确的位置
struct Node* insert_sort(struct Node* head){
    struct Node* sorted = NULL; // 这是一个新的链表，用来放已经排好序的“车厢”
    struct Node* current = head; // 当前正在处理的“车厢”
    
    // 只要还有没处理的“车厢”，就继续循环
    while(current != NULL){
        struct Node* next = current->next; // 先记住下一节车厢在哪里，不然等会儿断开连接就找不到了
        
        // 如果排好序的链表是空的，或者当前车厢的数字比排好序的第一节还小
        // 那就把当前车厢放到最前面
        if(sorted == NULL || sorted->data >= current->data){
            current->next = sorted;
            sorted = current;
        } else {
            // 否则，我们需要在排好序的链表里找到合适的位置插进去
            struct Node* temp = sorted;
            // 往后找，直到找到一个比当前车厢数字大的位置，或者找完整个链表
            while(temp->next != NULL && temp->next->data < current->data){
                temp = temp->next;
            }
            // 找到位置了，把当前车厢插进去
            current->next = temp->next;
            temp->next = current;
        }
        // 处理下一节车厢
        current = next;
    }
    return sorted; // 返回排好序的链表头
}
// strlenth: 计算字符串长度
// 这个函数用来数一数一串字里面有多少个字符，就像数糖果一样
int strleng(char str[]){
    int len; // 用来记录数到了多少个
    // 只要还没遇到字符串的结束标志 '\0'（就像句号），就继续数
    while(str[len]!='\0'){
        len++; // 数到一个，计数器加一
    }
    return len; // 告诉大家一共数了多少个
}

// strcpy: 字符串复制
// 这个函数用来把一个字符串的内容抄到另一个地方去
char* strcpy(char* new, char* ret){
    char* temp = new; // 记住新字符串的开始位置，不然抄完就找不到了
    // 只要原来的字符串还没结束，就一个字一个字地抄
    while(*ret != '\0'){
        *new = *ret; // 把 ret 指向的字抄给 new
        new++;       // new 往后移一格，准备接下一个字
        ret++;       // ret 往后移一格，准备读下一个字
    }
    *new = '\0'; // 抄完了，别忘了在新字符串后面加个结束标志
    return temp; // 返回新字符串的开始位置
}

// str compare: 字符串比较
// 这个函数用来比较两个字符串是不是一样的，或者哪个更大
int strcmp(char* a,char* b){
    // 只要两个字符串都没结束，就一个字一个字地比
    while(*a != '\0' && *b != '\0'){
        // 如果发现不一样的地方
        if(*a != *b){
            return (*a - *b); // 告诉大家它们的差距是多少
        }
        a++; // 往后移，比下一个字
        b++; // 往后移，比下一个字
    }
    // 如果比完了，或者其中一个结束了，返回最后的差距（如果是0说明完全一样）
    return (*a - *b);
}

// strcat: 字符串连接
// 这个函数用来把两个字符串拼在一起，就像把两节火车连起来
char* strcat(char*a,char*b){
    char* temp = a; // 记住第一个字符串的开始位置
    // 先找到第一个字符串的末尾
    while(*a != '\0'){
        a++;
    }
    // 然后把第二个字符串一个字一个字地接到第一个字符串后面
    while(*b != '\0'){
        *a = *b;
        a++;
        b++;
    }
    *a = '\0'; // 拼完了，加个结束标志
    return temp; // 返回拼好后的字符串
}
// factorial: 计算阶乘
// 这个函数用来算一个数的阶乘，比如 5 的阶乘就是 5*4*3*2*1
long factorial(int n){
    // 如果是 0，阶乘就是 1（这是数学规定哦）
    if(n==0){
        return 1;
    }
    else{
        // 否则，就是这个数乘以（它减一的阶乘），自己调用自己，这叫递归
        return n*factorial(n-1);
    }
}

// printinorder: 顺序打印
// 这个函数用来把一个长长的数字，一位一位地打印出来
void printinorder(long n){
    // 如果数字小于 10，说明只剩一位了，直接打印出来
    if(n<10){
        printf("%ld ",n);
    }
    else{
        // 如果还有多位，先处理前面的数字（除以 10 去掉最后一位）
        printinorder(n/10);
        // 处理完前面的，再打印最后这一位（取余数得到最后一位）
        printf("%ld ", n % 10);
    }
}
// hundred_day: 计算百日宴日期
// 这个函数用来算宝宝出生100天后是哪一天
int hundred_day(int*year,int*month,int*day){
    // 这里记下了每个月有多少天，比如一月有31天，二月有28天...
    int days_in_months[12]={31,28,31,30,31,30,31,31,30,31,30,31};
    // 先把现在的日子加上99天（因为出生那天也算1天，所以加99）
    int total_days= *day + 99; 
    int i;
    
    // 检查是不是闰年（闰年的二月有29天）
    // 规则是：能被4整除但不能被100整除，或者能被400整除的年份
    if(((*year % 4 == 0) && (*year % 100 != 0)) || (*year % 400 == 0)){
        days_in_months[1] = 29; // 如果是闰年，二月改成29天
    }
    
    // 如果总天数超过了当前这个月的天数，就要往后翻一个月
    while(total_days > days_in_months[*month - 1]){
        // 减去当前这个月的天数
        total_days -= days_in_months[*month - 1];
        (*month)++; // 月份加一
        
        // 如果月份超过12了，说明过年了
        if(*month > 12){
            *month = 1; // 月份变回1月
            (*year)++;  // 年份加一
            
            // 新的一年，又要检查是不是闰年
            if(((*year % 4 == 0) && (*year % 100 != 0)) || (*year % 400 == 0)){
                days_in_months[1] = 29;
            } else {
                days_in_months[1] = 28; // 不是闰年就变回28天
            }
        }
    }
    // 剩下的天数就是那个月的几号
    *day = total_days;
    return 0;
}
//杨辉三角的函数<10
void pascaltriangle(int n){
    int a[10][10];
    int i, j;
    for(i=0; i<n; i++){
        for(j=0; j<=i; j++){
            if(j==0 || j==i){
                a[i][j]=1;
            }
            else{
                a[i][j]=a[i-1][j-1]+a[i-1][j];
            }
            printf("%d ",a[i][j]);
        }
        printf("\n");
    }
}
// 主函数：程序的入口，就像大门一样
int fiobonacci(int n){
    int a1,a2;
    if(n<=2){
        return 1;
    }
    if(n>2){
        return fiobonacci(n-1)+fiobonacci(n-2);
        printf("\n");
    }
}

int main() 
{ 
    int year, month, day; // 用来存年、月、日
    
    // 提示用户输入宝宝的生日
    printf("Enter the baby's birthday: "); 
    // 读取用户输入的年、月、日
    scanf("%d.%d.%d", &year, &month, &day); 
    
    // 调用刚才写的函数算出100天后的日期
    hundred_day(&year, &month, &day); 
    
    // 把算出来的日期打印给大家看
    printf("The baby's 100-day date is: %d.%d.%d\n", year, month, day); 
    
    return 0; // 程序顺利结束
}
/*
// 这是另一个主函数，用来测试阶乘功能的
int main(){
    int a,b,c;
    // 问你要一个数字
    printf("enter a number to find factorial:");
    scanf("%d",&a);
    // 算出阶乘并打印出来
    printf("factorial=%ld\n",factorial(a));
    // 把结果一位一位打印出来
    printinorder(factorial(a));
    return 0;
}*/