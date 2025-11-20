from tokens import *
from utils import *

class Lexer:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
    def add_token(self, token_type,text=1):
        if text == 1:
            text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, self.line))
    def peak(self):
        if self.current >= len(self.source):
            return '\0'
        return self.source[self.current]
    def lookahead(self,n=1):
        if self.current + n >= len(self.source):
            return '\0'
        return self.source[self.current + n]
    def match(self, expected):
        # match will check always next character 
        # (due to the self.advance is used in the
        # beginning of tokenize).
        if self.current >= len(self.source):
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    def tokenize(self):
        while self.current < len(self.source):
            # For every token that we find,
            # we set the start pointer to the current pointer.
            # Because every while iteration,
            # we must get a new token from the current pointer.
            self.start = self.current
            # We are getting the current character,
            # after that we are incrementing the current pointer.
            # so while;
            # current = 0, CH = source[0], current = 1.
            ch = self.advance()
            if ch == '\n': 
                self.line += 1
            elif ch == ' ': pass
            elif ch == '\r': pass
            elif ch == '\t': pass
            elif ch == '-':
                # TODO: ismail generate comment handle
                # and multi-line comment handle /* ... */
                if self.match('-'):
                    while self.peak() != '\n' and self.current < len(self.source):
                        self.advance()
                else:
                    self.add_token(TOK_MINUS)
            elif ch == '(':self.add_token(TOK_LPAREN)
            elif ch == ')':self.add_token(TOK_RPAREN)
            elif ch == '{':self.add_token(TOK_LCURLY)
            elif ch == '}':self.add_token(TOK_RCURLY)
            elif ch == '[':self.add_token(TOK_LSQUAR)
            elif ch == ']':self.add_token(TOK_RSQUAR)
            elif ch == ',':self.add_token(TOK_COMMA)
            elif ch == '.':self.add_token(TOK_DOT)
            elif ch == '+':self.add_token(TOK_PLUS)
            elif ch == '*':self.add_token(TOK_STAR)
            elif ch == '^':self.add_token(TOK_CARET)
            elif ch == '/':self.add_token(TOK_SLASH)
            elif ch == ';':self.add_token(TOK_SEMICOLON)
            elif ch == '?':self.add_token(TOK_QUESTION)
            elif ch == '%':self.add_token(TOK_MOD)
            elif ch == '=':
                if self.match('='):
                    self.add_token(TOK_EQ)
                else:
                    self.add_token(TOK_ASSIGN)
            elif ch == '!':
                if self.match('='):
                    self.add_token(TOK_NE)
                else:
                    self.add_token(TOK_NOT)
            elif ch == '>':
                if self.match('='):
                    self.add_token(TOK_GE)
                else:
                    self.add_token(TOK_GT)
            elif ch == '<':
                if self.match('='):
                    self.add_token(TOK_LE)
                else:
                    self.add_token(TOK_LT)
            elif ch == ':':
                if self.match('='):
                    self.add_token(TOK_ASSIGN)
                else:
                    self.add_token(TOK_COLON)
            elif ch.isdigit():
                self.handle_number()
            elif ch == '"':
                self.handle_string()
            elif ch == "'":
                self.handle_string(stringStarter="'")
            elif ch == "_" or ch.isalpha():
                self.handle_identifier()
            else:
                lexer_error(f"Unexpected character: {ch}", self.line)
        return self.tokens
    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char
    def handle_number(self):
        while self.peak().isdigit():
            self.advance()
        if self.peak() == '.' and self.lookahead().isdigit():
            self.advance()
            while self.peak().isdigit():
                self.advance()
            self.add_token(TOK_FLOAT)
        else:
            self.add_token(TOK_INTEGER)
    def handle_string(self, stringStarter='"', multiLine=True):
        # TODO: If multiLine is false, we should raise an error 
        # If we are not able to see the ending stringStarter before a new \n.
        while self.peak() != stringStarter and self.current < len(self.source):
            if self.peak() == '\n':
                self.line += 1
            self.advance()
        # If we reached the end of the source without
        # finding a other stringStarter, it's an unterminated string.
        if self.current >= len(self.source):
            lexer_error(f"unterminated string", self.line)
            return
        self.advance() 
        self.add_token(TOK_STRING)
    def handle_identifier(self):
        while self.peak() == "_" or self.peak().isalnum():
            self.advance()
        text = self.source[self.start:self.current]
        if text in keywords:
            self.add_token(keywords[text])
            return
        self.add_token(TOK_IDENTIFIER)

    

