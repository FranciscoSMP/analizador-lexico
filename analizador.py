import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Definición de tokens
keywords = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double',
    'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long',
    'register', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
    'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', 'class', 'public', 'private'
}

# Uso de raw strings para evitar warnings
operators = {r'\+', r'-', r'\*', r'/', r'%', r'=', r'==', r'!=', r'<', r'>', r'<=', r'>=', r'&&', r'\|\|', r'\+\+', r'--'}
delimiters = {r';', r',', r'\(', r'\)', r'\{', r'\}', r'\[', r'\]'}

token_specification = [
    ('COMMENT',     r'//.*|/\*[\s\S]*?\*/'),  # Comentarios
    ('STRING',      r'"[^"]*"'),              # Literales de cadena
    ('NUMBER',      r'\d+(\.\d*)?'),          # Números
    ('ID',          r'[A-Za-z_]\w*'),         # Identificadores
    ('OP',          r'|'.join(operators)),    # Operadores
    ('DELIM',       r'|'.join(delimiters)),   # Delimitadores
    ('NEWLINE',     r'\n'),                   # Nueva línea
    ('SKIP',        r'[ \t]+'),               # Espacios y tabuladores
    ('MISMATCH',    r'.'),                    # Cualquier otro carácter
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

def lexer(code):
    pos = 0
    tokens = []
    line = 1
    mo = get_token(code)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE':
            line += 1
        elif kind == 'SKIP' or kind == 'COMMENT':
            pass
        elif kind == 'ID':
            if value in keywords:
                tokens.append(('KEYWORD', value, line))
            else:
                tokens.append(('IDENTIFIER', value, line))
        elif kind == 'NUMBER':
            tokens.append(('NUMBER', value, line))
        elif kind == 'STRING':
            tokens.append(('STRING', value, line))
        elif kind == 'OP':
            tokens.append(('OPERATOR', value, line))
        elif kind == 'DELIM':
            tokens.append(('DELIMITER', value, line))
        elif kind == 'MISMATCH':
            tokens.append(('UNKNOWN', value, line))
        pos = mo.end()
        mo = get_token(code, pos)
    return tokens

def main():
    filename = input("Ingrese la ruta completa o el nombre del archivo C++ a analizar (ejemplo: C:/Users/VIRTUALPC/Desktop/programa.cpp): ")
    try:
        with open(filename, 'r') as file:
            code = file.read()
            tokens = lexer(code)
            print(f"\nTokens encontrados en {filename}:\n")
            print(f"{'Tipo':<12} {'Lexema':<20} {'Línea'}")
            print("-" * 40)
            for token in tokens:
                print(f"{token[0]:<12} {token[1]:<20} {token[2]}")
    except FileNotFoundError:
        print("El archivo especificado no fue encontrado.")

if __name__ == "__main__":
    main()