Type_of_tokens = {
 "NUM" : "0123456789",
 "ID" : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
 "letters" : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
"KEYWORD": ["if", "else", "void", "int", "for", "break", "return", "endif"],
"SYMBOL" : [";", ":" ,"," ,"[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", "=="],
"COMMENT " :"///*",
"WHITESPACE"  : "\n\r\t\v\f"
}

tokens=[]

class Token:   
    
        
    def __init__(self , value , type):
        self.value=value
        self.type=type
        tokens.append(self)
        
    def __str__ (self):
        return f"({self.type}, {self.value})"
    
    
    
    
class Line:
    
    def __init(self,number,pointer_loc,str):    
        self.line_number=number
        self.pointer_loc=pointer_loc
        self.str=str
        
    def __Str__(self):
        return self.pointer_loc
        
def lookahead_NUM (i,str):
    token_str=""
    line=Line(i,line)
    while str[line.pointer_loc] in Type_of_tokens["ID"] :
        token_str+=str[line.pointer_loc]
        line.pointer_loc+=1
    if str[line.pointer_loc] in Type_of_tokens["letter"]:
        return #error
    else:
               
        return Token(token_str,"NUM")


def lookahead_IDKEYWORD (j,str):
    token_str=""
    line=Line(j,line)
    while str[line.pointer_loc] in Type_of_tokens["ID"] :
            token_str+=str[line.pointer_loc]
            line.pointer_loc+=1
    if token_str in Type_of_tokens["KEYWORD"]:
        return Token(token_str,"KEYWORD")
    else:       
        return Token(token_str,"ID")


  
def get_next_token (i,line):
    n=len(line)
    l_num=i
    line=Line(i,line)
    line.pointer_loc=0
    
    if line[line.pointer_loc] in Type_of_tokens ["SYMBOL"]:
        Token(line[line.pointer_loc],"SYMBOL")
        
    elif line[line.pointer_loc] in Type_of_tokens ["NUM"]:
            lookahead_NUM(l_num,line)
            
    elif line[line.pointer_loc]in Type_of_tokens["letter"] :
        lookahead_IDKEYWORD(l_num,line)    
  
            
    

     
file1 = open("input.txt", "r") 
file2=open("tokens.txt", "w")
line_list = file1.readlines();
for line in line_list:
    get_next_token(line_list.index(line),line)
file2.write(tokens)
file2.close()
file1.close() 

    
     
     
     
     
     
     
     
     
     
    
    
    
        
        