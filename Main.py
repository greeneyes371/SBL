from SBL_Lexer import SBL_Lexer
from SBL_Parser import SBL_Parser
print('Welcome to SBL+ ; a Server Based Language')
print('SBL+ ver 1.0.0')

lexer = SBL_Lexer()
parser = SBL_Parser()

while True:
    try:
        command = input('SBL+ >> ')
    except EOFError:
        break

    #parse code
    tokens = lexer.tokenize(command)
    result = parser.parse(tokens)