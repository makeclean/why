import sys
from token import OP
sys.path.append('/opt/Coreform-Cubit-2023.8/bin/')
import cubit

from geometry import Box,Cylinder,Union,Subtract

""" start cubit 
"""
def init():
    cubit.init(['cubit','-nojournal'])
    return

def outer_shell(blanket_radius,blanket_width,blanket_height):
    cylinder1 = Cylinder(name="top",radius=blanket_radius,height=blanket_width,\
                        position=[0,blanket_width/2.0 - blanket_radius,blanket_height/2. - blanket_radius],\
                        direction=[0,1,0])
    cylinder1.create()

    cylinder2 = Cylinder(name="bottom",radius=blanket_radius,height=blanket_width,\
                        position=[0,blanket_width/2.0 - blanket_radius, -blanket_height/2.0 + blanket_radius],\
                        direction=[0,1,0])
    cylinder2.create()

    box1 = Box(name="main",height=blanket_height,width=blanket_width,\
               depth=blanket_width - blanket_radius,position=[0,-blanket_radius/2.0,0])
    box1.create()

    box2 = Box(name="front",height=blanket_height - 2.*blanket_radius,width=blanket_width,\
               depth=blanket_radius,position=[0,blanket_width/2.0 - blanket_radius/2.0,0])
    box2.create()

    union = Union(name="blanket",entities=[cylinder1,cylinder2,box1,box2])
    union.create()

    return union
    #return [cylinder1,cylinder2,box1,box2]

def make_blanket():

    blanket_radius = 5.
    blanket_width = 40.
    blanket_height = 100.
    shell_thickness = 1.0

    inner_radius = blanket_radius - shell_thickness
    inner_width = blanket_width -  2*shell_thickness
    inner_height = blanket_height - 2*shell_thickness

    peice = outer_shell(blanket_radius,blanket_width,blanket_height)
    peice2 = outer_shell(inner_radius,inner_width,inner_height)
    
    # make the hollow shell
    shell = Subtract(tools_in=[peice2],bodies_in=[peice])
    #shell = Subtract(tools_in=peice2,bodies_in=peice)
    shell.create()

    # make the inner fill
    inner = outer_shell(inner_radius,inner_width,inner_height)

def main():
    init()
    
    make_blanket()

    cubit.cmd("save as 'test.cub5' overwrite")
    
if __name__ == "__main__":
    main()
