<<<<<<< HEAD
#include <stdio.h>
int main(){
    while(1){
        int choice;
        printf("=== 迷你计算器 ===\n1. 加法运算\n2. 减法运算\n3. 乘法运算\n4. 除法运算\n5. 退出程序\n请选择(1-5):");
        if(scanf("%d",&choice)!=1) return 0;
        if(choice==5) break;

        while (1){
            switch(choice){
                case 1:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a+b);
                    break;
                }
                case 2:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a-b);
                    break;
                }
                case 3:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a*b);
                    break;
                }
                case 4:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    if(b==0){
                        printf("错误：除数不能为零！\n");
                    }else{
                        printf("结果：%.2f\n",a/b);
                    }
                    break;
                }
                default:
                    printf("无效选择，请重新输入。\n");
            }

            
            printf("继续当前运算？(0继续，-1 返回主菜单): ");
            int cont;
            if (scanf(" %d", &cont) != 1) return 0;  
            if (cont == -1) break;       
        }
    }
=======
<<<<<<< HEAD
#include <stdio.h>
int main(){
    while(1){
        int choice;
        printf("=== 迷你计算器 ===\n1. 加法运算\n2. 减法运算\n3. 乘法运算\n4. 除法运算\n5. 退出程序\n请选择(1-5):");
        if(scanf("%d",&choice)!=1) return 0;
        if(choice==5) break;

        while (1){
            switch(choice){
                case 1:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a+b);
                    break;
                }
                case 2:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a-b);
                    break;
                }
                case 3:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a*b);
                    break;
                }
                case 4:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    if(b==0){
                        printf("错误：除数不能为零！\n");
                    }else{
                        printf("结果：%.2f\n",a/b);
                    }
                    break;
                }
                default:
                    printf("无效选择，请重新输入。\n");
            }

            
            printf("继续当前运算？(0继续，-1 返回主菜单): ");
            int cont;
            if (scanf(" %d", &cont) != 1) return 0;  
            if (cont == -1) break;       
        }
    }
=======
#include <stdio.h>
int main(){
    while(1){
        int choice;
        printf("=== 迷你计算器 ===\n1. 加法运算\n2. 减法运算\n3. 乘法运算\n4. 除法运算\n5. 退出程序\n请选择(1-5):");
        if(scanf("%d",&choice)!=1) return 0;
        if(choice==5) break;

        while (1){
            switch(choice){
                case 1:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a+b);
                    break;
                }
                case 2:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a-b);
                    break;
                }
                case 3:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    printf("结果：%.2f\n",a*b);
                    break;
                }
                case 4:{
                    double a,b;
                    printf("请输入两个数字，用空格分隔：");
                    if(scanf("%lf %lf",&a,&b)!=2) return 0;
                    if(b==0){
                        printf("错误：除数不能为零！\n");
                    }else{
                        printf("结果：%.2f\n",a/b);
                    }
                    break;
                }
                default:
                    printf("无效选择，请重新输入。\n");
            }

            
            printf("继续当前运算？(0继续，-1 返回主菜单): ");
            int cont;
            if (scanf(" %d", &cont) != 1) return 0;  
            if (cont == -1) break;       
        }
    }
>>>>>>> 02297afcddcad879a453ccb4c6175697dc0edd72
>>>>>>> b6f6c6d4bd78d0c45678438642b709b0eba48ced
}