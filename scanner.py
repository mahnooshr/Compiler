Type_of_tokens = {
    "NUM": "0123456789",
    "ID": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "letters": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "KEYWORD": ["if", "else", "void", "int", "for", "break", "return", "endif"],
    "SYMBOL": [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", "=="],
    "COMMENT": "///",
    "WHITESPACE": "\n\r\t\v\f"
}

tokens = []

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        tokens.append(self)

    def __str__(self):
        return f"({self.type}, {self.value})"

class Line:
    def __init__(self, number, line):
        self.line_number = number
        self.pointer_loc = 0
        self.line = line

    def lookahead_NUM(self):
        token_str = ""
        while self.pointer_loc < len(self.line) and self.line[self.pointer_loc] in Type_of_tokens["NUM"]:
            token_str += self.line[self.pointer_loc]
            self.pointer_loc += 1
        return Token(token_str, "NUM")

    def lookahead_IDKEYWORD(self):
        token_str = ""
        while self.pointer_loc < len(self.line) and self.line[self.pointer_loc] in Type_of_tokens["ID"]:
            token_str += self.line[self.pointer_loc]
            self.pointer_loc += 1
        if token_str in Type_of_tokens["KEYWORD"]:
            return Token(token_str, "KEYWORD")
        else:
            return Token(token_str, "ID")

    def get_next_token(self):
        while self.pointer_loc < len(self.line):
            if self.line[self.pointer_loc] in Type_of_tokens["SYMBOL"]:
                token = Token(self.line[self.pointer_loc], "SYMBOL")
                self.pointer_loc += 1
                return token
            elif self.line[self.pointer_loc] in Type_of_tokens["NUM"]:
                return self.lookahead_NUM()
            elif self.line[self.pointer_loc] in Type_of_tokens["letters"]:
                return self.lookahead_IDKEYWORD()
            elif self.line[self.pointer_loc] in Type_of_tokens["WHITESPACE"]:
                self.pointer_loc += 1
            else:
                self.pointer_loc += 1
        return None

def tokenize_file(filename):
    tokens.clear()
    with open(filename, "r") as file1:
        for i, line in enumerate(file1):
            line = line.strip()
            if line:
                line_obj = Line(i + 1, line)
                while True:
                    token = line_obj.get_next_token()
                    if token is None:
                        break

    with open("tokens.txt", "w") as file2:
        for token in tokens:
            file2.write(str(token) + "\n")

tokenize_file("input.txt")