#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main() {
    srand(time(NULL));
    int ra=rand()%101;
    int guess,times=0;
    while(1){
        
        printf("��������µ����֣�0-100��������-1�˳���");
        if (scanf("%d", &guess) != 1) return 0;
        times++;
        if (guess == -1) break;
        if(times>7){
            printf("���ź�������7�λ��ᣬ��Ϸ��������ȷ������%d��\n", ra);
            break;
        }
        if (guess < ra) {
            printf("̫С�ˣ�\n");
        } else if (guess > ra) {
            printf("̫���ˣ�\n");
        } else {
            printf("��ϲ�㣬�¶��ˣ������%d�Ρ�\n", times);
            break;
        }

    }
    return 0;
}