from typing import Union
from collections.abc import Callable

class Counter:
    def __init__(self):
        self.count=0
    
    def next(self):
        self.count+=1
        return self.count

#Arithmetic expressions
class Expression:
    def value(self,state) -> Union[int,bool] :
        raise NotImplementedError()
    
    def node2gv(self,counter,output) -> int:
        pass
    
    def operational_semantic(self,state:dict[str,int|bool]) -> int|bool:
        raise NotImplementedError()
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],int|bool]:
        raise NotImplementedError()

class ArithmeticExpression(Expression):
    pass

class IntConstant(ArithmeticExpression):
    def __init__(self,value) -> None:
        self.value=value
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Const({self.value})" shape=oval style=filled fillcolor=lightgreen]')
        return counter.count
    
    def operational_semantic(self,state:dict[str,int|bool]) -> int:
        return self.value
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],int]:
        return lambda _:self.value
    


class IntVariable(ArithmeticExpression):
    def __init__(self,name) -> None:
        self.name=name
    
    def operational_semantic(self,state:dict[str,int|bool]) -> int:
        return state[self.name]
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],int]:
        return lambda state:state[self.name]
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Var({self.name})" shape=egg style=filled fillcolor=pink]')
        return counter.count
    

class UnaryIntOperator(ArithmeticExpression):
    def __init__(self,op,operand) -> None:
        self.op=op
        self.operand=operand
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],int]:
        return None if self.op!="-" else lambda state:-self.operand.denotational_semantic()(state)
    
    def operational_semantic(self,state:dict[str,int|bool]) -> int:
        if self.op=="-":
            return -self.operand.operational_semantic(state)
        else:
            raise NotImplementedError()

    
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
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],int]:
        def make_op(op,x,y):
            match op:
                case "+":
                    return x+y
                case "-":
                    return x-y
                case "*":
                    return x*y
                case "/":
                    return x//y

        return None if self.op not in ["+","-","*","/"] else lambda state:make_op(self.op,self.operand1.denotational_semantic()(state),self.operand2.denotational_semantic()(state))
            
    
    def operational_semantic(self, state:dict[str,int|bool]) -> int:
        match self.op:
            case "+":
                return self.operand1.operational_semantic(state)+self.operand2.operational_semantic(state)
            case "-":
                return self.operand1.operational_semantic(state)-self.operand2.operational_semantic(state)
            case "*":
                return self.operand1.operational_semantic(state)*self.operand2.operational_semantic(state)
            case "/":
                return self.operand1.operational_semantic(state)//self.operand2.operational_semantic(state)
            case _:
                raise NotImplementedError()
    
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
    
    def operational_semantic(self, state:dict[str,int|bool]) -> bool:
        return self.value
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],bool]:
        return lambda _:self.value
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Const({self.value})"]')
        return counter.count

class BooleanVariable(BooleanExpression):
    def __init__(self,name):
        self.name = name
    
    def operational_semantic(self, state:dict[str,int|bool]) -> bool:
        return state[self.name]
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],bool]:
        return lambda state:state[self.name]
    
    def node2gv(self,counter,output):
        counter.next()
        output.append(f'Node{counter.count} [label="Var({self.name})" shape=egg style=filled fillcolor=pink]')
        return counter.count


class UnaryBooleanOperator(BooleanExpression):
    def __init__(self,op,operand):
        self.op = op
        self.operand = operand
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],bool]:
        return None if self.op!="not" else lambda state:not self.operand.denotational_semantic()(state)
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="{self.op}" style=filled shape=septagon fillcolor=lightyellow]')
        child=self.operand.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child}')
        return v
    
    def operational_semantic(self, state:dict[str,int|bool]) -> bool:
        if self.op=="!":
            return not self.operand.operational_semantic(state)

class BinaryBooleanOperator(BooleanExpression):
    def __init__(self,op,operand1,operand2):
        self.op = op
        self.operand1 = operand1
        self.operand2 = operand2
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],bool]:
        def make_op(op,x,y):
            match op:
                case "and":
                    return x and y
                case "or":
                    return x or y
                
        return None if self.op not in ["and","or"] else lambda state:make_op(self.op,self.operand1.denotational_semantic()(state),self.operand2.denotational_semantic()(state))
    
    def operational_semantic(self, state:dict[str,int|bool]) -> bool:
        match self.op:
            case "and":
                return self.operand1.operational_semantic(state) and self.operand2.operational_semantic(state)
            case "or":
                return self.operand1.operational_semantic(state) or self.operand2.operational_semantic(state)
            case _:
                raise NotImplementedError()
    
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
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],bool]:
        def make_op(op,x,y):
            match op:
                case "==":
                    return x==y
                case "!=":
                    return x!=y
                case "<":
                    return x<y
                case ">":
                    return x>y
                case "<=":
                    return x<=y
                case ">=":
                    return x>=y

        return None if self.op not in ["==","!=","<",">","<=",">="] else lambda state:make_op(self.op,self.operand1.denotational_semantic()(state),self.operand2.denotational_semantic()(state))
    
    def operational_semantic(self, state:dict[str,int|bool]) -> bool:
        match self.op:
            case "==":
                return self.operand1.operational_semantic(state) == self.operand2.operational_semantic(state)
            case "!=":
                return self.operand1.operational_semantic(state) != self.operand2.operational_semantic(state)
            case ">":
                return self.operand1.operational_semantic(state) > self.operand2.operational_semantic(state)
            case ">=":
                return self.operand1.operational_semantic(state) >= self.operand2.operational_semantic(state)
            case "<":
                return self.operand1.operational_semantic(state) < self.operand2.operational_semantic(state)
            case "<=":
                return self.operand1.operational_semantic(state) <= self.operand2.operational_semantic(state)
            case _:
                raise NotImplementedError()
    
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
    
    def operational_semantic(self,state:dict[str,int|bool]) -> dict[str,int|bool]:
        raise NotImplementedError()
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],dict[str,int|bool]]:
        raise NotImplementedError()
    
    

class Assign(Instruction):
    def __init__(self,var,expression) -> None:
        self.var=var
        self.expression=expression
    
    def operational_semantic(self, state:dict[str,int|bool]) -> dict[str,int|bool]:
        state[self.var]=self.expression.operational_semantic(state)
        return state
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],dict[str,int|bool]]:
        return lambda state:{**state,self.var:self.expression.denotational_semantic()(state)}
    
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
    
    def operational_semantic(self, state:dict[str,int|bool]) -> dict[str,int|bool]:
        return state
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],dict[str,int|bool]]:
        return lambda state:state

class Sequence(Instruction):
    def __init__(self,first,second) -> None:
        self.first=first
        self.second=second
    
    def operational_semantic(self, state:dict[str,int|bool]) -> dict[str,int|bool]:
        return self.second.operational_semantic(self.first.operational_semantic(state))
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],dict[str,int|bool]]:
        return lambda state:self.second.denotational_semantic()(self.first.denotational_semantic()(state))
    
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
    
    def operational_semantic(self, state:dict[str,int|bool]) -> dict[str,int|bool]:
        if self.cdt.operational_semantic(state):
            return self.positive.operational_semantic(state)
        else:
            return self.negative.operational_semantic(state)
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],dict[str,int|bool]]:
        return lambda state:self.positive.denotational_semantic()(state) if self.cdt.denotational_semantic()(state) else self.negative.denotational_semantic()(state)
    
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
    
    def operational_semantic(self, state:dict[str,int|bool]) -> dict[str,int|bool]:
        while self.cdt.operational_semantic(state):
            state=self.internal.operational_semantic(state)
        return state
    
    def denotational_semantic(self) -> Callable[[dict[str,int|bool]],dict[str,int|bool]]:
        def h_bc(w):
            denot=self.internal.denotational_semantic()
            return lambda state:w(denot(state)) if self.cdt.denotational_semantic()(state) else state
        
        def fixed_point(w,state):
            cur=h_bc(w)
            if w(state)==cur(state) and cur(state) is not None:
                return w
            else:
                return fixed_point(cur,state)
        return lambda state:fixed_point(lambda _:None,state)(state)
        # return lambda state:self.denotational_semantic()(self.internal.denotational_semantic()(state)) if self.cdt.denotational_semantic()(state) else state
        
    
    def node2gv(self,counter,output):
        counter.next()
        v=counter.count
        output.append(f'Node{v} [label="While" style="filled,rounded" shape=box fillcolor=lightblue]')
        child1=self.cdt.node2gv(counter,output)
        child2=self.internal.node2gv(counter,output)
        output.append(f'Node{v} -> Node{child1} [label="condition"]')
        output.append(f'Node{v} -> Node{child2} [label="body"]')
        return v


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

#print(get_gv(division))
# state={"a":7,"b":2,"q":0,"r":0}
state={"x":140,"y":40}
#print(gcd.operational_semantic(state))
print(gcd.denotational_semantic()(state))

