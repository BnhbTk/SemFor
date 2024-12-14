from ply import lex,yacc

from use_case import Package

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

def p_start(p):
    """start : eols STARTUML name EOL defs ENDUML eols
    """
    pass

def p_eols(p):
    """eols : EOL eols
    |
    """

def p_name(p):
    """name : ID
    |
    """
    pass
    

def p_defs(p):
    """defs : one_def  EOL
        | defs one_def EOL
    """
    pass

def p_one_def(p):
    """one_def : ACTOR def_act alias stereo
    | ACTOR_TXT alias stereo
    | USECASE def_uc alias stereo
    | USE_CASE_TXT alias stereo
    | var arrow var ucl_link
    | var INHERIT var
    | PACKAGE ID LBRACE defs RBRACE
    | 
    """
    pass

def p_stereo(p):
    """stereo : STEREO
    |
    """
    pass

def p_def_act(p):
    """def_act : ID
    | ACTOR_TXT
    | STRING
    """
    pass

def p_def_uc(p):
    """def_uc : ID
    | USE_CASE_TXT
    | STRING
    """
    pass

def p_ucl_link(p):
    """ucl_link : COLON EXTENDS
    | COLON INCLUDES
    | COLON ID
    |
    """
    pass
    
def p_arrow(p):
    """arrow : RIGHT_ARROW_1
    | RIGHT_ARROW_2
    """

def p_var(p):
    """var : ID
    | USE_CASE_TXT
    | ACTOR_TXT
    """
    pass

def p_alias(p):
    """alias : AS ID
    |
    """
    pass

def p_error(p):
    print(f"Syntax error {p}")


parser=yacc.yacc()
with open("usecase.plantuml") as f:
    spec=f.read()

yacc.parse(spec)
