#include <stdio.h>
#include <string.h>

#define WORDS 5     // 要读的单词个数
#define LEN   20    // 每个单词缓冲区长度（含结尾的 '\0'）

int main(void) {
    char dict[WORDS][LEN]; // 5 行、每行 20 个字符的“字符串数组”
    char tmp[LEN];         // 交换用的临时缓冲
    int i, j;

    // 输入：%19s 限制最多读 19 个可见字符，留 1 个位置给 '\0'，防止溢出
    for (i = 0; i < WORDS; ++i) {
        scanf("%19s", dict[i]);   // 读取一个以空白分隔的“单词”
    }

    // 冒泡排序：按字典序从小到大
    for (i = 1; i < WORDS; ++i) {
        for (j = 0; j < WORDS - i; ++j) {
            if (strcmp(dict[j], dict[j + 1]) > 0) {
                // 不能直接给数组赋值，使用 strcpy 通过临时缓冲交换
                strcpy(tmp,        dict[j]);
                strcpy(dict[j],    dict[j + 1]);
                strcpy(dict[j + 1], tmp);
            }
        }
    }

    // 输出：带空格更易读；若需与原题一致“无空格拼接”，把" %s"改成"%s"
    for (i = 0; i < WORDS; ++i) {
        printf("%s%s", dict[i], (i + 1 < WORDS) ? " " : "\n");
    }
    return 0;
}
