# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import os
with open("outfile.txt","r") as file: data=file.read().replace('\n', '')
import pandas as pd
# List of token names.   This is always required
tokens = (
    'INDICADORT',
    'INDICADORTC',
    'NUMT',
    'NUM',
    'NUMTC',
    'FECHAT',
    'FECHA',
    'FECHATC',
    'DIFFGR',
    'DIFFGRC',
    'ING',
    'INGC',
    'NUMBER',
    'LETTERS',
    'DATOSINICT',
    'DATOSINICTC',
    'DATASET',
    'DATASETC',
    'TRASH'
)

# Regular expression rules for simple tokens
t_INDICADORT = r'<COD_INDICADORINTERNO>'
t_INDICADORTC = r'</COD_INDICADORINTERNO>'
t_NUMT = r'<NUM_VALOR>'
t_NUMTC = r'</NUM_VALOR>'
t_FECHAT = r'<DES_FECHA>'
t_FECHATC = r'</DES_FECHA>'
t_DIFFGR = r'<diffgr.+-diffgram-v\d">'
t_DIFFGRC = r'</diffgr:diffgram>'
t_ING = r'<INGC\d+_CAT_INDICADORECONOMIC\sdiffgr:id="INGC\d+_CAT_INDICADORECONOMIC\d+"\smsdata:rowOrder="\d+">'
t_INGC = r'</INGC\d+_CAT_INDICADORECONOMIC>'
t_DATOSINICT = r'<Datos_de_INGC\d+_CAT_INDICADORECONOMIC\sxmlns="">'
t_DATOSINICTC = r'</Datos_de_INGC\d+_CAT_INDICADORECONOMIC>'
t_DATASET = r'DataSet\sxmlns="http://ws.sdde.bccr.fi.cr">'
t_DATASETC = r'</DataSet>'
t_LETTERS = r'[a-zA-Z]+'
t_TRASH = r'<xs:([a-zA-Z]+|\s+|[0-9]+|(=|\"|_|:|/|.|-)+)>{1}'

#Regla de Fecha

def t_FECHA(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}'
    return t

def t_NUM(t):
    r'\d{3}\.\d+'
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

#Creation of Objects of ArrayList type
dates = []
values = []
indicador = []

#Parsing rules

#dictionary of names
names = { }

def p_statement_DF(t): #Paso 1
    'statement : DIFFGR CDF DIFFGRC'

def p_statement_CDF(t): #Paso 2
    'CDF : DATOSINICT CCDFS DATOSINICTC'

def p_statement_CCDFS(t):
    'CCDFS : CCDF CCDFS'

def p_statement_CCDFSBase(t):
    'CCDFS : CCDF'

def p_statement_CCDF(t): #REGLA 1 de CCDF
    'CCDF : ING CING INGC'

def p_statement_CING(t):
    'CING : INDICADOR DATE VALOR'

def p_statement_INDICADOR(t):
    'INDICADOR : INDICADORT NUMBER INDICADORTC'
    indicador.append(t[2])

def p_statement_DATE(t):
    'DATE : FECHAT FECHA FECHATC'
    dates.append(t[2])

def p_statement_VALOR(t):
    'VALOR : NUMT NUM NUMTC'
    values.append(t[2])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()
parser.parse(data)

df = pd.DataFrame(list(zip(indicador,dates,values)), columns=['Indicador','Fecha','Tipo Cambio'])
print(df)
#while True:
#    try:
#        s = input('Input')   # Use raw_input on Python 2
#    except EOFError:
#        break
#    parser.parse(data)
