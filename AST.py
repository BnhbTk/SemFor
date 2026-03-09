from collections import namedtuple


# This is the solution with lists
prog1=["sequence",
    ["assign",["var","v1"],["const",0]],
    ["sequence",
        ["assign",["var","v2"],["const",0]],
        ["while",
            [">",["var","v1"],["var","v2"]],
            ["sequence",
                ["assign",["var","v1"],["var",["v2"]]],
                ["assign",["var","v2"],["+",["var","v1"],["const",1]]]
            ]
        ]
    ]
]

# This is the solution with namedtuple. This solution has a more 
# interesting abstraction level, but still lacks good encapsulation.
Assign=namedtuple('Assign', ['var', 'value'])
While=namedtuple('While', ['condition', 'body'])
Sequence=namedtuple('Sequence', ['first', 'second'])
Var=namedtuple('Var', ['name'])
Const=namedtuple('Const', ['value'])
BinOp=namedtuple('BinOp', ['op','first', 'second'])
If=namedtuple("If",["condition","positive","negative"])
Pass=namedtuple("Pass",[])

prog2=Sequence(
    Assign(Var('v1'), Const(0)),
    Sequence(
        Assign(Var('v2'), Const(0)),
        While(
            BinOp('>', Var('v1'), Var('v2')),
            Sequence(
                Assign(Var('v1'), Var('v2')),
                Assign(Var('v2'), BinOp('+', Var('v1'), Const(1)))
            )
        )
    )
)

pgcd=While(
        BinOp("!=",Var("a"),Var("b")),
        If(
            BinOp(">",Var("a"),Var("b")),
            Assign(Var("a"),BinOp("-",Var("a"),Var("b"))),
            Assign(Var("b"),BinOp("-",Var("b"),Var("a")))
        )
)

# The OOP solution has a better abstraction. It allows for a more
# convenient manipulation of the AST (through inheritance ans encapsulation).
# We use here the metho node2gv to built a Graphviz representation of each node.
# Notice the function node2gv returns an interger that uniquely identifies a node.

# This class is a helper class used to manage the identities of nodes
class Counter:
    def __init__(self):
        self.count=0
    
    def next(self):
        self.count+=1
        return self.count

#Arithmetic expressions
class Expression:
    def node2gv(self,counter,output) -> int:
        pass

class ArithmeticExpression(Expression):
    pass

class IntConstant(ArithmeticExpression):
    def __init__(self,value) -> None:
        self.value=value
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Const({self.value})" shape=oval style=filled fillcolor=lightgreen]')
        return counter.count
    


class IntVariable(ArithmeticExpression):
    def __init__(self,name) -> None:
        self.name=name
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Var({self.name})" shape=egg style=filled fillcolor=pink]')
        return counter.count
    

class UnaryIntOperator(ArithmeticExpression):
    def __init__(self,op,operand) -> None:
        self.op=op
        self.operand=operand
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="{self.op}" style=filled shape=septagon fillcolor=lightyellow]')
        child=self.operand.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child}')
        return v
    


class BinaryIntOperator(ArithmeticExpression):
    def __init__(self,op,operand1,operand2) -> None:
        self.op=op
        self.operand1=operand1
        self.operand2=operand2
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="{self.op}" style=filled shape=septagon fillcolor=lightyellow]')
        child1=self.operand1.node2gv(counter,output)
        child2=self.operand2.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1}')
        output.append(f'Node{v} -> Node{child2}')
        return v

#Boolean Expressions
class BooleanExpression(Expression):
    pass

class BooleanConstant(BooleanExpression):
    def __init__(self,value):
        self.value = value
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Const({self.value})"]')
        return counter.count

class BooleanVariable(BooleanExpression):
    def __init__(self,name):
        self.name = name
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Var({self.name})" shape=egg style=filled fillcolor=pink]')
        return counter.count


class UnaryBooleanOperator(BooleanExpression):
    def __init__(self,op,operand):
        self.op = op
        self.operand = operand
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="{self.op}" style=filled shape=septagon fillcolor=lightyellow]')
        child=self.operand.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child}')
        return v

class BinaryBooleanOperator(BooleanExpression):
    def __init__(self,op,operand1,operand2):
        self.op = op
        self.operand1 = operand1
        self.operand2 = operand2
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="{self.op}" style=filled shape=septagon fillcolor=lightyellow]')
        child1=self.operand1.node2gv(counter,output)
        child2=self.operand1.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1}')
        output.append(f'Node{v} -> Node{child2}')
        return v

class CompareIntegerOperator(BooleanExpression):
    def __init__(self,op,operand1,operand2):
        self.op = op
        self.operand1 = operand1
        self.operand2 = operand2
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="{self.op}" style=filled shape=septagon fillcolor=lightyellow]')
        child1=self.operand1.node2gv(counter,output)
        child2=self.operand2.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1}')
        output.append(f'Node{v} -> Node{child2}')
        return v
        
#Instructions

class Instruction:
    def node2gv(self,counter,output):
        pass

class Assign(Instruction):
    def __init__(self,var,expression) -> None:
        self.var=var
        self.expression=expression
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="Assign" style="filled,rounded" shape=box fillcolor=lightblue]')
        child1=counter.next()
        output.append(f'Node{counter.count} [label="Var({self.var})" shape=egg style=filled fillcolor=pink]')
        child2=self.expression.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1} [label="left"]')
        output.append(f'Node{v} -> Node{child2} [label="expression"]')
        return v
    

class Skip(Instruction): 
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="Skip" style="filled,rounded" shape=box fillcolor=lightblue]')
        return counter.count

class Sequence(Instruction):
    def __init__(self,first,second) -> None:
        self.first=first
        self.second=second
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="Sequence" style="filled,rounded" shape=box fillcolor=lightblue]')
        child1=self.first.node2gv(counter,output)
        child2=self.second.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1} [label="first"]')
        output.append(f'Node{v} -> Node{child2} [label="second"]')
        return v
    

class If(Instruction):
    def __init__(self,cdt,positive,negative) -> None:
        self.cdt=cdt
        self.positive=positive
        self.negative=negative
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="If" style="filled,rounded" shape=box fillcolor=lightblue]')
        child1=self.cdt.node2gv(counter,output)
        child2=self.positive.node2gv(counter,output)
        child3=self.negative.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1} [label="condition"]')
        output.append(f'Node{v} -> Node{child2} [label="then"]')
        output.append(f'Node{v} -> Node{child3} [label="else"]')
        return v
    


class While(Instruction):
    def __init__(self,cdt,internal) -> None:
        self.cdt=cdt
        self.internal=internal
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="While" style="filled,rounded" shape=box fillcolor=lightblue]')
        child1=self.cdt.node2gv(counter,output)
        child2=self.internal.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1} [label="condition"]')
        output.append(f'Node{v} -> Node{child2} [label="body"]')
        return v


# Examples of AST
division=Sequence(
        Assign("r",IntVariable("a")),
        Sequence(
            Assign("q",IntConstant(0)),
            While(
                CompareIntegerOperator(">=",IntVariable("r"),IntVariable("b")),
                Sequence(
                    Assign("q",BinaryIntOperator("+",IntVariable("q"),IntConstant(1))),
                    Assign("r",BinaryIntOperator("-",IntVariable("r"),IntVariable("b")))
                )
            )
        )
    )

gcd=While(
    CompareIntegerOperator('!=',IntVariable("x"),IntVariable("y")),
    If(
        CompareIntegerOperator('>',IntVariable("x"),IntVariable("y")),
        Assign("x",BinaryIntOperator("-",IntVariable("x"),IntVariable("y"))),
        Assign("y",BinaryIntOperator("-",IntVariable("y"),IntVariable("x")))
    )
)

# This function generate the whole representation of the AST as Graphviz code
def get_gv(instruction:Instruction):
    counter=Counter()
    output=[]
    instruction.node2gv(counter,output)
    newline="\n"
    return "\n".join(["digraph G {",
        'node [fontname="arial"]',
        'edge [fontname="arial" fontsize=10 fontcolor=green]',
        newline.join(output),
        "}"
    ])

# You can save the result in a file that can be viewed with the Graphviz CLI tools
print(get_gv(division))
