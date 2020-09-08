# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import os
import ply.lex as lex
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
t_NUM = r'\d{3}.\d+'
t_NUMTC = r'</NUM_VALOR>'
t_FECHAT = r'<DES_FECHA>'
t_FECHA = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}'
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
t_NUMBER = r'\d+' #prueba de Git
t_TRASH = r'<xs:([a-zA-Z]+|\s+|[0-9]+|(=|\"|_|:|/|.|-)+)>{1}'

#<xs:schema id="Datos_de_INGC011_CAT_INDICADORECONOMIC" xmlns="" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:msdata="urn:schemas-microsoft-com:xml-msdata">

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
