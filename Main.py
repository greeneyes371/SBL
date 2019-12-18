from SBL_Lexer import SBL_Lexer
from SBL_Parser import SBL_Parser
import sys

lexer = SBL_Lexer()
parser = SBL_Parser()

if len(sys.argv) > 1:
    args = sys.argv
    if args[1][len(args[1])-4:] != '.sbl':
        raise Exception('Script must be in correct format.')
else:
    print('Welcome to SBL+ : a Server Based Language')
    print('SBL+ ver 1.0.0')

keepRunning = True
while keepRunning:
    if len(sys.argv) > 1:
        file = sys.argv[1]
        command = 'RUN { '+file +' }'
        keepRunning = False

    else:
        command = input('SBL+ >> ')

    try:
    #parse code
        tokens = lexer.tokenize(command)
        result = parser.parse(tokens)

    except EOFError:
        break