# Dumps values into a passive tracer field
# 'blue' for cold (-1) : y >  y_centre
# 'red' for hot (+1)   : y <= y_centre

def val( (x,y,z), t):
    y_centre = 18325.597799

    blue=-1
    red=-1

    if(y>y_centre):
        fval=-1.0
    else:
        fval=1.0

    return fval
