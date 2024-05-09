

class parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.lookeahead = None
        self.type=type
    def Match(self,type):
        if self.lookeahead == type:
            return True
        else:
            return False

    def Program(self):
        if self.lookeahead in ['int','void','ID',';', 'NUM', '(',' {','}', 'break', 'if','for','return','+','-','$']:
            self.Declaration_List()
        else:
            print("error")

    def Declaration_List(self):
        if self.lookeahead in ['int', 'void']:
            self.Declaration()
            self.Declaration_List()
        elif self.lookeahead in ['ID', ';', 'NUM', '(', ' {', '}', 'break', 'if', 'for', 'return', '+','-', '$']:
            return
        else:
            print("error")

    def Declaration(self):
        if self.lookeahead in ['int', 'void']:
            self.Declaration_initial()
            self.Declaration_prime()
        else:
            print("error")


    def Declaration_initial(self):
        if self.lookeahead in ['int', 'void']:
            self.Type_specifier()
            self.Math('ID')
        else:
            print("error")

    def Declaration_prime(self):
        if self.lookeahead in ['(']:
            self.Fun_declaration_prime()
        elif self.lookeahead in [';','[']:
            self.Var_declaration_prime()
        else:
            print("error")
    def Var_declaration_prime(self):
        if self.lookeahead in [';']:
            self.Match(';')
        elif self.lookeahead in ['[']:
            self.Match('[')
            self.Match('NUM')
            self.Match(']')
            self.Match(';')
        else:
            print("error")

    def Fun_declaration_prime(self):
        if self.lookeahead in ['(']:
            self.Match('(')
            self.Params()
            self.Match(')')
            self.Compound_stmt()
        else:
            print("error")

    def Type_specifier(self):
        if self.lookeahead in ['int']:
            self.Match('int')
        elif self.lookeahead in ['void']:
            self.Match('void')
        else:
            print("error")

    def Params(self):
        if self.lookeahead in ['int']:
            self.Match('int')
            self.Match('ID')
            self.Param_prime()
            self.Param_list()
        elif self.lookeahead in ['void']:
            self.Match('void')
        else:
            print("error")

    def Param_list(self):
        if self.lookeahead in [',']:
            self.Match(',')
            self.Param_Param_list()
        elif self.lookeahead in [')']:
            return
        else:
            print("error")

    def Param(self):
        if self.lookeahead in ['int', 'void']:
            self.Declaration_initial_Param_prime()
        else:
            print("error")
    def  Param_prime(self):
        if self.lookeahead in ['[']:
            self.Match('[')
            self.Match(']')
        elif self.lookeahead in [')',',']:
            return
        else:
            print("error")

    def Compound_stmt(self):
        if self.lookeahead in ['{']:
            self.Match('{')
            self.Declaration_list()
            self.Statement_list()
            self.Match('}')
        else:
            print("error")

    def Statement_list(self):
        if self.lookeahead in ['ID',',','(','{','break','if','for','return','+','-']:
            self.Statement()
            self.Statement_list()
        elif self.lookeahead in ['}']:
            return
        else:
            print("error")

    def Statement(self):
        if self.lookeahead in ['ID',';','NUM','(','break','+','-']:
            self. Expression_stmt()
        elif self.lookeahead in ['{']:
            self.Compound_stmt()
        elif self.lookeahead in ['if']:
            self.Selection_stmt()
        elif self.lookeahead in ['for']:
            self. Iteration_stmt()
        elif self.lookeahead in ['return']:
            self. Return_stmt()
        else:
            print("error")

    def Expression_stmt(self):
        if self.lookeahead in ['ID','NUM','(','+','-']:
            self.Expression()
            self.Match(';')
        elif self.lookeahead in ['break']:
            self.Match('break')
            self.Match(';')
        elif self.lookeahead in [';']:
            self.Match(';')
        else:
            print("error")

    def Selection_stmt(self):
        if self.lookeahead in ['if']:
            self.Match('if')
            self.Match('(')
            self.Expression()
            self.Match(')')
            self.Statement()
            self.Else_stmt()
        else:
            print("error")

    def Else_stmt(self):
        if self.lookeahead in ['endif']:
            self.Match('endif')
        elif self.lookeahead in ['else']:
            self.Match('else')
            self.Statement()
            self.Match('endif')
        else:
            print("error")

    def Iteration_stmt(self):
        if self.lookeahead in ['for']:
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
        if  self.lookeahead in ['return']:
            self.Match('return')
            self.Return_stmt_prime()

        else:
            print('error')
    def Return_stmt_prime(self):
        if self.lookeahead in [';']:
            self.Match(';')
        elif self.lookeahead in ['ID','NUM','(','+','-']:
            self.Expression()
            self.Match(';')
        else:
            print('error')

    def Expression(self):
        if self.lookeahead in ['NUM','(','+','-']:
            self.Simple_expression_zegond()
        elif self.lookeahead in ['ID']:
            self.Match('ID')
            self.Match('B')

        else:
            print('error')

    def B(self):
        if self.lookeahead in ['=']:
            self.Match('=')
            self.Expression()
        elif self.lookeahead in ['[']:
            self.Match['[']
            self.Expression()
            self.Match[']']
            self.H()
        elif self.lookeahead in ['(','<','==','+','-','*',';',']',')',',']:
            self.Simple_expression_prime()
        else:
            print('error')

    def H(self):
        if self.lookeahead in ['=']:
            self.Match('=')
            self.Expression()
        elif self.lookeahead in ['*',';',']',')',',','<','==','+','-']:
            self.G()
            self.D()
            self.C()
        else:
            print('error')

    def Simple_expression_zegond(self):
        if self.lookeahead in ['NUM','(','+','-']:
            self.Additive_expression_prime()
            self.C()
        else:
            print('error')
    def Simple_expression_prime(self):
        if self.lookeahead in [';', ']',')',',','<','==']:
            self.Additive_expression_prime()
            self.C()
        else:
            print('error')
    def C(self):
        if self.lookeahead in ['<','==']:
            self.Relop()
            self.Additive_expression()
        elif self.lookeahead in [';',']',')',',']:
            return
        else:
            print('error')

    def Relop(self):
        if self.lookeahead in ['<']:
            self.Match('<')
        elif self.lookeahead in ['==']:
            self.Match('==')
        else:
            print('error')

    def Additive_expression(self):
        if self.lookeahead in ['ID','NUM','(','+','-']:
            self.Term()
            self.D()
        else:
            print('error')

    def Additive_expression_prime(self):
        if self.lookeahead in ['(','*',';',']',')',',','<','==','+','-']:
            self.Term_prime()
            self.D()

        else:
            print('error')

    def Aditive_expression_zegond(self):
        if self.lookeahead in ['NUM','(','+','-']:
            self.Term_zegond()
            self.D()
        else:
            print('error')

    def D(self):
        if self.lookeahead in ['+','-']:
            self.Addop()
            self.Term()
            self.D()
        elif self.lookeahead in [';',']',')',',','<','==']:
            return
        else:
            print('error')

    def Addop(self):
        if self.lookeahead in ['+']:
            self.Match('+')
        elif self.lookeahead in ['-']:
            self.Match('-')
        else:
            print('error')

    def Term(self):
        if self.lookeahead in ['ID','NUM','(','+','-']:
            self.Signed_factor()
            self.G()
        else:
            print('error')

    def Term_prime(self):
        if self.lookeahead in ['(',';',']',')',',','<','==','+','-','*']:
            self.Signed_factor_prime()
            self.G()
        else:
            print('error')

    def Term_zegond(self):
        if self.lookeahead in ['NUM','(','+','-']:
            self.Signed_factor_zegond()
            self.G()
        else:
            print('error')


    def G(self):
      if self.lookeahead in ['*']:
        self.Match('*')
        self.Signed_factor()
        self.G()
      elif self.lookeahead in [';',']',')',',','<','==','+','-']:
        return
      else:
        print('error')

    def Signed_factor(self):
        if self.lookeahead in ['+']:
            self.Match('+')
            self.Factor()
        elif self.lookeahead in ['-']:
            self.Match('-')
            self.Factor()
        elif self.lookeahead in ['ID','NUM','(']:
            self.Factor()
        else:
            print('error')

    def Signed_factor_prime(self):
        if self.lookeahead in ['(',';',']',')',',','<','==','+','-','*']:
            self.Factor_prime()
        else:
            print('error')

    def Signed_factor_zegond(self):
        if self.lookeahead in ['+']:
            self.Match('+')
            self.Factor()
        elif self.lookeahead in ['-']:
            self.Match('-')
            self.Factor()
        elif self.lookeahead in ['NUM','(']:
            self.Factor_zegond()
        else:
            print('error')

    def Factor(self):
        if self.lookeahead in ['(']:
            self.Match('(')
            self.Expression()
            self.Match(')')
        elif self.lookeahead in ['ID']:
            self.Match('ID')
            self.Var_call_prime
        elif self.lookeahead in ['NUM']:
            self.Match('NUM')
        else:
            print('error')

    def Var_call_prime(self):
        if self.lookeahead in ['(']:
            self.Match('(')
            self.Args()
            self.Match(')')
        elif self.lookeahead in ['[',';',']',')',',','<','==','+','-','*']:
            self.Var_prime()
        else:
            print('error')

    def Var_Prime(self):
        if self.lookeahead in ['[']:
            self.Match('[')
            self.Expression()
            self.Match(']')
        elif self.lookeahead in [';',']',')',',','<','==','+','-','*']:
            return
        else:
            print('error')

    def Factor_Prime(self):
        if self.lookeahead in ['(']:
            self.Match('(')
            self.Args()
            self.Match(')')
        elif self.lookeahead in [';',']',')',',','<','==','+','-','*']:
            return
        else:
            print('error')

    def Factor_zegond(self):
        if self.lookeahead in ['(']:
            self.Match('(')
            self.Expression()
            self.Match(')')
        elif self.lookeahead in ['NUM']:
            self.Match('NUM')
        else:
            print('error')

    def Args(self):
        if self.lookeahead in ['ID','NUM','(','+','-']:
            self.Arg_list()
        elif self.lookeahead in [')']:
            return
        else:
            print('error')

    def Arg_list(self):
        if self.lookeahead in ['ID','NUM','(','+','-']:
            self.Expression()
            self.Arg_list_prime()

        else:
            print('error')

    def Arg_list_prime(self):
        if self.lookeahead in [',']:
            self.Match(',')
            self.Expression()
            self.Arg_list_prime()
        elif self.lookeahead in [')']:
            return
        else:
            print('error')







