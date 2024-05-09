import scanner

class Parser:

    def __init__(self):
        self.lookahead = scanner.get_next_token()
    def Match(self, token ):
        if self.lookahead == token:
            self.lookahead = scanner.get_next_token()
        else:
            return False

    def Program(self):
        if self.lookahead in ['int','void','ID',';', 'NUM', '(',' {','}', 'break', 'if','for','return','+','-','$']:
            self.Declaration_List()
        else:
            print("error")

    def Declaration_List(self):
        if self.lookahead in ['int', 'void']:
            self.Declaration()
            self.Declaration_List()
        elif self.lookahead in ['ID', ';', 'NUM', '(', ' {', '}', 'break', 'if', 'for', 'return', '+','-', '$']:
            return
        else:
            print("error")

    def Declaration(self):
        if self.lookahead in ['int', 'void']:
            self.Declaration_initial()
            self.Declaration_prime()
        else:
            print("error")


    def Declaration_initial(self):
        if self.lookahead in ['int', 'void']:
            self.Type_specifier()
            self.Math('ID')
        else:
            print("error")

    def Declaration_prime(self):
        if self.lookahead in ['(']:
            self.Fun_declaration_prime()
        elif self.lookahead in [';','[']:
            self.Var_declaration_prime()
        else:
            print("error")
    def Var_declaration_prime(self):
        if self.lookahead in [';']:
            self.Match(';')
        elif self.lookahead in ['[']:
            self.Match('[')
            self.Match('NUM')
            self.Match(']')
            self.Match(';')
        else:
            print("error")

    def Fun_declaration_prime(self):
        if self.lookahead in ['(']:
            self.Match('(')
            self.Params()
            self.Match(')')
            self.Compound_stmt()
        else:
            print("error")

    def Type_specifier(self):
        if self.lookahead in ['int']:
            self.Match('int')
        elif self.lookahead in ['void']:
            self.Match('void')
        else:
            print("error")

    def Params(self):
        if self.lookahead in ['int']:
            self.Match('int')
            self.Match('ID')
            self.Param_prime()
            self.Param_list()
        elif self.lookahead in ['void']:
            self.Match('void')
        else:
            print("error")

    def Param_list(self):
        if self.lookahead in [',']:
            self.Match(',')
            self.Param_Param_list()
        elif self.lookahead in [')']:
            return
        else:
            print("error")

    def Param(self):
        if self.lookahead in ['int', 'void']:
            self.Declaration_initial_Param_prime()
        else:
            print("error")
    def  Param_prime(self):
        if self.lookahead in ['[']:
            self.Match('[')
            self.Match(']')
        elif self.lookahead in [')',',']:
            return
        else:
            print("error")

    def Compound_stmt(self):
        if self.lookahead in ['{']:
            self.Match('{')
            self.Declaration_list()
            self.Statement_list()
            self.Match('}')
        else:
            print("error")

    def Statement_list(self):
        if self.lookahead in ['ID',',','(','{','break','if','for','return','+','-']:
            self.Statement()
            self.Statement_list()
        elif self.lookahead in ['}']:
            return
        else:
            print("error")

    def Statement(self):
        if self.lookahead in ['ID',';','NUM','(','break','+','-']:
            self. Expression_stmt()
        elif self.lookahead in ['{']:
            self.Compound_stmt()
        elif self.lookahead in ['if']:
            self.Selection_stmt()
        elif self.lookahead in ['for']:
            self. Iteration_stmt()
        elif self.lookahead in ['return']:
            self. Return_stmt()
        else:
            print("error")

    def Expression_stmt(self):
        if self.lookahead in ['ID','NUM','(','+','-']:
            self.Expression()
            self.Match(';')
        elif self.lookahead in ['break']:
            self.Match('break')
            self.Match(';')
        elif self.lookahead in [';']:
            self.Match(';')
        else:
            print("error")

    def Selection_stmt(self):
        if self.lookahead in ['if']:
            self.Match('if')
            self.Match('(')
            self.Expression()
            self.Match(')')
            self.Statement()
            self.Else_stmt()
        else:
            print("error")

    def Else_stmt(self):
        if self.lookahead in ['endif']:
            self.Match('endif')
        elif self.lookahead in ['else']:
            self.Match('else')
            self.Statement()
            self.Match('endif')
        else:
            print("error")

    def Iteration_stmt(self):
        if self.lookahead in ['for']:
            self.Match('for')
            self.Match('(')
            self.Expression()
            self.Match(';')
            self.Expression()
            self.Match(';')
            self.Expression()
            self.Match(')')
            self.Statement()
        else:
            print("error")

    def Return_stmt(self):
        if  self.lookahead in ['return']:
            self.Match('return')
            self.Return_stmt_prime()

        else:
            print('error')
    def Return_stmt_prime(self):
        if self.lookahead in [';']:
            self.Match(';')
        elif self.lookahead in ['ID','NUM','(','+','-']:
            self.Expression()
            self.Match(';')
        else:
            print('error')

    def Expression(self):
        if self.lookahead in ['NUM','(','+','-']:
            self.Simple_expression_zegond()
        elif self.lookahead in ['ID']:
            self.Match('ID')
            self.Match('B')

        else:
            print('error')

    def B(self):
        if self.lookahead in ['=']:
            self.Match('=')
            self.Expression()
        elif self.lookahead in ['[']:
            self.Match['[']
            self.Expression()
            self.Match[']']
            self.H()
        elif self.lookahead in ['(','<','==','+','-','*',';',']',')',',']:
            self.Simple_expression_prime()
        else:
            print('error')

    def H(self):
        if self.lookahead in ['=']:
            self.Match('=')
            self.Expression()
        elif self.lookahead in ['*',';',']',')',',','<','==','+','-']:
            self.G()
            self.D()
            self.C()
        else:
            print('error')

    def Simple_expression_zegond(self):
        if self.lookahead in ['NUM','(','+','-']:
            self.Additive_expression_prime()
            self.C()
        else:
            print('error')
    def Simple_expression_prime(self):
        if self.lookahead in [';', ']',')',',','<','==']:
            self.Additive_expression_prime()
            self.C()
        else:
            print('error')
    def C(self):
        if self.lookahead in ['<','==']:
            self.Relop()
            self.Additive_expression()
        elif self.lookahead in [';',']',')',',']:
            return
        else:
            print('error')

    def Relop(self):
        if self.lookahead in ['<']:
            self.Match('<')
        elif self.lookahead in ['==']:
            self.Match('==')
        else:
            print('error')

    def Additive_expression(self):
        if self.lookahead in ['ID','NUM','(','+','-']:
            self.Term()
            self.D()
        else:
            print('error')

    def Additive_expression_prime(self):
        if self.lookahead in ['(','*',';',']',')',',','<','==','+','-']:
            self.Term_prime()
            self.D()

        else:
            print('error')

    def Aditive_expression_zegond(self):
        if self.lookahead in ['NUM','(','+','-']:
            self.Term_zegond()
            self.D()
        else:
            print('error')

    def D(self):
        if self.lookahead in ['+','-']:
            self.Addop()
            self.Term()
            self.D()
        elif self.lookahead in [';',']',')',',','<','==']:
            return
        else:
            print('error')

    def Addop(self):
        if self.lookahead in ['+']:
            self.Match('+')
        elif self.lookahead in ['-']:
            self.Match('-')
        else:
            print('error')

    def Term(self):
        if self.lookahead in ['ID','NUM','(','+','-']:
            self.Signed_factor()
            self.G()
        else:
            print('error')

    def Term_prime(self):
        if self.lookahead in ['(',';',']',')',',','<','==','+','-','*']:
            self.Signed_factor_prime()
            self.G()
        else:
            print('error')

    def Term_zegond(self):
        if self.lookahead in ['NUM','(','+','-']:
            self.Signed_factor_zegond()
            self.G()
        else:
            print('error')


    def G(self):
      if self.lookahead in ['*']:
        self.Match('*')
        self.Signed_factor()
        self.G()
      elif self.lookahead in [';',']',')',',','<','==','+','-']:
        return
      else:
        print('error')

    def Signed_factor(self):
        if self.lookahead in ['+']:
            self.Match('+')
            self.Factor()
        elif self.lookahead in ['-']:
            self.Match('-')
            self.Factor()
        elif self.lookahead in ['ID','NUM','(']:
            self.Factor()
        else:
            print('error')

    def Signed_factor_prime(self):
        if self.lookahead in ['(',';',']',')',',','<','==','+','-','*']:
            self.Factor_prime()
        else:
            print('error')

    def Signed_factor_zegond(self):
        if self.lookahead in ['+']:
            self.Match('+')
            self.Factor()
        elif self.lookahead in ['-']:
            self.Match('-')
            self.Factor()
        elif self.lookahead in ['NUM','(']:
            self.Factor_zegond()
        else:
            print('error')

    def Factor(self):
        if self.lookahead in ['(']:
            self.Match('(')
            self.Expression()
            self.Match(')')
        elif self.lookahead in ['ID']:
            self.Match('ID')
            self.Var_call_prime
        elif self.lookahead in ['NUM']:
            self.Match('NUM')
        else:
            print('error')

    def Var_call_prime(self):
        if self.lookahead in ['(']:
            self.Match('(')
            self.Args()
            self.Match(')')
        elif self.lookahead in ['[',';',']',')',',','<','==','+','-','*']:
            self.Var_prime()
        else:
            print('error')

    def Var_Prime(self):
        if self.lookahead in ['[']:
            self.Match('[')
            self.Expression()
            self.Match(']')
        elif self.lookahead in [';',']',')',',','<','==','+','-','*']:
            return
        else:
            print('error')

    def Factor_Prime(self):
        if self.lookahead in ['(']:
            self.Match('(')
            self.Args()
            self.Match(')')
        elif self.lookahead in [';',']',')',',','<','==','+','-','*']:
            return
        else:
            print('error')

    def Factor_zegond(self):
        if self.lookahead in ['(']:
            self.Match('(')
            self.Expression()
            self.Match(')')
        elif self.lookahead in ['NUM']:
            self.Match('NUM')
        else:
            print('error')

    def Args(self):
        if self.lookahead in ['ID','NUM','(','+','-']:
            self.Arg_list()
        elif self.lookahead in [')']:
            return
        else:
            print('error')

    def Arg_list(self):
        if self.lookahead in ['ID','NUM','(','+','-']:
            self.Expression()
            self.Arg_list_prime()

        else:
            print('error')

    def Arg_list_prime(self):
        if self.lookahead in [',']:
            self.Match(',')
            self.Expression()
            self.Arg_list_prime()
        elif self.lookahead in [')']:
            return
        else:
            print('error')


while True:
    parser=Parser()
    parser.Program()




