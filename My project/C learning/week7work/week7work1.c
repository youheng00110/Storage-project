#include <stdio.h>
#include <string.h>
/*字符串反转 reverse_string(char s[], int len)    s用来传递字符数组，len标识所传递数组的长度

递归思路：

基线条件： 如果字符串为空或只有一个字符，返回自身

递归关系： 把字符串看作 第一个字符 + 剩余字符串，反转结果就是 反转(剩余字符串) + 第一个字符*/
void reverse_string(char s[],int len){
    char temp;
    if(len<=1){
        return;
    }
    else{
        temp=s[len-1];
        s[len-1]=s[0];
        s[0]=temp;
        reverse_string(s+1,len-2);

    }
}
int main(){
    char str[]="abcdef";
    int len=strlen(str); 
    reverse_string(str,len);
    printf("反转后的字符串为：%s\n",str);
    return 0;
}