from sly import Lexer

class SBL_Lexer(Lexer):
    #Set of Tokens
    tokens = {'ID', 'NUMBER', 'STRING', 'ASSIGN',
              'OPERATOR', 'FUNCTION'}

    #Set of tokens to be interpreted as literals
    literals = {'{', '}', ':', '(', ')', '\.', ','}

    #String containing ignored characters
    ignore = ' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'%.*'

    #Regular expressions for tokens.
    OPERATOR = "\+" or "-" or "\*" or "/"
    STRING = r'\"(.*?)"'
    ASSIGN = r':='

    #Special cases
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        identifiers = {
            'createServer': 'FUNCTION',
            'sendMessage': 'FUNCTION',
            'receiveMessage': 'FUNCTION',
            'closeServer': 'FUNCTION',
            'getHostName': 'FUNCTION',
            'PRINT': 'FUNCTION',
            'SHOWVARS': 'FUNCTION',
            'EXIT': 'FUNCTION'
        }

        if t.value in identifiers:
            t.type = identifiers.get(t.value)

        else:
            t.type = 'ID'

        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

#lexer = SBL_Lexer()
#data = '''
#    x := \"This is a message.\"
#    PRINT{x}
#    PRINT{\"This is another message.\"}
#'''
#for tok in lexer.tokenize(data):
#    print('Type = %r , value = %r ' % (tok.type, tok.value))