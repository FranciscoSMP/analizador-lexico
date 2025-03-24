import re

def analizar_codigo(codigo):
    palabra_clave = {'int', 'if', 'return', 'using', 'namespace'}
    operadores = [r'\+\+', r'--', r'==', r'!=', r'<=', r'>=', r'&&', r'\|\|', r'<<', r'>>',
                 r'\+', r'-', r'\*', r'/', r'%', r'=', r'<', r'>']
    delimitadores = {r';', r',', r'\(', r'\)', r'\{', r'\}', r'\[', r'\]'}
    tipo_token = [
        ('NUMERO', r'\d+'),
        ('IDENTIFICADOR', r'[A-Za-z_]\w*'),
        ('OPERADOR', r'|'.join(sorted(operadores, key=lambda x: -len(x)))),
        ('DELIMITADOR', r'|'.join(delimitadores)),
        ('CADENA', r'"[^"]*"'),
        ('PREPROCESADOR', r'#\s*\w+'),
        ('OMITIR', r'[ \t]+'),
        ('NUEVA_LINEA', r'\n'),
        ('NO_COINCIDE', r'.'),
    ]
    regex_token = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in tipo_token)
    obtener_token = re.compile(regex_token).match
    num_linea = 1
    posicion = inicio_linea = 0
    tokens = []

    coincidencia = obtener_token(codigo)
    while coincidencia:
        tipo = coincidencia.lastgroup
        valor = coincidencia.group()
        if tipo == 'NUMERO':
            tokens.append(('NUMERO', valor, num_linea))
        elif tipo == 'IDENTIFICADOR':
            if valor in palabra_clave:
                tokens.append(('PLABRA CLAVE', valor, num_linea))
            else:
                tokens.append(('IDENTIFICADOR', valor, num_linea))
        elif tipo == 'OPERADOR':
            tokens.append(('OPERADOR', valor, num_linea))
        elif tipo == 'DELIMITADOR':
            tokens.append(('DELIMITADOR', valor, num_linea))
        elif tipo == 'CADENA':
            tokens.append(('CADENA', valor, num_linea))
        elif tipo == 'PREPROCESADOR':
            tokens.append(('PREPROCESADOR', valor.strip(), num_linea))
        elif tipo == 'NUEVA_LINEA':
            inicio_linea = coincidencia.end()
            num_linea += 1
        elif tipo == 'OMITIR':
            pass
        elif tipo == 'NO_COINCIDE':
            tokens.append(('DESCONOCIDO', valor, num_linea))
        posicion = coincidencia.end()
        coincidencia = obtener_token(codigo, posicion)
    return tokens
