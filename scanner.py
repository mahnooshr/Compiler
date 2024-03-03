Type_of_tokens = {
 "NUM" : "0123456789",
 "ID" : "[a-zA-Z]*",
"KEYWORD": ["if", "else", "void", "int", "for", "break", "return", "endif"],
"SYMBOL" :  "; : , [ ] ( ) { } + - * = < ==",
"COMMENT " :"///*",
"WHITESPACE"  : "\n\r\t\v\f"
}

l_num=1

class Token:       
    def __init__(self , line_number, value , type):
        self.line_number = line_number
        self.value=value
        self.type=type
        
    def get_token(self):
        recognize_token = str((self.type , self.value)) 
        return recognize_token
 
search_in_line 
     
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
    
     
     
     
     
     
     
     
     
     
    
    
    
        
        