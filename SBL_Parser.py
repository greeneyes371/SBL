from sly import Parser
from SBL_Lexer import SBL_Lexer
import Functions as builtin

class SBL_Parser(Parser):
    tokens = SBL_Lexer.tokens

    def __init__(self):
        self.names = {}

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

    @_('COMMENT')
    def statement(self, p):
        pass

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

    @_('ID ASSIGN function')
    def assignment(self, p):
        if p.ID in self.names:
            raise Exception("Variables are immutable.")

        else:
            self.names[p.ID] = p.function

    @_('FUNCTION "{" argumentList "}"')
    def function(self, p):
        try:
            arguments = p.argumentList.split(':')
        except:
            pass

        if p.FUNCTION == 'CREATE':
            if arguments[0] in self.names:
                raise Exception("Server name already exists.")
            else:
                self.names[arguments[0]] = builtin.createServer(arguments[1])

        elif p.FUNCTION == 'LISTEN':
            if arguments[0] not in self.names:
                raise Exception("Server does not exist.")

            elif arguments[1] in self.names:
                raise Exception("Connection name already exists.")

            else:
                self.names[arguments[1]] = builtin.listenForConnection(self.names[arguments[0]])

        elif p.FUNCTION == 'RECEIVE':
            if arguments[0] not in self.names:
                raise Exception("Connection does not exist.")

            else:
                return builtin.receiveMessage(self.names[arguments[0]])

        elif p.FUNCTION == 'SEND':
            if arguments[0] not in self.names:
                raise Exception("Connection does not exist.")

            elif arguments[1] in self.names:
                builtin.sendMessage(self.names[arguments[0]], self.names[arguments[1]])

            else:
                builtin.sendMessage(self.names[arguments[0]], arguments[1])

        elif p.FUNCTION == 'CLOSE':
            if arguments[0] not in self.names:
                raise Exception("Connection does not exist.")

            else:
                builtin.closeConnection(self.names[arguments[0]], arguments[0])
                del self.names[arguments[0]]

        elif p.FUNCTION == 'DESTROY':
            if arguments[0] not in self.names:
                raise Exception("Server does not exist.")

            else:
                builtin.closeServer(self.names[arguments[0]], arguments[0])
                del self.names[arguments[0]]

        elif p.FUNCTION == 'DELETE':
            if arguments[0] not in self.names:
                raise Exception("Variable does not exist.")

            else:
                del self.names[arguments[0]]

        elif p.FUNCTION == 'RUN':
            try:
                file = open(arguments[0])
            except:
                print('File does not exist.')

            for line in file.readlines():
                if line.strip():
                    try:
                        parser.parse(lexer.tokenize(line))

                    except SyntaxError:
                        print('Invalid syntax.')

                    except EOFError:
                        return

        elif p.FUNCTION == 'PRINT':
            if arguments[0] in self.names:
                value = self.names[arguments[0]]
                builtin.display(value[1: len(value) -1])

            elif arguments[0].isdigit():
                builtin.display(arguments[0])

            elif arguments[0].startswith("\""):
                builtin.display(arguments[0][1:len(arguments[0]) - 1])

            else:
                builtin.display("Variable does not exist.")

        elif p.FUNCTION == 'SHOW':
            builtin.show(self.names)

        elif p.FUNCTION == 'EXIT':
            builtin.close()

    @_('argument ":" argumentList')
    def argumentList(self, p):
        return p.argument + ":" + p.argumentList

    @_('argument')
    def argumentList(self, p):
        return p.argument

    @_('ID')
    def argument(self, p):
        return p.ID

    @_('NUMBER')
    def argument(self, p):
        return p.NUMBER

    @_('STRING')
    def argument(self, p):
        return p.STRING

    @_('function')
    def argument(self, p):
        return p.function

    @_('filename')
    def argument(self, p):
        return p.filename

    @_('ID "." ID')
    def filename(self, p):
        if p.ID1 != "sbl":
            raise Exception('File must be in SBL+ format.')
        else:
            return p.ID0 + "." + p.ID1

    @_('empty')
    def argument(self, p):
        return p.empty

    @_('')
    def empty(self, p):
        pass


parser = SBL_Parser()
lexer = SBL_Lexer()

#data = '''
#    RUN { tester.sbl }
#'''
#for line in data.splitlines():
#    result = parser.parse(lexer.tokenize(line))