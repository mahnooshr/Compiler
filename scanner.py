Type_of_tokens = {
 "NUM" : "0123456789",
 "ID" : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
 "letters" : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
"KEYWORD": ["if", "else", "void", "int", "for", "break", "return", "endif"],
"SYMBOL" : [";", ":" ,"," ,"[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", "=="],
"COMMENT " :"///*",
"WHITESPACE"  : "\n\r\t\v\f"
}

def is_num(str):
    if str in Type_of_tokens["NUM"]:
        return True
    else:
        return False

def is_id(str):
    if str in Type_of_tokens["ID"]:
        if str[0] in Type_of_tokens["letters"]:
            return True
    else:
        return False

def is_keyword(str):
    if str in Type_of_tokens["KEYWORD"]:
        return True
    else:
        return False

def is_symbol(str):
    if str in Type_of_tokens["SYMBOL"]:
        return True
    else:
        return False




l_num=1

tokens=[]

class Token:   
    
        
    def __init__(self , value , type):
        self.value=value
        self.type=type
        tokens.append(self)
        
    def get_token(self):
        recognize_token = str((self.type , self.value)) 
        return recognize_token


def search_in_line (line):
    current_loc=0
    words=line.split(" ")
    for word in words:
        if is_keyword(word):
            word=Token(word,"KEYWORD")
        elif is_symbol(word):
            word=Token(word,"SYMBOL")
        elif is_num(word):
            word=Token(word,"NUM")
        elif is_id(word):
            word=Token(word,"ID")   
        else:
                 
            
    

     
file1 = open("input.txt", "r") 
file2=open("tokens.txt", "w")
line_list = file1.readlines();
for line in line_list:
    str = line
    ;
    ;
    ;
    l_num = l_num + 1;

file1.close() 



file2.write(l_num +   )


file2.close()
    
     
     
     
     
     
     
     
     
     
    
    
    
        
        