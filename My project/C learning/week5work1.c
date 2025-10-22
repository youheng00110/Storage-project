#include <stdio.h>
int main(void){
    while (1) {
       
        int num, i, j, k;
        printf("请输入一个整数,输入-1退出：");
        if (scanf("%d", &num) != 1) return 0;
        if (num == -1) break;

        for (i = 1; i <= num; i++) {
            for (j = 0; j < num - i; j++) {
                printf(" ");
            }
            for (k = 1; k <= i; k++) {
                printf("%d", k);   
            }
            for (k = i - 1; k >= 1; k--) {
                printf("%d", k);
            }
            printf("\n");
        }
    }
    return 0;
}

