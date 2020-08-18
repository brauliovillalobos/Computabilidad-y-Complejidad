# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import os
import ply.lex as lex
import github
with open("ejemploTopo.xml","r") as file: data=file.read().replace('\n', '')

# List of token names.   This is always required
tokens = (
    'TOPO',
    'TOPOC',
    'SWITCHES',
    'SWITCHESC',
    'SWITCH',
    'SWITCHC',
    'DPID',
    'DPIDC',
    'NAME',
    'NAMEC',
    'LINKS',
    'LINKSC',
    'SWITCHTOSWITCH',
    'SWITCHTOSWITCHC',
    'LINK',
    'LINKC',
    'PORT',
    'PORTC',
    'DESCRIPTION',
    'DESCRIPTIONC',
    'SWITCHTOOTHER',
    'SWITCHTOOTHERC',
    'NETWORKS',
    'NETWORKSC',
    'NETWORK',
    'NETWORKC',
    'ID',
    'IDC',
    'SUBNET',
    'SUBNETC',
    'NETMASK',
    'NETMASKC',
    'LETTERS',
    'IP',
    'NUMBER'
)

# Regular expression rules for simple tokens

t_TOPO = r'<topo>'
t_TOPOC = r'</topo>'
t_SWITCHES = r'<switches>'
t_SWITCHESC = r'</switches>'
t_SWITCH = r'<switch>'
t_SWITCHC = r'</switch>'
t_DPID = r'<dpid>'
t_DPIDC = r'</dpid>'
t_NAME = r'<name>'
t_NAMEC = r'</name>'
t_LINKS = r'<links>'
t_LINKSC = r'</links>'
t_SWITCHTOSWITCH = r'<switch-to-switch>'
t_SWITCHTOSWITCHC = r'</switch-to-switch>'
t_LINK = r'<link>'
t_LINKC = r'</link>'
t_PORT = r'<port>'
t_PORTC = r'</port>'
t_DESCRIPTION = r'<description>'
t_DESCRIPTIONC = r'</description>'
t_SWITCHTOOTHER = r'<switch-to-other>'
t_SWITCHTOOTHERC = r'</switch-to-other>'
t_NETWORKS = r'<networks>'
t_NETWORKSC = r'</networks>'
t_NETWORK = r'<network>'
t_NETWORKC = r'</network>'
t_ID = r'<id>'
t_IDC = r'</id>'
t_SUBNET = r'<subnet>'
t_SUBNETC = r'</subnet>'
t_NETMASK = r'<netmask>'
t_NETMASKC = r'</netmask>'
t_LETTERS = r'[a-zA-Z ]+'
t_IP = r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?){1,3}\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?){1,3}\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?){1,3}\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?){1,3}'
t_NUMBER = r'\d+'


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