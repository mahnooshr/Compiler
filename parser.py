import scanner
from anytree import RenderTree, Node

tree = []

error=[]
first_sets = {
        "Program": [";","[","(","int","void"],
        "Declaration_list" : [";","[","(","int","void"],
        "Declaration" : [";","[","(","int","void"],
         "Declaration_initial": ["int","void"]

    }

follow_set ={
    "Program": [";","[","(","int","void"],
}
class Parser:

    def __init__(self):
        self.lookahead = scanner.get_next_token()

    def Match(self, token, num_of_item):
        if self.lookahead.term == token:
            if self.lookahead.value == '$':
                tree.append(Node('$', parent= tree[0]))
                return
            tree.append(Node(self.lookahead, parent=tree[num_of_item]))
            self.lookahead = scanner.get_next_token()
        else:
             error.append(f"#{scanner.line_no+1} : syntax error, missing {self.lookahead.term}")
             self.lookahead = token
             return



    def Program(self, num_of_item):
        if self.lookahead.term in ['int', 'void', 'ID', ';', 'NUM', '(', ' {', '}', 'break', 'if', 'for', 'return', '+',
                                   '-', '$']:
            tree.append(Node("Declaration-list", parent=tree[num_of_item]))
            self.Declaration_list(len(tree) - 1)
        else:
            error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
            self.lookahead = scanner.get_next_token()
            self.Program(num_of_item)

    def Declaration_list(self, num_of_item):
        if self.lookahead.term in ['int', 'void']:
            tree.append(Node("Declaration", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Declaration-list", parent=tree[num_of_item]))
            self.Declaration(temp)
            self.Declaration_list(temp + 1)
        elif self.lookahead.term in ['ID', ';', 'NUM', '(', ' {', '}', 'break', 'if', 'for', 'return', '+', '-', '$']:
            tree.append(Node("epsilon", parent=tree[num_of_item]))

            if self.lookahead.value == '$':
                self.Match('$',0)
            return
        else:
            error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
            self.lookahead = scanner.get_next_token()
            self.Declaration_list(len(tree) - 1)

    def Declaration(self, num_of_item):
        if self.lookahead.term in ['int', 'void']:
            tree.append(Node("Declaration-initial", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Declaration-prime", parent=tree[num_of_item]))
            self.Declaration_initial(temp)
            self.Declaration_prime(temp + 1)
        else:
            if self.lookahead.term in ['ID',';','NUM','(','int','void','{','}','break','if','for','return','+', '-', '$']:
                error.append(f"#{scanner.line_no + 1} : syntax error, illegal Declaration")
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Declaration(len(tree) - 1)

    def Declaration_initial(self, num_of_item):
        if self.lookahead.term in ['int', 'void']:
            tree.append(Node("Type-specifier", parent=tree[num_of_item]))
            self.Type_specifier(len(tree) - 1)
            self.Match('ID', num_of_item)
        else:
            if self.lookahead.term in [';','[','(',')',',']:
                self.Match('int', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Declaration_initial(len(tree) - 1)

    def Declaration_prime(self, num_of_item):
        if self.lookahead.term in ['(']:
            tree.append(Node("Fun-declaration-prime", parent=tree[num_of_item]))
            self.Fun_declaration_prime(len(tree) - 1)
        elif self.lookahead.term in [';', '[']:
            tree.append(Node("Var-declaration-prime", parent=tree[num_of_item]))
            self.Var_declaration_prime(len(tree) - 1)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return',
                                       '+', '-', '$']:
                self.Match('(', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Declaration_prime(len(tree) - 1)
    def Var_declaration_prime(self, num_of_item):
        if self.lookahead.term in [';']:
            self.Match(';', num_of_item)
        elif self.lookahead.term in ['[']:
            self.Match('[', num_of_item)
            self.Match('NUM', num_of_item)
            self.Match(']', num_of_item)
            self.Match(';', num_of_item)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return',
                                       '+', '-', '$']:
                self.Match(';', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Var_declaration_prime(len(tree) - 1)

    def Fun_declaration_prime(self, num_of_item):
        if self.lookahead.term in ['(']:
            self.Match('(', num_of_item)
            tree.append(Node("Params", parent=tree[num_of_item]))
            temp = len(tree) - 1
            self.Params(temp)
            self.Match(')', num_of_item)
            tree.append(Node("Compound-stmt", parent=tree[num_of_item]))
            tmp = len(tree) - 1
            self.Compound_stmt(tmp)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'for', 'return',
                                       '+', '-', '$']:
                self.Match('(', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Fun_declaration_prime(len(tree) - 1)

    def Type_specifier(self, num_of_item):
        if self.lookahead.term in ['int']:
            self.Match('int', num_of_item)
        elif self.lookahead.term in ['void']:
            self.Match('void', num_of_item)
        else:
            if self.lookahead.term in ['ID']:
                self.Match('int', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Type_specifier(len(tree) - 1)

    def Params(self, num_of_item):
        if self.lookahead.term in ['int']:
            self.Match('int', num_of_item)
            self.Match('ID', num_of_item)
            tree.append(Node("Param-prime", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Param-list", parent=tree[num_of_item]))
            self.Param_prime(temp)
            self.Param_list(temp + 1)
        elif self.lookahead.term in ['void']:
            self.Match('void', num_of_item)
        else:
            if self.lookahead.term in [')']:
                self.Match('int', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Params(len(tree) - 1)

    def Param_list(self, num_of_item):
        if self.lookahead.term in [',']:
            self.Match(',', num_of_item)
            tree.append(Node("Param", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Param-list", parent=tree[num_of_item]))
            self.Param(temp)
            self.Param_list(temp + 1)
        elif self.lookahead.term in [')']:
            tree.append(Node("epsilon", parent=tree[num_of_item]))
            return
        else:

            error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
            self.lookahead = scanner.get_next_token()
            self.Param_list(len(tree) - 1)

    def Param(self, num_of_item):
        if self.lookahead.term in ['int', 'void']:
            tree.append(Node("Declaration-initial", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Param-prime", parent=tree[num_of_item]))
            self.Declaration_initial(num_of_item)
            self.Param_prime(num_of_item)
        else:
            if self.lookahead.term in [')',',']:
                self.Match('void', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Param(len(tree) - 1)

    def Param_prime(self, num_of_item):
        if self.lookahead.term  in ['[']:
            self.Match('[', num_of_item)
            self.Match(']', num_of_item)
        elif self.lookahead.term in [')', ',']:
            tree.append(Node("epsilon", parent=tree[num_of_item]))
            return
        else:
            error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
            self.lookahead = scanner.get_next_token()
            self.Param_prime(len(tree)-1)

    def Compound_stmt(self, num_of_item):
        if self.lookahead.term in ['{']:
            self.Match('{', num_of_item)
            tree.append(Node("Declaration-list", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Statement-list", parent=tree[num_of_item]))
            self.Declaration_list(temp)
            self.Statement_list(temp + 1)
            self.Match('}', num_of_item)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'for','endif','else', 'return',
                                       '+', '-', '$']:
                self.Match('{', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Compound_stmt(len(tree) - 1)

    def Statement_list(self, num_of_item):
        if self.lookahead.term in ['ID', ',', '(', '{', 'break', 'if', 'for', 'return', '+', '-']:
            tree.append(Node("Statement", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Statement-list", parent=tree[num_of_item]))
            self.Statement(temp)
            self.Statement_list(temp + 1)
        elif self.lookahead.term in ['}']:
            tree.append(Node("epsilon", parent=tree[num_of_item]))
            return
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Statement_list(len(tree) - 1)

    def Statement(self, num_of_item):
        if self.lookahead.term in ['ID', ';', 'NUM', '(', 'break', '+', '-']:
            tree.append(Node("Expression-stmt", parent=tree[num_of_item]))
            self.Expression_stmt(len(tree) - 1)
        elif self.lookahead.term in ['{']:
            tree.append(Node("Compound-stmt", parent=tree[num_of_item]))
            self.Compound_stmt(len(tree) - 1)
        elif self.lookahead.term in ['if']:
            tree.append(Node("Selection-stmt", parent=tree[num_of_item]))
            self.Selection_stmt(len(tree) - 1)
        elif self.lookahead.term in ['for']:
            tree.append(Node("Iteration-stmt", parent=tree[num_of_item]))
            self.Iteration_stmt(len(tree) - 1)
        elif self.lookahead.term in ['return']:
            tree.append(Node("Return-stmt", parent=tree[num_of_item]))
            self.Return_stmt(len(tree) - 1)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'endif',
                                       'else', 'return',
                                       '+', '-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Statement_list(len(tree) - 1)

    def Expression_stmt(self, num_of_item):
        if self.lookahead.term in ['ID', 'NUM', '(', '+', '-']:
            tree.append(Node("Expression", parent=tree[num_of_item]))
            self.Expression(len(tree) - 1)
            self.Match(';', num_of_item)
        elif self.lookahead.term in ['break']:
            self.Match('break', num_of_item)
            self.Match(';', num_of_item)
        elif self.lookahead.term in [';']:
            self.Match(';', num_of_item)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'endif',
                                       'else', 'return',
                                       '+', '-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Expression_stmt(len(tree) - 1)

    def Selection_stmt(self, num_of_item):
        if self.lookahead.term in ['if']:
            self.Match('if', num_of_item)
            self.Match('(', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            temp = len(tree) - 1
            self.Expression(temp)
            self.Match(')', num_of_item)
            tree.append(Node("Statement", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Else-stmt", parent=tree[num_of_item]))
            self.Statement(temp)
            self.Else_stmt(temp+1)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'endif',
                                       'else', 'return',
                                       '+', '-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Selection_stmt(len(tree) - 1)

    def Else_stmt(self, num_of_item):
        if self.lookahead.term in ['endif']:
            self.Match('endif', num_of_item)
        elif self.lookahead.term in ['else']:
            self.Match('else', num_of_item)
            tree.append(Node("Statement", parent=tree[num_of_item]))
            self.Statement(len(tree) - 1)
            self.Match('endif', num_of_item)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'endif',
                                       'else', 'return',
                                       '+', '-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Else_stmt(len(tree) - 1)

    def Iteration_stmt(self, num_of_item):
        if self.lookahead.term in ['for']:
            self.Match('for', num_of_item)
            self.Match('(', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Expression", parent=tree[num_of_item]))
            tree.append(Node("Expression", parent=tree[num_of_item]))
            tree.append(Node("Statement", parent=tree[num_of_item]))
            self.Expression(temp)
            self.Match(';', num_of_item)
            self.Expression(temp + 1)
            self.Match(';', num_of_item)
            self.Expression(temp + 2)
            self.Match(')', num_of_item)
            self.Statement(temp + 3)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'endif',
                                       'else', 'return',
                                       '+', '-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Iteration_stmt(len(tree) - 1)

    def Return_stmt(self, num_of_item):
        if self.lookahead.term in ['return']:
            self.Match('return', num_of_item)
            tree.append(Node("Return-stmt-prime", parent=tree[num_of_item]))
            self.Return_stmt_prime(len(tree) - 1)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'endif',
                                       'else', 'return',
                                       '+', '-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Return_stmt(len(tree) - 1)

    def Return_stmt_prime(self, num_of_item):
        if self.lookahead.term in [';']:
            self.Match(';', num_of_item)
        elif self.lookahead.term in ['ID', 'NUM', '(', '+', '-']:
            tree.append(Node("Expression", parent=tree[num_of_item]))
            self.Expression(len(tree) - 1)
            self.Match(';', num_of_item)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'for', 'endif',
                                       'else', 'return',
                                       '+', '-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Return_stmt_prime(len(tree) - 1)

    def Expression(self, num_of_item):
        if self.lookahead.term in ['NUM', '(', '+', '-']:
            tree.append(Node("Simple-expression-zegond", parent=tree[num_of_item]))
            self.Simple_expression_zegond(len(tree) - 1)
        elif self.lookahead.term in ['ID']:
            self.Match('ID', num_of_item)
            tree.append(Node("B", parent=tree[num_of_item]))
            self.B(len(tree) -1)

        else:
            if self.lookahead.term in [';',']',')',',']:
                self.Match('NUM', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Expression(len(tree) - 1)

    def B(self, num_of_item):
        if self.lookahead.term in ['=']:
            self.Match('=', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            self.Expression(len(tree) - 1)
        elif self.lookahead.term in ['[']:
            self.Match('[', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            temp = len(tree) - 1
            self.Expression(temp)
            self.Match(']', num_of_item)
            tree.append(Node("H", parent=tree[num_of_item]))
            temp = len(tree) - 1
            self.H(temp)
        elif self.lookahead.term in ['(', '<', '==', '+', '-', '*', ';', ']', ')', ',']:
            tree.append(Node("Simple-expression-prime", parent=tree[num_of_item]))
            self.Simple_expression_prime(len(tree) - 1)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.B(len(tree) - 1)

    def H(self, num_of_item):
        if self.lookahead.term in ['=']:
            self.Match('=', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            self.Expression(len(tree) - 1)
        elif self.lookahead.term in ['*', ';', ']', ')', ',', '<', '==', '+', '-']:
            tree.append(Node("G", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("D", parent=tree[num_of_item]))
            tree.append(Node("C", parent=tree[num_of_item]))
            self.G(temp)
            self.D(temp + 1)
            self.C(temp + 2)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.H(len(tree) - 1)

    def Simple_expression_zegond(self, num_of_item):
        if self.lookahead.term in ['NUM', '(', '+', '-']:
            tree.append(Node("Additive-expression-zegond", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("C", parent=tree[num_of_item]))
            self.Additive_expression_zegond(temp)
            self.C(temp + 1)
        else:

            if self.lookahead.term in [';', ']', ')', ',']:
                self.Match('NUM', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Signed_factor_zegond(len(tree) - 1)

    def Simple_expression_prime(self, num_of_item):
        if self.lookahead.term in [';', ']', ')', ',', '<', '==', '*', '-', '+', '(']:
            tree.append(Node("Additive-expression-prime", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("C", parent=tree[num_of_item]))
            self.Additive_expression_prime(temp)
            self.C(temp + 1)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Signed_factor_prime(len(tree) - 1)

    def C(self, num_of_item):
        if self.lookahead.term in ['<', '==']:
            tree.append(Node("Relop", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Additive-expression", parent=tree[num_of_item]))
            self.Relop(temp)
            self.Additive_expression(temp + 1)
        elif self.lookahead.term in [';', ']', ')', ',']:
            self.Match('<', num_of_item)
            return
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.C(len(tree) - 1)

    def Relop(self, num_of_item):
        if self.lookahead.term in ['<']:
            self.Match('<', num_of_item)
        elif self.lookahead.term in ['==']:
            self.Match('==', num_of_item)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(',
                                       '+', '-']:
                self.Match('<', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Relop(len(tree) - 1)

    def Additive_expression(self, num_of_item):
        if self.lookahead.term in ['ID', 'NUM', '(', '+', '-']:
            tree.append(Node("Term", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("D", parent=tree[num_of_item]))
            self.Term(temp)
            self.D(temp + 1)
        else:
            if self.lookahead.term in [';', ']', ')', ',']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Additive_expression(len(tree) - 1)

    def Additive_expression_prime(self, num_of_item):
        if self.lookahead.term in ['(', '*', ';', ']', ')', ',', '<', '==', '+', '-']:
            tree.append(Node("Term-prime", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("D", parent=tree[num_of_item]))
            self.Term_prime(temp)
            self.D(temp + 1)

        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Additive_expression_prime(len(tree) - 1)

    def Additive_expression_zegond(self, num_of_item):
        if self.lookahead.term in ['NUM', '(', '+', '-']:
            tree.append(Node("Term-zegond", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("D", parent=tree[num_of_item]))
            self.Term_zegond(temp)
            self.D(temp + 1)
        else:
            if self.lookahead.term in [';', ']', ')', ',','<','==']:
                self.Match('NUM', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Additive_expression_zegond(len(tree) - 1)

    def D(self, num_of_item):
        if self.lookahead.term in ['+', '-']:
            tree.append(Node("Addop", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Term", parent=tree[num_of_item]))
            tree.append(Node("D", parent=tree[num_of_item]))
            self.Addop(temp)
            self.Term(temp + 1)
            self.D(temp + 2)
        elif self.lookahead.term in [';', ']', ')', ',', '<', '==']:
            self.Match('+', num_of_item)
            return
        else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.D(len(tree) - 1)

    def Addop(self, num_of_item):
        if self.lookahead.term in ['+']:
            self.Match('+', num_of_item)
        elif self.lookahead.term in ['-']:
            self.Match('-', num_of_item)
        else:
            if self.lookahead.term in ['ID', ';', 'NUM', '(',
                                       '+', '-']:
                self.Match('+', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Addop(len(tree) - 1)

    def Term(self, num_of_item):
        if self.lookahead.term in ['ID', 'NUM', '(', '+', '-']:
            tree.append(Node("Signed-factor", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("G", parent=tree[num_of_item]))
            self.Signed_factor(temp)
            self.G(temp + 1)
        else:
            if self.lookahead.term in [';', ']', ')', ',', '<', '==','+','-']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Term(len(tree) - 1)

    def Term_prime(self, num_of_item):
        if self.lookahead.term in ['(', ';', ']', ')', ',', '<', '==', '+', '-', '*']:
            tree.append(Node("Signed-factor-prime", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("G", parent=tree[num_of_item]))
            self.Signed_factor_prime(temp)
            self.G(temp + 1)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Term_prime(len(tree) - 1)

    def Term_zegond(self, num_of_item):
        if self.lookahead.term in ['NUM', '(', '+', '-']:
            tree.append(Node("Signed-factor-zegond", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("G", parent=tree[num_of_item]))
            self.Signed_factor_zegond(temp)
            self.G(temp + 1)
        else:
            if self.lookahead.term in [';', ']', ')', ',', '<', '==', '-','+']:
                self.Match('NUM', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Term_zegond(len(tree) - 1)

    def G(self, num_of_item):
        if self.lookahead.term in ['*']:
            self.Match('*', num_of_item)
            tree.append(Node("Signed-factor", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("G", parent=tree[num_of_item]))
            self.Signed_factor(temp)
            self.G(temp + 1)
        elif self.lookahead.term in [';', ']', ')', ',', '<', '==', '+', '-']:
            self.Match('*', num_of_item)
            return
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.G(len(tree) - 1)

    def Signed_factor(self, num_of_item):
        if self.lookahead.term in ['+']:
            self.Match('+', num_of_item)
            tree.append(Node("Factor", parent=tree[num_of_item]))
            self.Factor(len(tree) - 1)
        elif self.lookahead.term in ['-']:
            self.Match('-', num_of_item)
            tree.append(Node("Factor", parent=tree[num_of_item]))
            self.Factor(len(tree) - 1)
        elif self.lookahead.term in ['ID', 'NUM', '(']:
            tree.append(Node("Factor", parent=tree[num_of_item]))
            self.Factor(len(tree) - 1)
        else:
            if self.lookahead.term in [';', ']', ')', ',', '<', '==', '-', '+','*']:
                self.Match('+', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Signed_factor(len(tree) - 1)

    def Signed_factor_prime(self, num_of_item):
        if self.lookahead.term in ['(', ';', ']', ')', ',', '<', '==', '+', '-', '*']:
            tree.append(Node("Factor-prime", parent=tree[num_of_item]))
            self.Factor_prime(len(tree) - 1)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Signed_factor_prime(len(tree) - 1)

    def Signed_factor_zegond(self, num_of_item):
        if self.lookahead.term in ['+']:
            self.Match('+', num_of_item)
            tree.append(Node("Factor", parent=tree[num_of_item]))
            self.Factor(len(tree) - 1)
        elif self.lookahead.term in ['-']:
            self.Match('-', num_of_item)
            tree.append(Node("Factor", parent=tree[num_of_item]))
            self.Factor(len(tree) - 1)
        elif self.lookahead.term in ['NUM', '(']:
            tree.append(Node("Factor-zegond", parent=tree[num_of_item]))
            self.Factor_zegond(len(tree) - 1)
        else:
            if self.lookahead.term in [';', ']', ')', ',', '<', '==', '-', '+', '*']:
                self.Match('+', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Signed_factor_zegond(len(tree) - 1)

    def Factor(self, num_of_item):
        if self.lookahead.term in ['(']:
            self.Match('(', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            self.Expression(len(tree) - 1)
            self.Match(')', num_of_item)
        elif self.lookahead.term in ['ID']:
            self.Match('ID', num_of_item)
            tree.append(Node("Var-call-prime", parent=tree[num_of_item]))
            self.Var_call_prime(len(tree) - 1)
        elif self.lookahead.term in ['NUM']:
            self.Match('NUM', num_of_item)
        else:
            if self.lookahead.term in [';', ']', ')', ',', '<', '==', '-', '+', '*']:
                self.Match('(', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Factor(len(tree) - 1)

    def Var_call_prime(self, num_of_item):
        if self.lookahead.term in ['(']:
            self.Match('(', num_of_item)
            tree.append(Node("Args", parent=tree[num_of_item]))
            self.Args(len(tree) - 1)
            self.Match(')', num_of_item)
        elif self.lookahead.term in ['[', ';', ']', ')', ',', '<', '==', '+', '-', '*']:
            tree.append(Node("Var-prime", parent=tree[num_of_item]))
            self.Var_prime(len(tree) - 1)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Var_call_prime(len(tree) - 1)

    def Var_prime(self, num_of_item):
        if self.lookahead.term in ['[']:
            self.Match('[', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            self.Expression(len(tree) - 1)
            self.Match(']', num_of_item)
        elif self.lookahead.term in [';', ']', ')', ',', '<', '==', '+', '-', '*']:
            self.Match('[', num_of_item)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Var_prime(len(tree) - 1)

    def Factor_prime(self, num_of_item):
        if self.lookahead.term in ['(']:
            self.Match('(', num_of_item)
            tree.append(Node("Args", parent=tree[num_of_item]))
            self.Args(len(tree) - 1)
            self.Match(')', num_of_item)
        elif self.lookahead.term in [';', ']', ')', ',', '<', '==', '+', '-', '*']:
            self.Match('(', num_of_item)
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Factor_prime(len(tree) - 1)

    def Factor_zegond(self, num_of_item):
        if self.lookahead.term in ['(']:
            self.Match('(', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            self.Expression(len(tree) - 1)
            self.Match(')', num_of_item)
        elif self.lookahead.term in ['NUM']:
            self.Match('NUM', num_of_item)
        else:
            if self.lookahead.term in [';', ']', ')', ',', '<', '==', '-', '+', '*']:
                self.Match('(', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Factor_zegond(len(tree) - 1)

    def Args(self, num_of_item):
        if self.lookahead.term in ['ID', 'NUM', '(', '+', '-']:
            tree.append(Node("Arg-list", parent=tree[num_of_item]))
            self.Arg_list(len(tree) - 1)
        elif self.lookahead.term in [')']:
            tree.append(Node("epsilon", parent=tree[num_of_item]))
            return
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Args(len(tree) - 1)

    def Arg_list(self, num_of_item):
        if self.lookahead.term in ['ID', 'NUM', '(', '+', '-']:
            tree.append(Node("Expression", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Arg-list-prime", parent=tree[num_of_item]))
            self.Expression(temp)
            self.Arg_list_prime(temp + 1)

        else:
            if self.lookahead.term in [')']:
                self.Match('ID', num_of_item)
                return
            else:
                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Arg_list(len(tree) - 1)

    def Arg_list_prime(self, num_of_item):
        if self.lookahead.term in [',']:
            self.Match(',', num_of_item)
            tree.append(Node("Expression", parent=tree[num_of_item]))
            temp = len(tree) - 1
            tree.append(Node("Arg-list-prime", parent=tree[num_of_item]))
            self.Expression(temp)
            self.Arg_list_prime(temp + 1)
        elif self.lookahead.term in [')']:
            tree.append(Node("epsilon", parent=tree[num_of_item]))
            return
        else:

                error.append(f"#{scanner.line_no+1} : syntax error, illegal {self.lookahead.term}")
                self.lookahead = scanner.get_next_token()
                self.Arg_list_prime(len(tree) - 1)

def print_parse_tree():
    with open("parse_tree.txt", "w+", encoding="utf-8") as f:
        for pre, fill, node in RenderTree(tree[0]):
            f.write("%s%s\n" % (pre, node.name))


parser = Parser()
tree.append(Node("Program"))
parser.Program(0)
print_parse_tree()

with open("syntax_errors.txt", "w+", encoding="utf-8") as f:
    if len(error) > 0:
        for errors in error:
            f.write(errors+"\n")
    else:
        f.write("There is no syntax error.")