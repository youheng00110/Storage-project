#include <stdio.h>
int main(void){
    int ar[100];
    int i,max=0,a=0,b=0,c=0,d=0,e=0,test=0;
    long total=0;
    int n = 0;                    

    //����
    while (n < 100) {             
        printf("����ѧ���ɼ�������-1������");
        if (scanf("%d", &ar[n]) != 1) return 0;
        if (ar[n] == -1) break;
        total = total + ar[n];
        n++;
    }

    //ͳ��
    for (i = 0; i < n; i++) {     
        if (ar[i] > max) max = ar[i];
        if (ar[i] >= 90) a++;
        else if (ar[i] >= 80) b++;
        else if (ar[i] >= 70) c++;
        else if (ar[i] >= 60) d++;
        else e++;
    }

    //���

    printf("ƽ����Ϊ��%.2f\n", (double)total / n);
    printf("��߷�Ϊ��%d\n", max);
    printf("90������������%d\n", a);
    printf("80-89��������%d\n", b);
    printf("70-79��������%d\n", c);
    printf("60-69��������%d\n", d);
    printf("60������������%d\n", e);
    return 0;
}