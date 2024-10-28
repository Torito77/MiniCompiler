#Yet Another Attemp Of a Compiler
import ply.yacc as yacc
from LexA2 import tokens, tablaSimbolos, lexer, ListaLineas  # Import tokens, symbol table, and lexer

# Precedencia
precedence = (
    ('right', 'ASIG'),         # Right-associative assignment operator
    ('left', 'SUMA', 'RESTA'), # Left-associative addition and subtraction
    ('left', 'MULT', 'DIV'),   # Left-associative multiplication and division
    ('right', 'UMINUS'),       # Right-associative unary minus
)

# Reglas de parseo
def p_statement_expr(p):
    '''statement : expression'''
    print("Expression result:", p[1])

def p_statement_assign(p):
    '''statement : ID ASIG expression
                 | INT ID ASIG expression'''
    if len(p) == 4:
        tablaSimbolos[p[1]] = p[3]  # Actualizar la tabla de simbolos
        print(f"Assignment: {p[1]} = {p[3]}")
    else:
        tablaSimbolos[p[2]] = p[4]  # Actualizar la tabla de simbolos
        print(f"Assignment: {p[2]} = {p[4]}")

def p_expression_binop(p):
    '''expression : expression SUMA expression
                  | expression RESTA expression
                  | expression MULT expression
                  | expression DIV expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_uminus(p):
    '''expression : RESTA expression %prec UMINUS'''
    p[0] = -p[2]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_integer(p):
    '''expression : INTEGER'''
    p[0] = p[1]

def p_expression_id(p):
    '''expression : ID'''
    # Retrieve the value of the identifier from the symbol table
    if p[1] in tablaSimbolos:
        p[0] = tablaSimbolos[p[1]]
    else:
        print(f"Error: Identifier '{p[1]}' not found")
        p[0] = 0

def p_error(p):
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOL")

# Construye el parser
parser = yacc.yacc()

# Test the parser
def parse_input(input_text):
    lexer.input(input_text)
    result = parser.parse(input_text)
    return result




# ProbaInador
if __name__ == "__main__":
    ubicacion = 'C:/Users/elzuk/Desktop/pitón/AnalizadorLexico/codigo.dep'
    archivo = open(ubicacion,'r')
    c = 0
    for linea in archivo:
        if 'ASIG' in ListaLineas[c] and linea != "\n" :
            parse_input(linea)
        if linea != "\n":
            c+=1

    """
    while True:
        try:
            
            #s = input('Enter statement > ')
        except EOFError:
            break
        
        if not s:
            continue
        parse_input(s)
    """

"""
for x in ListaLineas
    ListaLineas[X]
"""

    