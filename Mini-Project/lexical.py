from ply import lex

tokens=("STARTUML","ENDUML","COLON","RIGHT_ARROW_1","RIGHT_ARROW_2","ACTOR","ID","AS","USECASE","STRING",
        "PACKAGE","LBRACE","RBRACE","INHERIT","STEREO","INCLUDES","EXTENDS","ACTOR_TXT","USE_CASE_TXT","EOL")

reserved={"actor":"ACTOR","as":"AS","usecase":"USECASE","package":"PACKAGE","includes":"INCLUDES","extends":"EXTENDS"}

t_STARTUML="@startuml"
t_ENDUML="@enduml"
t_COLON=":"
t_RIGHT_ARROW_1="-+>"
t_RIGHT_ARROW_2=r"\.+>"
t_LBRACE=r"\{"
t_RBRACE=r"\}"
t_INHERIT=r"<\|--"
t_EOL=r"\n"


def t_STRING(t): 
    r'"[^"]*"'
    t.value=t.value[1:-1]
    return t

def t_STEREO(t):
    r"<<[a-zA-Z_][a-zA-Z_0-9]*>>"
    t.value=t.value[2:-2]
    return t

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in reserved.keys():
        t.type=reserved[t.value]
    return t

def t_ACTOR_TXT(t):
    ":[^ :\n][^\n:]*:"
    t.value=t.value[1:-1]
    return t

def t_USE_CASE_TXT(t):
    r"\([^ \(\n][^\n:]*\)"
    t.value=t.value[1:-1]
    return t

t_ignore=" \t"

def t_error(t):
    raise ValueError(f"Unexpected symbol {t}")
    
lexer=lex.lex()

# You can use the two examples provided in the project statement
with open("usecase.plantuml") as f:
    spec=f.read()

# This part is just a test for the lexical part. It should be removed when you make the syntactic part
lexer.input(spec)
while True:
    tok=lexer.token()
    if tok:print(tok)
    else:break
