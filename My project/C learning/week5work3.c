<<<<<<< HEAD
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main() {
    srand(time(NULL));
    int ra=rand()%101;
    int guess,times=0;
    while(1){
        
        printf("请输入你猜的数字（0-100），输入-1退出：");
        if (scanf("%d", &guess) != 1) return 0;
        times++;
        if (guess == -1) break;
        if(times>7){
            printf("很遗憾，超过7次机会，游戏结束！正确数字是%d。\n", ra);
            break;
        }
        if (guess < ra) {
            printf("太小了！\n");
        } else if (guess > ra) {
            printf("太大了！\n");
        } else {
            printf("恭喜你，猜对了！你猜了%d次。\n", times);
            break;
        }

    }
    return 0;
=======
<<<<<<< HEAD
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main() {
    srand(time(NULL));
    int ra=rand()%101;
    int guess,times=0;
    while(1){
        
        printf("请输入你猜的数字（0-100），输入-1退出：");
        if (scanf("%d", &guess) != 1) return 0;
        times++;
        if (guess == -1) break;
        if(times>7){
            printf("很遗憾，超过7次机会，游戏结束！正确数字是%d。\n", ra);
            break;
        }
        if (guess < ra) {
            printf("太小了！\n");
        } else if (guess > ra) {
            printf("太大了！\n");
        } else {
            printf("恭喜你，猜对了！你猜了%d次。\n", times);
            break;
        }

    }
    return 0;
=======
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main() {
    srand(time(NULL));
    int ra=rand()%101;
    int guess,times=0;
    while(1){
        
        printf("请输入你猜的数字（0-100），输入-1退出：");
        if (scanf("%d", &guess) != 1) return 0;
        times++;
        if (guess == -1) break;
        if(times>7){
            printf("很遗憾，超过7次机会，游戏结束！正确数字是%d。\n", ra);
            break;
        }
        if (guess < ra) {
            printf("太小了！\n");
        } else if (guess > ra) {
            printf("太大了！\n");
        } else {
            printf("恭喜你，猜对了！你猜了%d次。\n", times);
            break;
        }

    }
    return 0;
>>>>>>> 02297afcddcad879a453ccb4c6175697dc0edd72
>>>>>>> b6f6c6d4bd78d0c45678438642b709b0eba48ced
}