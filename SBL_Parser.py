from sly import Parser
from SBL_Lexer import SBL_Lexer
import Functions as builtin

class SBL_Parser(Parser):
    tokens = SBL_Lexer.tokens
    names = {}

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
    @_('functionList')
    def statement(self, p):
        return p.functionList

    @_('function "," functionList')
    def functionList(self, p):
        p.function, p.functionList

    @_('function')
    def functionList(self, p):
        p.function

    @_('assignment')
    def statement(self, p):
        return p.assignment

    @_('ID ASSIGN STRING')
    def assignment(self, p):
        if p.ID in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            self.names[p.ID] = p.STRING

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

    @_('NUMBER OPERATOR NUMBER')
    def expr(self, p):
        return ('+', p.NUMBER0, p.NUMBER1)

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

    @_('NUMBER')
    def argument(self, p):
        return p.NUMBER

    @_('STRING')
    def argument(self, p):
        return p.STRING

    @_('empty')
    def argument(self, p):
        return p.empty

    @_('')
    def empty(self, p):
        pass

#parser = SBL_Parser()
#lexer = SBL_Lexer()

#data = '''
#    x := \"This is a message.\"
#    y := \"This is another message.\"
#    PRINT{x}
#    PRINT{y}
#    z := 34 + 43
#'''
#for line in data.splitlines():
#    result = parser.parse(lexer.tokenize(line))