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
    
    def __init__(self,number,str):    
        self.line_number=number
        self.pointer_loc=0
        self.str=str


def lookahead_NUM (i,line):
    token_str=""
    # line=Line(i,line)
    while str[line.pointer_loc] in Type_of_tokens["NUM"] :
        token_str+=str[line.pointer_loc]
        line.pointer_loc+=1
    if str[line.pointer_loc] in Type_of_tokens["letters"]:
        return #error
    else:
               
        return Token(token_str,"NUM")


def lookahead_IDKEYWORD (j,line):
    token_str=""
    # line=Line(j,str)
    while line.str[line.pointer_loc] in Type_of_tokens["ID"] :
            token_str+=line.str[line.pointer_loc]
            line.pointer_loc+=1
    if token_str in Type_of_tokens["KEYWORD"]:
        return Token(token_str,"KEYWORD")
    else:       
        return Token(token_str,"ID")


  
def get_next_token (i,line):
    n=len(line)
    l_num=i
    l=Line(i,line)
    while (l.pointer_loc < n):
        if line[l.pointer_loc] in Type_of_tokens ["SYMBOL"]:
            Token(line[line.pointer_loc],"SYMBOL")
            l.pointer_loc += 1
        elif line[l.pointer_loc] in Type_of_tokens ["NUM"]:
                lookahead_NUM(l_num,l)
                
        elif line[l.pointer_loc]in Type_of_tokens["letters"] :
            lookahead_IDKEYWORD(l_num,l)    
  
            
    

     
file1 = open("input.txt", "r") 
file2 = open("tokens.txt", "w")
line_list = file1.readlines();
for line in line_list:
    get_next_token(line_list.index(line)+1,line)
file2.write(tokens)
file2.close()
file1.close() 

    
     
     
     
     
     
     
     
     
     
    
    
    
        
        