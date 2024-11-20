#Importamos la libreria
import ply.lex as lex 
import re

# Lista de tokens
tokens = [
                                                    # OPERADORES #
'SUMA' ,        # +
'RESTA' ,       # -
'MULT',         # *
'DIV',          # /

'ASIG',         # =
'COMA',         # ,
'PC',           # ;

                                                    # COMPARACIONES #
'NOT',          # ~
'MENOR',        # <
'MAYOR',        # >
'MENORIGUAL',   # <=
'MAYORIGUAL',   # >=
'IGUAL',        # ==
'NIGUAL',       # !=
'AND',          # &
'OR' ,          # |                                                

                                                    # BRACKETS #
'LPAREN',       # (
'RPAREN',       # )

'COMMENT',  # Comentarios de linea  -> #

                                                    # TIPOS DE DATOS #
'INTEGER',      # int
'ERROR'
]

# Expresiones regulares para tokens simples
t_SUMA    = r'\+'
t_RESTA   = r'-'
t_MULT   = r'\*'
t_DIV  = r'/'

t_COMA = r'\,'
t_ASIG = r'\='
t_PC = r'\;'

t_NOT = r'\~'
t_MAYOR = r'\>'
t_MENOR = r'\<'
t_MENORIGUAL = r'\<\='
t_MAYORIGUAL = r'\>\='
t_IGUAL = r'\=\='
t_NIGUAL = r'\!\='
t_AND = r'\&'
t_OR = r'\|'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'

t_COMMENT = r'\#.*'            
t_ignore  = ' \t' #ignora espacios y tabs

# Regla para numeros enteros
def t_INTEGER(t):
    r'\d+[a-zA-Z_][a-zA-Z_0-9]*|\d+'
    if t.value.isdigit():
        t.value = int(t.value)
        return t
    else:
        print(f"Identificador inválido: '{t.value}'")
        #t.lexer.skip(len(t.value))  # Skip the invalid token

# Nueva linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print("Error en la linea " + str(t.lexer.lineno) + ", Token inválido '%s'"  % t.value[0])
    t.lexer.skip(1)

# Palabras reservadas
reserved = {
    'pf2024':'PROG',
    'begin':'BEGIN',
    'decl':'DECL',
    'end':'END',
    'if' : 'IF',
    'else' : 'ELSE',
    'cad' : 'STRING',
    'boolean':'BOOLEAN',
    'int':'INT'
    }

tokens.append('ID')
tokens = tokens + list(reserved.values())


# Definicion de los identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Busca palabras reservadas

    # t.value = (t.value, symbol_lookup(t.value)) # Guarda en la tabla de simbolos si es que es declaracion
    
    return t



# Construccion de la tabla de simbolos 
tablaSimbolos = {}
simbolos = ['+','-','*','/','=',',',';','~','<','>','<=','>=','==','!=','&','|','(',')','#']
for x in range (len(simbolos)):
    tablaSimbolos[simbolos[x]] = tokens[x]

z = tablaSimbolos.copy()
z.update(reserved)
tablaSimbolos = z

# Metodo para agregar renglones a la tabla de simbolos
def addTabla(valor,tipo):
    if valor not in tablaSimbolos.keys():
        tablaSimbolos[valor] = tipo

# C:\Users\elzuk\Desktop\pitón\MiniCompiler\codigo.txt
ubicacion = 'C:/Users/elzuk/Desktop/pitón/MiniCompiler/codigo.txt'
data = open(ubicacion,'r')

# Depuracion de comentarios - - - - - - - - - - -
def depurar(archivo):
    archivofinal = ''
    for dato in archivo:
        aux = dato
        for i in range(0,len(dato)):
            #print(dato[i])
            if dato[i] == "#":
                aux = re.sub(r'#\w*','',dato[i])
            #print(archivofinal + 'final')
            #print(aux + 'auxiliar')}
        archivofinal += aux
    return archivofinal

codigo = depurar(data)


# Generamos el .dep
ubicacionD = ubicacion.replace("txt","dep")
auxD = open( ubicacionD ,'w')
auxD.write(codigo)
auxD.close()


# Construimos el Lexer - PARTE FINAL
lexer = lex.lex()
data = open(ubicacionD,'r')
lexer.input(data.read())


# TokenizaInador
ListaLineas = [[]]
Renglon = 1
Lexema = None
Token = None
for tok in lexer:



    if Renglon != lexer.lineno:
        ListaLineas.append([])
        Renglon = lexer.lineno

    Lexema = tok.value
    Token = tok.type

    ListaLineas[-1].append(Token)

    print("Renglón: "+ str(Renglon) + ", Lexema: "+ str(Lexema) +", Token: "+ str(Token) )

    if str(tok.type) != "COMMENT":
        if "INT" in ListaLineas[- 1] or "STRING" in ListaLineas[ - 1] or "BOOLEAN" in ListaLineas[- 1]:
            addTabla(str(tok.value),str(tok.type))


# Tabla de simbolos
def print_symbol_table():
    print("\n\nTabla de símbolos:")
    print("-" * 57)
    print("| {:<20} | {:<30} |".format("Lexema", "Token"))
    print("-" * 57)

    for lexema,token in tablaSimbolos.items():
        print("| {:<20} | {:<30} |".format(lexema, token))

    print("-" * 57)


print_symbol_table()
# Lista de lineas
print(ListaLineas)