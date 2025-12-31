#include <stdio.h>
#if 0
int multiply(int a) {
    int result = 1,i;
    for(i=1;i<=a;i++){
        result = result * i;
    }
    return result;
}
int main(void) {
    printf("Enter a number to calculate its factorial: ");
    int a;
    scanf("%d",&a);
    int fact = multiply(a);
    printf("Factorial of %d is %d\n", a, fact);
}
#endif
#if 0
int fibonacci(int n){
    if(n==1) return 1;
    if(n==2) return 2;
    return fiobonacci(n-1)+fiobonacci(n-2);
}
int main(){
    int n;
    scanf("%d",&n);
    printf("%d\n",fiobonacci(n));
    return 0;
}
#endif
//hannoi函数，目的是将n个盘子每次只移动一个盘子且保持大盘在下小盘在上的顺序从A移到C，B作为辅助
int hannoi(int n,char orig,char targ,char temp)
//orig是原柱子A，targ是目标要放过去的柱子C，temp是辅助柱子B.这个是最后要达到的目标，与下一句话不冲突
//操作就是把（除开n，n是盘子个数）第一个参数的柱子上的盘子移到第二个参数的柱子，这个规则始终不变
{
    if(n==1){ 
        printf("%c->%c\n",orig,targ);//只用一步操作将最底下的盘子从orig移动到targ，故直接print
    }
    else{
        hannoi(n-1,orig,temp,targ);//先将上面的n-1个盘子从orig移动到temp，这个是一个笼统操作，因为你一次只能拿一个，用迭代直接给上一步的函数
        printf("%c->%c\n",orig,targ);//将最底下的盘子从orig移动到targ，这一步是单一的可以直接prinnt
        hannoi(n-1,temp,targ,orig);//将temp上的n-1个盘子移动到targ，也是笼统操作迭代直接给上一步的函数，
        //但是是把temp上的n-1作为原柱子，targ作为目标柱子，orig（此时已经空了）作为辅助柱子
    }
}
int main(){
    int n;
    printf("Enter number of disks: ");
    scanf("%d",&n);
    hannoi(n,'A','C','B');//直接调用hannoi函数
    return 0;
}