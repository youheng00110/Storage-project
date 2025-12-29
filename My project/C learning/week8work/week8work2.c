# include<stdio.h>
int mystrwrl(char* str){
    int n=0;
    while(*str!='\0'){
        if(*str<'a'){
            *str=*str+32;
        }
        n++;
        str++;
    }
    return n;
}
int main(){
char s[]="HeLlOWoRLDBROHHH";
mystrwrl(s);
printf("%s\n",s);
return 0;
}