# semantics of x=x-y
A=lambda x,y:(x-y,y)

# semantics of y=y-x
B=lambda x,y:(x,y-x)

# semantics of IF
K=lambda x,y:A(x,y) if x>y else B(x,y)


def gcd(x,y):
    while x!=y:
        if x>y:
            x=x-y
        else:
            y=y-x
    return (x,y)



def fixed_point(xx,yy):
    def h_bc(w):
        return lambda x,y:w(*K(x,y)) if x!=y else (x,y)
    
    y0=lambda x,y:None
    while True:
        next_y=h_bc(y0)
        if next_y(xx,yy)==y0(xx,yy) and y0(xx,yy) is not None:
            return next_y
        y0=next_y


W=fixed_point(140,40)
print(W)


print(W(140,40))
print(gcd(140,40))
