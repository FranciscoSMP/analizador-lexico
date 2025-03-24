import re  # Importa la librería 're' para trabajar con expresiones regulares.

# Función principal para analizar el código de entrada.
def analizar_codigo(codigo):
    # Conjunto de palabras clave a identificar como tokens.
    palabra_clave = {'int', 'if', 'return', 'using', 'namespace'}
    
    # Lista de operadores comunes en lenguajes de programación.
    operadores = [r'\+\+', r'--', r'==', r'!=', r'<=', r'>=', r'&&', r'\|\|', r'<<', r'>>',
                  r'\+', r'-', r'\*', r'/', r'%', r'=', r'<', r'>']
    
    # Conjunto de delimitadores (símbolos que separan declaraciones o expresiones).
    delimitadores = {r';', r',', r'\(', r'\)', r'\{', r'\}', r'\[', r'\]'}
    
    # Definición de tipos de tokens con su correspondiente patrón de búsqueda en regex.
    tipo_token = [
        ('NUMERO', r'\d+'),  # Detecta números enteros.
        ('IDENTIFICADOR', r'[A-Za-z_]\w*'),  # Detecta identificadores (variables, funciones, etc.).
        
        # Detecta operadores. Se ordenan de mayor a menor longitud para evitar conflictos en la detección.
        ('OPERADOR', r'|'.join(sorted(operadores, key=lambda x: -len(x)))),
        
        # Detecta delimitadores.
        ('DELIMITADOR', r'|'.join(delimitadores)),
        
        # Detecta cadenas encerradas entre comillas dobles.
        ('CADENA', r'"[^"]*"'),
        
        # Detecta líneas de preprocesador como '#include'.
        ('PREPROCESADOR', r'#\s*\w+'),
        
        # Detecta espacios y tabulaciones que deben ser ignorados.
        ('OMITIR', r'[ \t]+'),
        
        # Detecta saltos de línea para llevar un control de la línea actual.
        ('NUEVA_LINEA', r'\n'),
        
        # Detecta cualquier cosa que no coincida con lo anterior (errores o caracteres desconocidos).
        ('NO_COINCIDE', r'.'),
    ]
    
    # Genera una expresión regular completa que une todos los patrones anteriores.
    regex_token = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in tipo_token)
    
    # Compila la expresión regular para una búsqueda más rápida.
    obtener_token = re.compile(regex_token).match
    
    # Inicializa variables para el control de posición y línea.
    num_linea = 1
    posicion = inicio_linea = 0
    tokens = []

    # Inicia el proceso de detección de tokens en el código.
    coincidencia = obtener_token(codigo)
    while coincidencia:
        tipo = coincidencia.lastgroup  # Tipo de token detectado.
        valor = coincidencia.group()  # Texto del token detectado.
        
        # Clasificación de tokens según su tipo.
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
            inicio_linea = coincidencia.end()  # Actualiza el inicio de línea.
            num_linea += 1  # Incrementa el número de línea.
        elif tipo == 'OMITIR':
            pass  # Ignora espacios y tabulaciones.
        elif tipo == 'NO_COINCIDE':
            tokens.append(('DESCONOCIDO', valor, num_linea))  # Detecta tokens inválidos.
        
        # Actualiza la posición actual en el código.
        posicion = coincidencia.end()
        
        # Intenta obtener el siguiente token.
        coincidencia = obtener_token(codigo, posicion)
    
    # Devuelve la lista de tokens encontrados.
    return tokens

