#include <stdio.h>
int main(){
    while(1){
        int choice;
        printf("=== ��������� ===\n1. �ӷ�����\n2. ��������\n3. �˷�����\n4. ��������\n5. �˳�����\n��ѡ��(1-5):");
        if(scanf("%d",&choice)!=1) return 0;
        if(choice==5) break;

        while (1){
            switch(choice){
                case 1:{
                    double a,b;
                    printf("�������������֣��ÿո�ָ���");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("�����%.2f\n",a+b);
                    break;
                }
                case 2:{
                    double a,b;
                    printf("�������������֣��ÿո�ָ���");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("�����%.2f\n",a-b);
                    break;
                }
                case 3:{
                    double a,b;
                    printf("�������������֣��ÿո�ָ���");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("�����%.2f\n",a*b);
                    break;
                }
                case 4:{
                    double a,b;
                    printf("�������������֣��ÿո�ָ���");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    if(b==0){
                        printf("���󣺳�������Ϊ�㣡\n");
                    }else{
                        printf("�����%.2f\n",a/b);
                    }
                    break;
                }
                default:
                    printf("��Чѡ�����������롣\n");
            }

            
            printf("������ǰ���㣿(0������-1 �������˵�): ");
            int cont;
            if (scanf(" %d", &cont) != 1) return 0;  
            if (cont == -1) break;       
        }
    }
}