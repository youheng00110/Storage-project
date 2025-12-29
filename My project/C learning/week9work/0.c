#include  <stdio.h>
#include  <math.h>
struct point{
   int x;  
   int y;
} p[3];  //结构数组，存储三个坐标点
int menu(){  //菜单函数
  int choice;
  do {  
     printf("\n\n\n");
     printf("  1.指定点，并为它输入坐标值\n");
     printf("  2.指定点，显示它的坐标值\n");
     printf("  3.指定两点,求出它们的中点坐标给另外一个点\n");
     printf("  4.指定两点，显示两点间的矩离\n");
     printf("  5.指定两点，判另一点是否在两点的连线上\n");
     printf("  6.结束程序\n");
     printf("\t输入你的选择!\n");
     scanf("%d", &choice);
     if (choice >= 1 && choice <= 6) return choice;  //返回选择
     printf("选择出错！重新选择。\n");
  } while ( 1 );  
}
int pointNo(){   //接受用户指定的点的代号
    int pno;
    while (1) {
        printf("指定点的代号:\n"); 
        scanf("%d", &pno);
        if(pno >= 1 && pno <= 3)  return pno-1;
        printf("点的代号出错！重新指定。\n");
    }
}
void inputPoint(int pno){  //输入指定点的坐标
      printf("输入第 %d 点的 X 坐标和 Y 坐标\n", pno+1);
      scanf("%d%d", &p[pno].x, &p[pno].y);
}
void displayPoint(int pno){ //显示指定点的坐标
      printf("第 %d 点的 X 坐标 = %d , 它的 Y 坐标 = %d\n", 
	  pno+1, p[pno].x, p[pno].y);
}

void midPoint(){ //求指定两点的连线中点为另一点
  int pno1, pno2, pno3;
  pno1 = pointNo(); 
  pno2 = pointNo();
  pno3 = 3 - pno1 - pno2;  //?tip
  p[pno3]. x = (p[pno1].x + p[pno2].x)/2;
  p[pno3]. y = (p[pno1].y + p[pno2].y)/2;
}
void distance(){  //指定两点，显示两点间的矩离
  int pno1, pno2;
  pno1 = pointNo(); 
  pno2 = pointNo();
  printf("这两点之间的矩离 = %f\n",
      sqrt((double)(p[pno1]. x - p[pno2].x)*(p[pno1]. x - p[pno2].x) +	   (double)(p[pno1]. y - p[pno2].y)*(p[pno1]. y - p[pno2].y)));
}
void isInLine(){ //判另一点是否在指定两点的连线上
   int pno1, pno2, pno3;  double t;
   pno1 = pointNo();  
   pno2 = pointNo();  
   pno3 = 3 - pno1 - pno2;
   t = (double)(p[pno2].y-p[pno1].y)*(double)(p[pno3].x - p[pno1].x)     -  (double)(p[pno3].y - p[pno1].y)* (double)(p[pno2].x - p[pno1].x);
  if (fabs(t) < 1.0e-5)  printf("In same line\n");
  else printf("Not in same line\n");
} //?思考：为什么要用浮点数比较？能否避免？
void main(){
   int choice;
   while (1) {
     choice = menu();
     switch(choice) {
       case 1: inputPoint(pointNo()); break;
       case 2: displayPoint(pointNo()); break;
       case 3: midPoint(); break;
       case 4: distance(); break;
       case 5: isInLine(); break;
       case 6: return;
     }
   }
}
