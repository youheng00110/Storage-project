#include <stdio.h>

/* 函数尝试修改参数的值 */
void modify_parameters(int a, int b, int c) {
    printf("函数内部修改前：a=%d, b=%d, c=%d\n", a, b, c);
    
    /* 在函数内部修改参数的值 */
    a = a * 10;
    b = b + 100;
    c = c - 50;
    
    printf("函数内部修改后：a=%d, b=%d, c=%d\n", a, b, c);
}

/* 另一个例子：数组参数的情况 */
void modify_array(int arr[], int size) {
    int i;  /* C89: 变量要在块开头声明 */

    printf("函数内部数组修改前：");
    for (i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    /* 修改数组元素 */
    for (i = 0; i < size; i++) {
        arr[i] = arr[i] * 2;
    }
    
    printf("函数内部数组修改后：");
    for (i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

/* 对比：使用指针真正修改原值 */
void modify_with_pointers(int *a, int *b) {
    printf("指针函数内部修改前：*a=%d, *b=%d\n", *a, *b);
    
    *a = *a * 10;
    *b = *b + 100;
    
    printf("指针函数内部修改后：*a=%d, *b=%d\n", *a, *b);
}

int main(void) {
    int x = 5, y = 10, z = 20;
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    int i;          /* C89: 循环变量提前声明 */
    int m = 5, n = 10;

    printf("=== 验证基本类型参数的单向传递 ===\n");
    
    printf("主函数调用前：x=%d, y=%d, z=%d\n", x, y, z);
    modify_parameters(x, y, z);
    printf("主函数调用后：x=%d, y=%d, z=%d\n", x, y, z);
    printf("→ 说明：基本类型参数是值传递，函数内的修改不影响原变量\n\n");
    
    printf("=== 验证数组参数的'伪双向'传递 ===\n");
    
    printf("主函数数组调用前：");
    for (i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    
    modify_array(numbers, size);
    
    printf("主函数数组调用后：");
    for (i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    printf("→ 说明：数组名作为指针传递，函数内可以修改原数组内容\n\n");
    
    printf("=== 验证指针参数的真正双向传递 ===\n");
    
    printf("主函数指针调用前：m=%d, n=%d\n", m, n);
    modify_with_pointers(&m, &n);
    printf("主函数指针调用后：m=%d, n=%d\n", m, n);
    printf("→ 说明：通过指针传递地址，可以实现真正的双向传递\n");
    
    return 0;
}