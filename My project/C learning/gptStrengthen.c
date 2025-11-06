<<<<<<< HEAD
#include <stdio.h>
/*int main(){
    int i;
    while(1){
    printf("input a number(-1break):\n");
    scanf("%d",&i);
    if(i<0){
        break;
    }
    if(i%2==0){
        if(i%3==0){
            if(i%5==0){
                printf("Divisible by 2, 3, and 5\n");
            }
            else{
                printf("Divisible by 2 and 3\n");
            }
        }
        else if(i%5==0){
            printf("Divisible by 2 and 5\n");
        }
        else{
            printf("Divisible by 2\n");
        }
    }
    else if(i%3==0){
        if(i%5==0){
            printf("Divisible by 3 and 5\n");
        }
        else{
            printf("Divisible by 3\n");
        }
    }
    else if(i%5==0){
        printf("Divisible by 5\n");
    }
    else{
        printf("Not divisible by 2, 3, or 5\n");
    }
   
}
return 0;
}
*/
/*
int main(){
    int i,j,a,sum=0,mult=1,aver=0,temp=0;
    printf("Input a number:\n");
    scanf("%d",&a);
    for(i=1;i<=a;i+=2){
        sum+=i;
    }
    for(j=3;j<=a;j+=3){
        mult*=j;
    }
    for(i=0;i<=a;i+=2){
        aver+=i;
        temp++;
    }
    printf("\nSum=%d\n",sum);
    printf("Product=%d\n",mult);
    printf("Average=%d\n",aver/temp);
    return 0;
}
*/
int main(){
    int a[100];
    int n = 0;           // 实际输入的个数
    int i, j;
    long long sum = 0;   // 防止累加溢出
    int num = 0;         // 大于平均值的数量

    // 输入阶段：读到 0 结束，不把 0 放进数组
    while (n < 100) {
        int x;
        printf("Input number (0 to stop):\n");
        if (scanf("%d", &x) != 1) {
            printf("Invalid input. Stop.\n");
            return 0;
        }
        if (x == 0) break;
        a[n++] = x;
    }

    if (n == 0) {
        printf("No data.\n");
        return 0;
    }

    // 计算平均值（double）
    for (i = 0; i < n; i++) sum += a[i];
    double aver = (double)sum / n;

    // 统计并打印超过平均值的元素
    for (i = 0; i < n; i++) {
        if (a[i] > aver) {
            num++;
            printf("over average:%d\n", a[i]);
        }
    }

    // 计算最小值与最大值
    int min = a[0], max = a[0];
    for (i = 1; i < n; i++) {
        if (a[i] < min) min = a[i];
        if (a[i] > max) max = a[i];
    }

    printf("average=%.2f\n", aver);
    printf("number over average=%d\n", num);
    printf("min=%d\n", min);
    printf("max=%d\n", max);

    // 冒泡排序（仅对前 n 个有效元素）
    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - 1 - i; j++) {
            if (a[j] > a[j + 1]) {
                int t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
            }
        }
    }

    // 打印排序后数组
    printf("sorted array:\n");
    for (i = 0; i < n; i++) {
        printf("%d%s", a[i], (i + 1 < n) ? "," : "\n");
    }

    return 0;
}

=======
<<<<<<< HEAD
#include <stdio.h>
/*int main(){
    int i;
    while(1){
    printf("input a number(-1break):\n");
    scanf("%d",&i);
    if(i<0){
        break;
    }
    if(i%2==0){
        if(i%3==0){
            if(i%5==0){
                printf("Divisible by 2, 3, and 5\n");
            }
            else{
                printf("Divisible by 2 and 3\n");
            }
        }
        else if(i%5==0){
            printf("Divisible by 2 and 5\n");
        }
        else{
            printf("Divisible by 2\n");
        }
    }
    else if(i%3==0){
        if(i%5==0){
            printf("Divisible by 3 and 5\n");
        }
        else{
            printf("Divisible by 3\n");
        }
    }
    else if(i%5==0){
        printf("Divisible by 5\n");
    }
    else{
        printf("Not divisible by 2, 3, or 5\n");
    }
   
}
return 0;
}
*/
/*
int main(){
    int i,j,a,sum=0,mult=1,aver=0,temp=0;
    printf("Input a number:\n");
    scanf("%d",&a);
    for(i=1;i<=a;i+=2){
        sum+=i;
    }
    for(j=3;j<=a;j+=3){
        mult*=j;
    }
    for(i=0;i<=a;i+=2){
        aver+=i;
        temp++;
    }
    printf("\nSum=%d\n",sum);
    printf("Product=%d\n",mult);
    printf("Average=%d\n",aver/temp);
    return 0;
}
*/

=======
#include <stdio.h>
/*int main(){
    int i;
    while(1){
    printf("input a number(-1break):\n");
    scanf("%d",&i);
    if(i<0){
        break;
    }
    if(i%2==0){
        if(i%3==0){
            if(i%5==0){
                printf("Divisible by 2, 3, and 5\n");
            }
            else{
                printf("Divisible by 2 and 3\n");
            }
        }
        else if(i%5==0){
            printf("Divisible by 2 and 5\n");
        }
        else{
            printf("Divisible by 2\n");
        }
    }
    else if(i%3==0){
        if(i%5==0){
            printf("Divisible by 3 and 5\n");
        }
        else{
            printf("Divisible by 3\n");
        }
    }
    else if(i%5==0){
        printf("Divisible by 5\n");
    }
    else{
        printf("Not divisible by 2, 3, or 5\n");
    }
   
}
return 0;
}
*/
/*
int main(){
    int i,j,a,sum=0,mult=1,aver=0,temp=0;
    printf("Input a number:\n");
    scanf("%d",&a);
    for(i=1;i<=a;i+=2){
        sum+=i;
    }
    for(j=3;j<=a;j+=3){
        mult*=j;
    }
    for(i=0;i<=a;i+=2){
        aver+=i;
        temp++;
    }
    printf("\nSum=%d\n",sum);
    printf("Product=%d\n",mult);
    printf("Average=%d\n",aver/temp);
    return 0;
}
*/

>>>>>>> 4a87f54d87283ef5f945e9c293497f4661295b68
>>>>>>> 02297afcddcad879a453ccb4c6175697dc0edd72
