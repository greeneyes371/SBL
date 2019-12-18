from sly import Lexer

class SBL_Lexer(Lexer):
    #Set of Tokens
    tokens = {'ID', 'NUMBER', 'STRING', 'ASSIGN', 'FUNCTION', 'COMMENT'}

    #Set of tokens to be interpreted as literals
    literals = {'{', '}', ':', '(', ')', ',', '.'}

    #String containing ignored characters
    ignore = ' \t'

    #Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    #Error handling
    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

    #Regular expressions for tokens.
    STRING = r'\"(.*?)"'
    COMMENT = r'%.*'
    NUMBER = r'\d+'
    ASSIGN = r':='

    #Special cases
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        identifiers = {
            'CREATE': 'FUNCTION',
            'LISTEN': 'FUNCTION',
            'RECEIVE': 'FUNCTION',
            'SEND': 'FUNCTION',
            'CLOSE': 'FUNCTION',
            'DESTROY': 'FUNCTION',
            'DELETE': 'FUNCTION',
            'RUN': 'FUNCTION',
            'PRINT': 'FUNCTION',
            'SHOW': 'FUNCTION',
            'EXIT': 'FUNCTION'
        }

        if t.value in identifiers:
            t.type = identifiers.get(t.value)

        else:
            t.type = 'ID'

        return t

lexer = SBL_Lexer()

#data = '''
#    x := \"This is a message.\"
#    PRINT{x}
#    ;
#    PRINT{\"This is another message.\"}
#'''
#for tok in lexer.tokenize(data):
#    print('Type = %r , value = %r ' % (tok.type, tok.value))
