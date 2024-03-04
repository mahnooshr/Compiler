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
        
def lookahead_NUM (j,str):
    token_str=""
    line=Line(i,line)
    for i in range(line.pointer_loc,len(str)):
        if str[i] in Type_of_tokens["NUM"] :
            token_str+=str[i]
            line.pointer_loc+=1
        else:
            break
    return Token(token_str,"NUM")
  
def get_next_token (i,line):
    n=len(line)
    l_num=i
    line=Line(i,line)
    line.pointer_loc=0
    
    if line[line.pointer_loc] in Type_of_tokens ["SYMBOL"]:
        Token(line[line.pointer_loc],"SYMBOL")
        
    else:
        token_str=""
        while line[line.pointer_loc] in Type_of_tokens["NUM"]
            token_str+=line[line.pointer_loc]
            line.pointer_loc+=1
            lookahead_NUM(l_num,line)
            
    elif line[line.pointer_loc]in Type_of_tokens["letter"] :
        lookahead_NUM(line)    
  
            
    

     
file1 = open("input.txt", "r") 
file2=open("tokens.txt", "w")
line_list = file1.readlines();
for line in line_list:
    str = line
    get_next_token(line_list.index(line),line)
    ;
    ;
    ;
    l_num = l_num + 1;

file1.close() 



file2.write(l_num +   )


file2.close()
    
     
     
     
     
     
     
     
     
     
    
    
    
        
        