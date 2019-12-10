from sly import Parser
from SBL_Lexer import SBL_Lexer
import Functions as builtin
import operator

class SBL_Parser(Parser):
    tokens = SBL_Lexer.tokens

    def __init__(self):
        self.names = {}
        self.functions = {
            'PRINT': builtin.PRINT,
            'SHOWVARS': builtin.SHOWVARS,
            'EXIT': builtin.EXIT,
            'createServer': builtin.createServer,
            'listen': builtin.listenForConnection
        }

    #Grammar rules
    @_('statementList')
    def declaration(self, p):
        return p.statementList

    @_('function "," statementList')
    def statementList(self, p):
        return p.function, p.statementList

    @_('assignment "," statementList')
    def statementList(self, p):
        return p.assignment, p.statementList

    @_('statement')
    def statementList(self, p):
        return p.statement

    @_('function')
    def statement(self, p):
        return p.function

    @_('assignment')
    def statement(self, p):
        return p.assignment

    @_('ID ASSIGN STRING')
    def assignment(self, p):
        if p.ID in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            self.names[p.ID] = p.STRING

    @_('ID ASSIGN NUMBER')
    def assignment(self, p):
        if p.ID in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            self.names[p.ID] = p.NUMBER

    @_('ID ASSIGN ID')
    def assignment(self, p):
        if p.ID0 in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            if p.ID1 not in self.names.keys():
                raise Exception("Variable " + p.ID1 + " does not exist.")
            else:
                self.names[p.ID0] = self.names[p.ID1]

    @_('ID ASSIGN expr')
    def assignment(self, p):
        if p.ID in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            self.names[p.ID] = p.expr

    @_('expr OPERATOR expr')
    def expr(self, p):
        operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

        return operators[p.OPERATOR](p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('FUNCTION "{" argumentList "}"')
    def function(self, p):
        if p.FUNCTION == 'SHOWVARS':
            self.functions[p.FUNCTION](self.names)

        else:
            self.functions[p.FUNCTION](p.argumentList)

    @_('argument ":" argumentList')
    def argumentList(self, p):
        return p.argument, p.argumentList

    @_('argument')
    def argumentList(self, p):
        return p.argument

    @_('ID')
    def argument(self, p):
        return self.names[p.ID]

    @_('expr')
    def argument(self, p):
        return p.expr

    @_('STRING')
    def argument(self, p):
        return p.STRING

    @_('empty')
    def argument(self, p):
        return p.empty

    @_('')
    def empty(self, p):
        pass

parser = SBL_Parser()
lexer = SBL_Lexer()

data = '''
    x := \"This is a message.\"
    y := \"This is another message.\"
    PRINT{x} 
    PRINT{22} 
    z := (34 + 23)
    PRINT{z}
    EXIT{}
'''
for line in data.splitlines():
    result = parser.parse(lexer.tokenize(line))