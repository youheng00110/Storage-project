language=input("your language is:")
def lang(language):    
    if language=="english":
        print("hello")
    elif language=="chinese":
        print("ni hao")
    elif language=="german":
        print("guten tag")
    elif language=="french":
        print("bonjour")
    elif language=="italian":
        print("ciao")
    else:
         print("try another language")
    return 0
lang(language)