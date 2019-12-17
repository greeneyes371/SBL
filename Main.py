from SBL_Lexer import SBL_Lexer
from SBL_Parser import SBL_Parser
import sys

print('Welcome to SBL+ : a Server Based Language')
print('SBL+ ver 1.0.0')

lexer = SBL_Lexer()
parser = SBL_Parser()

if len(sys.argv) > 1:
    args = sys.argv
    if args[1][len(args[1])-4:] != '.sbl':
        raise Exception('Script must be in correct format.')

keepRunning = True
while keepRunning:
    try:
        if len(sys.argv) > 1:
            lines = open(sys.argv[1]).lines

            command = 'RUN { '+ args[1] + '}'
            keepRunning = False

        else:
            command = input('SBL+ >> ')
    except EOFError:
        break

    #parse code
    tokens = lexer.tokenize(command)
    result = parser.parse(tokens)