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
 
 
     
file1 = open("input.txt", "r") 

str = file1.readline();

file1.close() 


file2=open("tokens.txt", "w")



file2.close()
    
     
     
     
     
     
     
     
     
     
    
    
    
        
        