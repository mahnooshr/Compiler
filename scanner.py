# Compiler project phase 2 - Scanner
# Mahdi Mohammadi 400105239
# Mahnoosh Ramtin 99101592


Type_of_tokens = {
    "NUM": "0123456789",
    "ID": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "letters": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "KEYWORD": ["if", "else", "void", "int", "for", "break", "return", "endif"],
    "SYMBOL": [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", "=="],
    "COMMENT": "/*",
    "WHITESPACE": ["\n", "\r", "\t", "\v", "\f", " "]
}
symbols = Type_of_tokens["KEYWORD"].copy()
tokens = []
text = []
txt = ""
errors = []
line_no = 0
pointer_location = 0
with open('input.txt', "r") as file1:
    for j, ln in enumerate(file1):
        text.append(ln)


def read_file_into_list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


file = read_file_into_list('input.txt')

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.term = value
        tokens.append(self)

    def __str__(self):
        return f"({self.type}, {self.value})"


class Line:
    def __init__(self, number, line, pointer_loc):
        self.line_number = number
        self.pointer_loc = pointer_loc
        self.line = line
        self.errors = errors

    def lookahead_Sym(self):
        global pointer_location
        if (str(self.line[self.pointer_loc]) == "=") and (str(self.line[self.pointer_loc + 1]) == "="):
            # if str(self.line[self.pointer_loc+1])=="=":
            self.pointer_loc += 2
            token_str = "=="
        else:
            token_str = self.line[self.pointer_loc]
            self.pointer_loc += 1

        pointer_location = self.pointer_loc
        return Token(token_str, "SYMBOL")

    def lookahead_comment(self):
        global pointer_location

        rst = text.copy()

        i = 1
        while i < self.line_number:
            rst.pop(0)
            i = i + 1
        rest = ''.join(rst)
        rest = rest.strip()
        # rest = rest + '\n'
        rest = rest[self.pointer_loc + 1:]
        end = rest.find("*/")
        if end != -1:
            token_str = rest[0:end + 1]
            num_of_lines = token_str.count('\n')
            if num_of_lines == 0:
                self.pointer_loc += len(token_str) + 2
            pointer_location = self.pointer_loc
            return num_of_lines

        else:
            stt = ""
            z = 0

            while self.pointer_loc + 2 < len(self.line):
                stt += self.line[self.pointer_loc + 2]
                self.pointer_loc += 1
                z += 1
                if z == 5:
                    break
            stt = stt + "..."
            errors.append(f"({'/*'}{stt}, {'Unclosed comment'})")
            return -2

    def lookahead_NUM(self):
        global pointer_location
        token_str = ""
        while self.pointer_loc < len(self.line) and self.line[self.pointer_loc] in Type_of_tokens["NUM"]:
            token_str += self.line[self.pointer_loc]
            self.pointer_loc += 1
        if len(self.line) > self.pointer_loc + 1:
            if self.line[self.pointer_loc] in Type_of_tokens["SYMBOL"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["COMMENT"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["WHITESPACE"]:
                pointer_location = self.pointer_loc
                temp = Token(token_str, "NUM")
                temp.term = temp.type
                return temp

            elif self.line[self.pointer_loc] in Type_of_tokens["letters"]:
                token_str += self.line[self.pointer_loc]

                errors.append(f"({token_str}, {'Invalid number'})")
                self.pointer_loc += 1
                return -1
            else:
                token_str += self.line[self.pointer_loc]

                errors.append(f"({token_str}, {'Invalid input'})")
                self.pointer_loc += 1
        else:
            pointer_location = self.pointer_loc
            temp = Token(token_str, "NUM")
            temp.term = temp.type
            return temp

    def lookahead_IDKEYWORD(self):
        global pointer_location
        token_str = ""
        while self.pointer_loc < len(self.line) and self.line[self.pointer_loc] in Type_of_tokens["ID"]:
            token_str += self.line[self.pointer_loc]
            self.pointer_loc += 1
        if len(self.line) > self.pointer_loc + 1:
            if self.line[self.pointer_loc] in Type_of_tokens["SYMBOL"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["COMMENT"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["WHITESPACE"]:

                if token_str in Type_of_tokens["KEYWORD"]:
                    pointer_location = self.pointer_loc
                    return Token(token_str, "KEYWORD")
                else:
                    if token_str not in symbols:
                        symbols.append(token_str)
                    pointer_location = self.pointer_loc
                    temp = Token(token_str, "ID")
                    temp.term = temp.type
                    return temp
            else:

                token_str += self.line[self.pointer_loc]
                errors.append(f"({token_str}, {'Invalid input'})")
                self.pointer_loc += 1
                return -1

        else:

            if token_str in Type_of_tokens["KEYWORD"]:
                pointer_location = self.pointer_loc
                return Token(token_str, "KEYWORD")
            else:
                if token_str not in symbols:
                    symbols.append(token_str)

                pointer_location = self.pointer_loc
                temp = Token(token_str, "ID")
                temp.term = temp.type
                return temp

def get_next_token():
    global line_no, pointer_location
    while True:
        if line_no == len(file):
            return Token('$', '$')
        line_obj = Line(line_no + 1, file[line_no], pointer_location)
        if line_obj.pointer_loc < len(line_obj.line):
            if (str(line_obj.line[line_obj.pointer_loc]) == "*") and (str(line_obj.line[line_obj.pointer_loc + 1]) == "/"):
                    errors.append(f"({'*/'}, {'Unmatched comment'})")
                    line_obj.pointer_loc = line_obj.pointer_loc + 2
            elif line_obj.line[line_obj.pointer_loc] in Type_of_tokens["SYMBOL"]:
                return line_obj.lookahead_Sym()
            elif line_obj.line[line_obj.pointer_loc] in Type_of_tokens["NUM"]:
                return line_obj.lookahead_NUM()
            elif line_obj.line[line_obj.pointer_loc] in Type_of_tokens["letters"]:
                return line_obj.lookahead_IDKEYWORD()
            elif str(line_obj.line[line_obj.pointer_loc]) == "/":
                if str(line_obj.line[line_obj.pointer_loc + 1]) == "*":
                    line_no = line_no + line_obj.lookahead_comment()
            elif line_obj.line[line_obj.pointer_loc] in Type_of_tokens["WHITESPACE"]:
                pointer_location += 1

            else:
                pointer_location += 1
        else:
            line_no = line_no + 1
            pointer_location = 0