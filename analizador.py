import re

def analizar_codigo(codigo):
    keywords = {'int', 'if', 'return', 'using', 'namespace'}
    operators = [r'\+\+', r'--', r'==', r'!=', r'<=', r'>=', r'&&', r'\|\|', r'<<', r'>>',
                 r'\+', r'-', r'\*', r'/', r'%', r'=', r'<', r'>']
    delimiters = {r';', r',', r'\(', r'\)', r'\{', r'\}', r'\[', r'\]'}
    token_spec = [
        ('NUMBER', r'\d+'),
        ('ID', r'[A-Za-z_]\w*'),
        ('OP', r'|'.join(sorted(operators, key=lambda x: -len(x)))),
        ('DELIM', r'|'.join(delimiters)),
        ('STRING', r'"[^"]*"'),
        ('PREPROCESSOR', r'#\s*\w+'),
        ('SKIP', r'[ \t]+'),
        ('NEWLINE', r'\n'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    get_token = re.compile(tok_regex).match
    line_num = 1
    pos = line_start = 0
    tokens = []

    mo = get_token(codigo)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', value, line_num))
        elif kind == 'ID':
            if value in keywords:
                tokens.append(('KEYWORD', value, line_num))
            else:
                tokens.append(('IDENTIFIER', value, line_num))
        elif kind == 'OP':
            tokens.append(('OPERATOR', value, line_num))
        elif kind == 'DELIM':
            tokens.append(('DELIMITER', value, line_num))
        elif kind == 'STRING':
            tokens.append(('STRING', value, line_num))
        elif kind == 'PREPROCESSOR':
            tokens.append(('PREPROCESSOR', value.strip(), line_num))
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            tokens.append(('UNKNOWN', value, line_num))
        pos = mo.end()
        mo = get_token(codigo, pos)
    return tokens
