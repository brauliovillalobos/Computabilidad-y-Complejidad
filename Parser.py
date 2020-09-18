# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import os
with open("outfile.txt","r") as file: data=file.read().replace('\n', '')

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
#t_NUM = r'\d{3}\.\d+'
t_NUMTC = r'</NUM_VALOR>'
t_FECHAT = r'<DES_FECHA>'
#t_FECHA = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}'
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

#<xs:schema id="Datos_de_INGC011_CAT_INDICADORECONOMIC" xmlns="" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:msdata="urn:schemas-microsoft-com:xml-msdata">

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

#Parsing rules

#dictionary of names
names = { }

def p_statement_DF(t): #Paso 1
    'statement : DIFFGR CDF DIFFGRC'
    print(t[1])
    print(t[3])

def p_statement_CDF(t): #Paso 2
    'CDF : DATOSINICT CCDFS DATOSINICTC'
    print(t[1])
    print(t[3])

def p_statement_CCDFS(t):
    'CCDFS : CCDF CCDFS'
    print(t[1])
    print(t[2])

def p_statement_CCDFSBase(t):
    'CCDFS : CCDF'
    print(t[1])
def p_statement_CCDF(t): #REGLA 1 de CCDF
    'CCDF : ING CING INGC'
    print(t[1])
    print(t[2])
    print(t[3])


#<diffgr:diffgram xmlns:msdata="urn:schemas-microsoft-com:xml-msdata" xmlns:diffgr="urn:schemas-microsoft-com:xml-diffgram-v1"> <Datos_de_INGC011_CAT_INDICADORECONOMIC xmlns=""> <INGC011_CAT_INDICADORECONOMIC diffgr:id="INGC011_CAT_INDICADORECONOMIC1" msdata:rowOrder="0"> <DES_FECHA>2019-05-25T00:00:00-06:00</DES_FECHA> <NUM_VALOR>588.41000000</NUM_VALOR> </INGC011_CAT_INDICADORECONOMIC> <INGC011_CAT_INDICADORECONOMIC diffgr:id="INGC011_CAT_INDICADORECONOMIC2" msdata:rowOrder="1"> <DES_FECHA>2019-05-26T00:00:00-06:00</DES_FECHA> <NUM_VALOR>588.41000000</NUM_VALOR> </INGC011_CAT_INDICADORECONOMIC> <INGC011_CAT_INDICADORECONOMIC diffgr:id="INGC011_CAT_INDICADORECONOMIC3" msdata:rowOrder="2"> <DES_FECHA>2019-05-27T00:00:00-06:00</DES_FECHA> <NUM_VALOR>588.41000000</NUM_VALOR> </INGC011_CAT_INDICADORECONOMIC> </Datos_de_INGC011_CAT_INDICADORECONOMIC> </diffgr:diffgram>

def p_statement_CING(t):
    'CING : INDICADOR DATE VALOR'

def p_statement_INDICADOR(t):
    'INDICADOR : INDICADORT NUMBER INDICADORTC'
    print(t[1])
    print(t[2])
    print(t[3])

def p_statement_DATE(t):
    'DATE : FECHAT FECHA FECHATC'
    print(t[1])
    print(t[2])
    print(t[3])

def p_statement_VALOR(t):
    'VALOR : NUMT NUM NUMTC'
    print(t[1])
    print(t[2])
    print(t[3])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()
parser.parse(data)

#while True:
#    try:
#        s = input('Input')   # Use raw_input on Python 2
#    except EOFError:
#        break
#    parser.parse(data)
