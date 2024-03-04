Type_of_tokens = {
 "NUM" : "0123456789",
 "ID" : "[a-zA-Z]*",
"KEYWORD": ["if", "else", "void", "int", "for", "break", "return", "endif"],
"SYMBOL" :  "; : , [ ] ( ) { } + - * = < ==",
"COMMENT " :"///*",
"WHITESPACE"  : "\n\r\t\v\f"
}

def is_num(str):

def is_id(str):

def is_keyword(str):

def is_symbol(str):




l_num=1


class Token:   
    tokens=[]
        
    def __init__(self , value , type):
        self.value=value
        self.type=type
        
    def get_token(self):
        recognize_token = str((self.type , self.value)) 
        return recognize_token


def search_in_line (line):
    current_loc=0
    words=line.split(" ")
    for word in words:
        if is_keyword(word):
            word=Token(word,"keyword")
    

     
file1 = open("input.txt", "r") 
line_list = file1.readlines();
for line in line_list:
    str = line
    ;
    ;
    ;
    l_num = l_num + 1;

file1.close() 


file2=open("tokens.txt", "w")
file2.write(l_num +   )


file2.close()
    
     
     
     
     
     
     
     
     
     
    
    
    
        
        