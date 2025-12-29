#include <stdio.h>
int ignorecommasoon(char* str){
    int n=0;
    while(*str!='\0'){
        if(!( (*str >= 'A' && *str <= 'Z') ||(*str >= 'a' && *str <= 'z') ))
        {
            *str=' ';
        }
        n++;
        str++;
    }
    return n;
}
int ignorethecap(char* str){
    while (*str != '\0') {
        if (*str >= 'A' && *str <= 'Z') {
            *str = *str + ('a' - 'A');
        }
        str++;
    }
    return 0;
}


int is_palindrome(char* str){
    char* start = str;
    char* end = str;

    while (*end != '\0') end++;
    end--;

    while (start < end) {

        while (start < end && *start == ' ')
            start++;

        while (start < end && *end == ' ')
            end--;

        if (*start != *end)
            return 0;

        start++;
        end--;
    }
    return 1;
}


int main(){
    char s[] = "tat+ata,.Tat";

    ignorecommasoon(s);
    ignorethecap(s);

    if (is_palindrome(s)) {
        printf("Is a palindrome\n");
    } else {
        printf("Not a palindrome\n");
    }

    return 0;
}

