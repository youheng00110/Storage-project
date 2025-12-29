<<<<<<< HEAD
#include <stdio.h>
int main(void){
    int ar[100];
    int i,max=0,a=0,b=0,c=0,d=0,e=0,test=0;
    long total=0;
    int n = 0;                    

    //输入
    while (n < 100) {             
        printf("输入学生成绩，输入-1结束：");
        if (scanf("%d", &ar[n]) != 1) return 0;
        if (ar[n] == -1) break;
        total = total + ar[n];
        n++;
    }

    //统计
    for (i = 0; i < n; i++) {     
        if (ar[i] > max) max = ar[i];
        if (ar[i] >= 90) a++;
        else if (ar[i] >= 80) b++;
        else if (ar[i] >= 70) c++;
        else if (ar[i] >= 60) d++;
        else e++;
    }

    //输出

    printf("平均分为：%.2f\n", (double)total / n);
    printf("最高分为：%d\n", max);
    printf("90分以上人数：%d\n", a);
    printf("80-89分人数：%d\n", b);
    printf("70-79分人数：%d\n", c);
    printf("60-69分人数：%d\n", d);
    printf("60分以下人数：%d\n", e);
    return 0;
=======
<<<<<<< HEAD
#include <stdio.h>
int main(void){
    int ar[100];
    int i,max=0,a=0,b=0,c=0,d=0,e=0,test=0;
    long total=0;
    int n = 0;                    

    //输入
    while (n < 100) {             
        printf("输入学生成绩，输入-1结束：");
        if (scanf("%d", &ar[n]) != 1) return 0;
        if (ar[n] == -1) break;
        total = total + ar[n];
        n++;
    }

    //统计
    for (i = 0; i < n; i++) {     
        if (ar[i] > max) max = ar[i];
        if (ar[i] >= 90) a++;
        else if (ar[i] >= 80) b++;
        else if (ar[i] >= 70) c++;
        else if (ar[i] >= 60) d++;
        else e++;
    }

    //输出

    printf("平均分为：%.2f\n", (double)total / n);
    printf("最高分为：%d\n", max);
    printf("90分以上人数：%d\n", a);
    printf("80-89分人数：%d\n", b);
    printf("70-79分人数：%d\n", c);
    printf("60-69分人数：%d\n", d);
    printf("60分以下人数：%d\n", e);
    return 0;
=======
#include <stdio.h>
int main(void){
    int ar[100];
    int i,max=0,a=0,b=0,c=0,d=0,e=0,test=0;
    long total=0;
    int n = 0;                    

    //输入
    while (n < 100) {             
        printf("输入学生成绩，输入-1结束：");
        if (scanf("%d", &ar[n]) != 1) return 0;
        if (ar[n] == -1) break;
        total = total + ar[n];
        n++;
    }

    //统计
    for (i = 0; i < n; i++) {     
        if (ar[i] > max) max = ar[i];
        if (ar[i] >= 90) a++;
        else if (ar[i] >= 80) b++;
        else if (ar[i] >= 70) c++;
        else if (ar[i] >= 60) d++;
        else e++;
    }

    //输出

    printf("平均分为：%.2f\n", (double)total / n);
    printf("最高分为：%d\n", max);
    printf("90分以上人数：%d\n", a);
    printf("80-89分人数：%d\n", b);
    printf("70-79分人数：%d\n", c);
    printf("60-69分人数：%d\n", d);
    printf("60分以下人数：%d\n", e);
    return 0;
>>>>>>> 02297afcddcad879a453ccb4c6175697dc0edd72
>>>>>>> b6f6c6d4bd78d0c45678438642b709b0eba48ced
}