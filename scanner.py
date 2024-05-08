# Compiler project phase 1
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
        self.errors = errors

    def lookahead_Sym(self):
        token_str = ""
        if (str(self.line[self.pointer_loc]) == "=") and (str(self.line[self.pointer_loc + 1]) == "="):
            # if str(self.line[self.pointer_loc+1])=="=":
            self.pointer_loc += 2
            token_str = "=="
        else:
            token_str = self.line[self.pointer_loc]
            self.pointer_loc += 1

        return Token(token_str, "SYMBOL")

    def lookahead_comment(self):
        token_str = ""

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
        token_str = ""
        while self.pointer_loc < len(self.line) and self.line[self.pointer_loc] in Type_of_tokens["NUM"]:
            token_str += self.line[self.pointer_loc]
            self.pointer_loc += 1
        if len(self.line) > self.pointer_loc + 1:
            if self.line[self.pointer_loc] in Type_of_tokens["SYMBOL"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["COMMENT"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["WHITESPACE"]:

                return Token(token_str, "NUM")

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
            return Token(token_str, "NUM")

    def lookahead_IDKEYWORD(self):
        token_str = ""
        while self.pointer_loc < len(self.line) and self.line[self.pointer_loc] in Type_of_tokens["ID"]:
            token_str += self.line[self.pointer_loc]
            self.pointer_loc += 1
        if len(self.line) > self.pointer_loc + 1:
            if self.line[self.pointer_loc] in Type_of_tokens["SYMBOL"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["COMMENT"] or \
                    self.line[self.pointer_loc] in Type_of_tokens["WHITESPACE"]:

                if token_str in Type_of_tokens["KEYWORD"]:

                    return Token(token_str, "KEYWORD")
                else:
                    if token_str not in symbols:
                        symbols.append(token_str)
                    return Token(token_str, "ID")
            else:

                token_str += self.line[self.pointer_loc]
                errors.append(f"({token_str}, {'Invalid input'})")
                self.pointer_loc += 1
                return -1

        else:

            if token_str in Type_of_tokens["KEYWORD"]:

                return Token(token_str, "KEYWORD")
            else:
                if token_str not in symbols:
                    symbols.append(token_str)

                return Token(token_str, "ID")

    def get_next_token(self):

        while self.pointer_loc < len(self.line):
            stri = ""
            if (str(self.line[self.pointer_loc]) == "*") and (str(self.line[self.pointer_loc + 1]) == "/"):
                    errors.append(f"({'*/'}, {'Unmatched comment'})")
                    self.pointer_loc = self.pointer_loc + 2
            elif self.line[self.pointer_loc] in Type_of_tokens["SYMBOL"]:
                return self.lookahead_Sym()
            elif self.line[self.pointer_loc] in Type_of_tokens["NUM"]:
                return self.lookahead_NUM()
            elif self.line[self.pointer_loc] in Type_of_tokens["letters"]:
                return self.lookahead_IDKEYWORD()
            elif str(self.line[self.pointer_loc]) == "/":
                if str(self.line[self.pointer_loc + 1]) == "*":
                    return self.lookahead_comment()
            elif self.line[self.pointer_loc] in Type_of_tokens["WHITESPACE"]:
                self.pointer_loc += 1

            else:
                stri = str(self.line[self.pointer_loc])
                errors.append(f"({stri}, {'Invalid input'})")
                self.pointer_loc += 1
        return None


def tokenize_file(filename):
    global txt
    tokens.clear()
    lexical_error_found = False  # Flag to track if any lexical error is found
    with open(filename, "r") as file1:
        for j, ln in enumerate(file1):
            text.append(ln)
    with open(filename, "r") as file1:
        token = ""
        for i, line in enumerate(file1):
            if (isinstance(token, int) and token > 0):
                token = token - 1
                continue
            line = line.strip()
            if line:
                line_obj = Line(i + 1, line)
                while True:
                    token = line_obj.get_next_token()
                    if token == -1:
                        continue
                    if token == -2:
                        break
                    if token is None or (isinstance(token, int) and token > 0):
                        break
                with open("tokens.txt", "a") as file2:
                    if i == 0:
                        file2.truncate(0)
                    if (len(tokens) != 0):
                        file2.write(str(i + 1) + ".\t")
                    for t in tokens:
                        file2.write(str(t) + " ")
                    if (len(tokens) != 0):
                        tokens.clear()
                        file2.write("\n")
                with open("lexical_errors.txt", "a") as file3:
                    if i == 0:
                        file3.truncate(0)
                    if (len(errors) != 0):
                        file3.write(str(i + 1) + ".\t")
                        lexical_error_found = True  # Set the flag if lexical error is found
                    for error in errors:
                        file3.write(str(error) + " ")
                    if (len(errors) != 0):
                        errors.clear()
                        file3.write("\n")
                if token == -2:
                    break
    if not lexical_error_found:
        with open("lexical_errors.txt", "a") as file3:
            file3.write("There is no lexical error.\n")


tokenize_file("input.txt")

with open("symbol_table.txt", "w") as symbol_table:
    for i, symbol in enumerate(symbols):
        symbol_table.write(str(i + 1) + ".\t" + symbol + "\n")
