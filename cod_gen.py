from enum import Enum
from dataclasses import dataclass
class ScopeType(Enum):
    PARAM = 1
    LOCAL = 2
    FUNC = 3
    GLOBAL = 4


class VarType(Enum):
    INT = 1
    VOID = 2
    ARR = 3


@dataclass
class Token:
    lexeme: str = ''
    type: str = ''
    context: str = ''
    line_num: int = 0


@dataclass
class Row:
    lexeme: str
    addr: str
    scope: int
    param_len: int
    rv_address: str
    scope_type: ScopeType
    var_type: VarType


class SymbolTable:

    def __init__(self):
        self.rows = []

    def add_row(self, lexeme=None, addr=None, scope=None, param_len=None, rv_address=None, scope_type=None, var_type=None ):
        for row in self.rows:
            if lexeme == row.lexeme:
                return
        row = Row(lexeme=lexeme, addr=addr, scope=scope, param_len=param_len, rv_address=rv_address,
                  scope_type=scope_type, var_type=var_type)
        self.rows.append(row)

class CodeGen:
    def __init__(self, symbol_table):
        self.current_inst = 0
        self.pb = {}
        self.ss = []
        self.bs = []
        self.rs = []
        self.symbol_table = symbol_table
        self.current_scope = 0
        self.current_function = None
        self.HP = 100
        self.SP_START = 544
        self.SP = "500"
        self.BP = "504"
        self.AX = "508"
        self.BX = "512"
        self.CX = "516"
        self.DX = "520"
        self.EX = "524"
        self.FX = "528"
        self.RET = "532"
        self.TMP = "536"
        self.POP_RES = "540"
        self.func_param_cnt = 0
        self.global_var_cnt = 0
        self.local_var_cnt = 0
        self.ops = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}
        self.init_stack()
        self.semantic_errors = {}
        self.errors = open("semantic_errors.txt", "w")
        self.current_token_type = ""
        self.var_type = {}
        self.function_param_type = []


    def get_temp(self):
        self.HP += 4
        return str(self.HP)

    def get_address(self, token, line_num):
        if token == "output":  # handle output
            return token
        for row in self.symbol_table.rows[::-1]:
            if row.lexeme == token:
                return row.addr
        for i in self.symbol_table.rows:
            if i.lexeme != token:
                self.semantic_errors[line_num] = (f"#{line_num} : Semantic Error! '{token}' is not defined.\n")

    def push_inst(self, x):
        self.add_inst("ASSIGN", x, f"@{self.SP}")
        self.add_inst("ADD", "#4", self.SP, self.SP)

    def pop_inst(self, x):
        self.add_inst("SUB", self.SP, "#4", self.SP)
        self.add_inst("ASSIGN", f"@{self.SP}", self.POP_RES)
        self.add_inst("ASSIGN", self.POP_RES, x)

    def init_stack(self):
        self.add_inst("ASSIGN", "#544", self.SP)
        self.add_inst("ASSIGN", "#544", self.BP)

    def add_inst(self, op, arg1, arg2='', arg3=''):
        self.pb[self.current_inst] = "({},{},{},{})".format(op, arg1, arg2, arg3)
        self.current_inst += 1

    def we_are_in_main(self):
        for row in self.symbol_table.rows[::-1]:
            if row.scope_type == ScopeType.FUNC:
                if row.lexeme == 'main':
                    return True
                break
        return False

    def mov_value_to_reg(self, x, reg):
        if str(x).startswith("offset#"):
            self.move_value_ebp_offset_to_reg(x[6:], reg)
        elif str(x).startswith("address#"):
            self.mov_value_with_address_to_reg(x[8:], reg)
        elif str(x).startswith("direct#"):
            self.add_inst("ASSIGN", x[7:], reg)
        else:
            self.add_inst("ASSIGN", x, reg)

    def mov_address_to_reg(self, x, reg):
        if str(x).startswith("offset#"):
            self.move_address_ebp_offset_to_reg(x[6:], reg)
        elif str(x).startswith("address#"):
            self.add_inst("ASSIGN", x[8:], reg)
        elif str(x).startswith("direct#"):
            self.add_inst("ASSIGN", "#" + x[7:], reg)
        else:
            self.add_inst("ASSIGN", x, reg)

    def move_value_ebp_offset_to_reg(self, offset, reg):
        self.add_inst("ASSIGN", self.BP, self.TMP)
        self.add_inst("ADD", offset, self.TMP, self.TMP)
        self.add_inst("ASSIGN", "@" + self.TMP, reg)

    def move_address_ebp_offset_to_reg(self, offset, reg):
        self.add_inst("ASSIGN", self.BP, self.TMP)
        self.add_inst("ADD", offset, self.TMP, self.TMP)
        self.add_inst("ASSIGN", self.TMP, reg)

    def mov_value_with_address_to_reg(self, reg_addr, reg):
        self.add_inst("ASSIGN", "@" + reg_addr, reg)

    def push_id(self, token, line_num):
        self.ss.append(token)

    def define_var(self, token, line_num):
        var_id = self.ss.pop()
        self.var_type[var_id] = self.current_token_type
        if self.current_token_type == "void":
            self.semantic_errors[line_num] = (
                f"#{line_num - 1} : Semantic Error! Illegal type of void for '{var_id}'.\n")
        if self.current_scope == 0:
            self.symbol_table.add_row(var_id, f"direct#{self.SP_START + self.global_var_cnt * 4}", self.current_scope,
                                      0, None, ScopeType.LOCAL)
            self.global_var_cnt += 1
        else:
            self.symbol_table.add_row(var_id, f"offset#{self.local_var_cnt * 4}", self.current_scope, 0, None,
                                      ScopeType.LOCAL)
            # print(f"defining new var: {var_id} with offset: {self.local_var_cnt * 4}")
            self.local_var_cnt += 1

        self.push_inst("#0")  # push 0 to stack

    def define_arr(self, token, line_num):
        arr_size = int(self.ss.pop()[1:])
        arr_id = self.ss.pop()
        self.var_type[arr_id] = "array"
        if self.current_token_type == "void":
            self.semantic_errors[line_num] = (f"#{line_num} : Semantic Error! Illegal type of void for '{arr_id}'.\n")
        if self.current_scope == 0:
            self.symbol_table.add_row(arr_id, f"direct#{self.SP_START + self.global_var_cnt * 4}", self.current_scope,
                                      arr_size, None, ScopeType.LOCAL)
            self.global_var_cnt += arr_size + 1
        else:
            self.symbol_table.add_row(arr_id, f"offset#{self.local_var_cnt * 4}", self.current_scope, arr_size, None,
                                      ScopeType.LOCAL)
            self.local_var_cnt += arr_size + 1

        # each array has a pointer that points to the first element of the array
        self.add_inst("ASSIGN", self.SP, self.AX)  # backing up SP
        self.push_inst("#0")  # push 0 to stack
        self.add_inst("ASSIGN", self.SP, f"@{self.AX}", )
        # print(f"defining new array: {self.symbol_table.rows[-1]}")
        for _ in range(arr_size):
            self.push_inst("#0")

    def arr_index(self, token, line_num):
        ind = self.ss.pop()
        arr_addr = self.ss.pop()
        tmp = self.get_temp()
        self.mov_value_to_reg(arr_addr, self.AX)
        self.mov_value_to_reg(ind, self.EX)
        self.add_inst("MULT", self.EX, "#4", self.BX)
        self.add_inst("ADD", self.AX, self.BX, tmp)
        self.ss.append(f"address#{tmp}")

    def get_function_call(self):
        for c in self.ss[::-1]:
            if c == "output":
                return c
            elif not str(c).startswith("direct#"):
                continue
            for row in self.symbol_table.rows[::-1]:
                if row.addr == c and row.scope_type == ScopeType.FUNC:
                    return row

    def get_function_addr(self):
        for c in self.ss[::-1]:
            if c == "output":
                return c
            elif not str(c).startswith("direct#"):
                continue
            for row in self.symbol_table.rows[::-1]:
                if row.addr == c and row.scope_type == ScopeType.FUNC:
                    return row.addr

    def get_function_param(self):
        for c in self.ss[::-1]:
            if c == "output":
                return c
            elif not str(c).startswith("direct#"):
                continue
            for row in self.symbol_table.rows[::-1]:
                if row.addr == c and row.scope_type == ScopeType.FUNC:
                    return row.param_len

    def before_func_params(self, token, line_num):
        # Here I swap the order of function name and a place in pb to jump over non-main function
        func_name = self.ss.pop()
        # print(f"before function params. function: {func_name}")
        self.ss.append(self.current_inst)
        self.current_inst += 1
        self.ss.append(func_name)
        self.func_param_cnt = 0  # reset func_param_cnt
        self.local_var_cnt = 0  # reset local_param_cnt

    def increase_param_cnt(self, token, line_num):
        self.func_param_cnt += 1

    def param_type_arr(self, token, line_num):
        self.ss.append(VarType.ARR)

    def param_type_void(self, token, line_num):
        self.ss.append(VarType.VOID)

    def param_type_int(self, token, line_num):
        self.ss.append(VarType.INT)

    def define_param_vars(self, token, line_num):
        offset_with_ebp = -8  # -4 is for saved ebp
        number = self.func_param_cnt
        for i in range(number):
            param = self.ss[-1 * (i + 1) * 2]
            t = self.ss[-1 * (i + 1) * 2 + 1]
            self.symbol_table.add_row(param, f"offset#{offset_with_ebp}", self.current_scope + 1, 0, None,
                                      ScopeType.PARAM, t)
            offset_with_ebp -= 4

        for s in self.symbol_table.rows:
            if s.scope_type == ScopeType.PARAM:
                self.function_param_type.append(s.var_type)

        for _ in range((self.func_param_cnt) * 2):
            a = (self.ss.pop())


    def create_function(self, token, line_num):

        if self.ss[-2] == "main":
            self.ss.pop()
        func_name = self.ss[-1]

        print(func_name)
        # print(f"creating function: {func_name}")
        self.symbol_table.add_row(func_name, f"direct#{self.current_inst}", self.current_scope, self.func_param_cnt,
                                  self.get_temp(), ScopeType.FUNC)
        self.current_function = self.symbol_table.rows[-1]
        """
        push ebp
        mov ebp, esp
        """
        self.push_inst(self.BP)
        self.add_inst("ASSIGN", self.SP, self.BP)

    def return_function(self, token, line_num):
        # print(f"returning from function: {self.current_function.lexeme}")
        """
        mov esp, ebp
        pop ebp
        """
        self.pop_inst(self.current_function.rv_address)
        self.add_inst("ASSIGN", self.BP, self.SP)
        self.pop_inst(self.BP)
        # flushing passed arguments + local variables
        self.add_inst("SUB", self.SP, f"#{(self.current_function.param_len) * 4}", self.SP)
        # ret
        in_main = self.we_are_in_main()
        if in_main:
            self.pb[self.ss[-2]] = f'(ASSIGN, #0, {self.TMP},)'  # dummy instruction just for main
        else:
            self.pop_inst(self.AX)  # put return address in AX
            self.push_inst(self.current_function.rv_address)  # push return value to stack
            self.add_inst("JP", "@" + self.AX)  # jump to return address
            # print(f"back patching: {self.ss[-2]} with address: {self.current_inst}")
            self.pb[self.ss[-2]] = f'(JP, {self.current_inst}, , )'  # back patching
        self.ss.pop()  # pop function name
        self.ss.pop()  # pop pushed address

    def ss_pop(self, token, line_num):
        self.ss.pop()

    def push_scope(self, token, line_num):
        self.current_scope += 1

    def pop_scope(self, token, line_num):
        for row in self.symbol_table.rows[::-1]:
            if row.scope == self.current_scope:
                self.symbol_table.rows.remove(row)
        self.current_scope -= 1

    def push_local_id_addr(self, token, line_num):
        if token == "output":
            self.ss.append(token)
        else:
            self.ss.append(self.get_address(token, line_num))

    def push_num(self, token, line_num):
        self.ss.append(f"#{token}")

    def get_var_type(self, token, lin_num):
        self.current_token_type = token

    def assign(self, token, line_num):
        self.mov_address_to_reg(self.ss[-2], self.BX)
        self.mov_value_to_reg(self.ss[-1], self.AX)
        self.check_type_mismatch(self.ss[-2], self.ss[-1], line_num)
        self.add_inst("ASSIGN", self.AX, f"@{self.BX}")
        self.ss.pop()

    def output(self, token, line_num):
        if self.ss[-2] == 'output':
            self.mov_value_to_reg(self.ss.pop(), self.AX)
            self.add_inst("PRINT", self.AX)

    def function_call(self, token, line_num):
        function_call = self.get_function_call()
        addr = self.get_function_addr()
        param_len = self.get_function_param()
        arguments = []
        arguments_lexeme = []
        arguments_type = []

        for i in self.ss[::-1]:
            if i == addr:
                break
            else:
                arguments.append(i)

        if function_call == "output":
            return
        for s in self.symbol_table.rows:
            for arg in arguments:
                if arg == s.addr:
                    arguments_lexeme.append(s.lexeme)
        for arg in arguments_lexeme:
            if arg in self.var_type.keys():
                arguments_type.append(self.var_type[arg])

        if len(arguments) != param_len:
            self.semantic_errors[line_num] = (
                f"#{line_num} : Semantic Error! Mismatch in numbers of arguments of '{function_call.lexeme}'.\n")
            num = abs(param_len - len(arguments))
            if len(arguments) > param_len:
                for _ in range(num):
                    self.ss.pop()
            else:
                for _ in range(num):
                    self.ss.append("")
        else:
            i = 0
            self.function_param_type.reverse()
            for i in range(len(arguments_type)):
                if self.function_param_type[i] == VarType.INT and arguments_type[i] != "int":
                    self.semantic_errors[line_num] = (
                        f"#{line_num} : Semantic Error! Mismatch in type of argument {i + 1} of 'abs'. Expected "
                        f"'int' but got '{arguments_type[i]}' instead.\n")
                elif self.function_param_type[i] == VarType.ARR and arguments_type[i] != "array":
                    self.semantic_errors[line_num] = (
                        f"#{line_num} : Semantic Error! Mismatch in type of argument {i + 1} of 'abs'. Expected "
                        f"'arr' but got '{arguments_type[i]}' instead.\n")
                elif self.function_param_type[i] == VarType.VOID and arguments_type[i] != "void":
                    self.semantic_errors[line_num] = (
                        f"#{line_num} : Semantic Error! Mismatch in type of argument {i + 1} of 'abs'. Expected "
                        f"'void' but got '{arguments_type[i]}' instead.\n")
            i += 1
        # push return address to stack.
        self.add_inst("ASSIGN", self.SP, self.DX)  # save return address place
        self.push_inst("#0")  # push 0 to stack. it will be replaced with return address
        if function_call.param_len > 0:
            for param in self.ss[-function_call.param_len:]:
                # print(f"pushing param: {param}, ss: {self.ss}")
                self.mov_value_to_reg(param, self.AX)
                self.push_inst(self.AX)
        self.ss = self.ss[:-function_call.param_len - 1]  # pop pushed arguments from scope stack and function address
        self.add_inst("ASSIGN", "#" + str(self.current_inst + 2), "@" + self.DX)
        self.add_inst("JP", str(function_call.addr[7:]))
        tmp = self.get_temp()
        self.pop_inst(tmp)
        self.ss.append(tmp)

    def push_current_inst(self, token, line_num):
        self.push_inst("#0")
        self.ss.append(f"#{self.current_inst}")

    def save_return_value(self, token, line_num):
        tmp = self.get_temp()
        self.mov_value_to_reg(self.ss.pop(), tmp)
        self.rs.append((self.current_inst, tmp))
        self.current_inst += 3

    def end_return(self, token, line_num):
        recent_return = len(self.rs) - self.rs[::-1].index("RETURN") - 1
        for ret in self.rs[recent_return + 1:]:
            self.pb[ret[0]] = f"(ASSIGN, {ret[1]}, @{self.SP}, )"
            self.pb[ret[0] + 1] = f"(ADD, #4, {self.SP}, {self.SP})"
            self.pb[ret[0] + 2] = f"(JP, {self.current_inst}, , )"
        self.rs = self.rs[:recent_return]

    def make_return(self, token, line_num):
        self.rs.append("RETURN")

    def push_op(self, token, line_num):
        self.ss.append(token)

    def op_action(self, token, line_num):
        op2 = self.ss.pop()
        op = self.ss.pop()
        op1 = self.ss.pop()
        self.check_type_mismatch(op1, op2, line_num)
        tmp = self.get_temp()
        self.mov_value_to_reg(op1, self.AX)
        self.mov_value_to_reg(op2, self.BX)
        self.add_inst(self.ops[op], self.AX, self.BX, tmp)
        self.ss.append(tmp)

    def mult(self, token, line_num):
        op1 = self.ss.pop()
        op2 = self.ss.pop()
        tmp = self.get_temp()
        self.mov_value_to_reg(op1, self.AX)
        self.mov_value_to_reg(op2, self.BX)
        self.add_inst("MULT", self.AX, self.BX, tmp)
        self.ss.append(tmp)

    def save(self, token, line_num):
        self.ss.append(self.current_inst)
        self.current_inst += 1


    def jpf(self,token,line_num):
        dest = self.ss.pop()
        src = self.ss.pop()
        self.pb[dest] = f"(JPF, {src}, {self.current_inst }, )"


    def jpf_save(self, token, line_num):
        dst = self.ss.pop()
        src = self.ss.pop()
        if src.startswith("address"):
            src = "@" + src[8:]
        self.pb[dst] = f"(JPF, {src}, {self.current_inst + 1}, )"
        self.save(token, line_num)

    def jump(self, token, line_num):
        dst = int(self.ss.pop())
        self.pb[dst] = f"(JP, {self.current_inst}, , )"

    def negate(self, token, line_num):
        op = self.ss.pop()
        tmp = self.get_temp()
        self.mov_value_to_reg(op, self.AX)
        self.add_inst("SUB", "#0", self.AX, tmp)
        self.ss.append(tmp)

    def label(self, token, line_num):
        self.ss.append(self.current_inst)





    def save(self, token, line_num):
        self.ss.append(self.current_inst)
        self.current_inst += 1

    def whilee(self, token, line_num):
        self.pb[int(self.ss[-1])] = f"(JPF, {self.ss[-2]}, {self.current_inst + 1}, )"
        self.add_inst("JP", self.ss[-3])
        self.ss.pop()
        self.ss.pop()
        self.ss.pop()

    def break_loop(self, token, line_num):
        if not self.bs:
            self.semantic_errors[line_num - 1] = (f"#{line_num - 1} : Semantic Error! No 'while' found for 'break'.\n")
        self.bs.append(self.current_inst)
        self.current_inst += 1

    def create_break(self, token, line_num):
        self.bs.append("BREAK")

    def fill_break(self, token, line_num):
        recent_break = len(self.bs) - self.bs[::-1].index("BREAK") - 1
        for brk in self.bs[recent_break + 1:]:
            self.pb[brk] = f"(JP, {self.current_inst}, , )"
        self.bs = self.bs[:recent_break]

    def write_semantic_errors(self):
        for m in self.semantic_errors.values():
            self.errors.write(m)

    def check_type_mismatch(self, op1, op2, line_num):
        op1_t = ""
        op2_t = ""

        for i in self.symbol_table.rows:
            if i.addr == op1 and i.lexeme in self.var_type.keys():
                op1_t = self.var_type[i.lexeme]

        for i in self.symbol_table.rows:
            if i.lexeme in self.var_type.keys() and i.addr == op2:
                op2_t = self.var_type[i.lexeme]

        if op2_t == "array" and op1_t == "int":
            self.semantic_errors[line_num] = (
                f"#{line_num} : Semantic Error! Type mismatch in operands, Got int instead of array.\n")