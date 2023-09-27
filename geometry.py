#!/usr/env/python3

import sys
from token import OP
sys.path.append('/opt/Coreform-Cubit-2023.8/bin/')
import cubit
import numpy as np

class Pattern:
    def __init__(self, name = "", **kwargs):
        self.name = name
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])   

# to do
class Polar(Pattern):
    def __init__(self, name="polar",**kwargs):
        super().__init__(name, **kwargs)

    def create():
        # the shape to be copied
        template = self.template
        # how many copies
        n_copies = self.copies
        # the direction about which we will pattern
        direction = self.direction
        # the centroid of the radius

class Operations:
    def __init__(self, name = "", **kwargs):
        self.name = name
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])   

class Union(Operations):
    def __init__(self, name = "union",**kwargs):
        super().__init__(name, **kwargs)

    def create(self):
        entities = []
        for item in self.entities:
            entities.append(item.cubit_entity_handle)

        self.cubit_entity_handle = cubit.unite(entities)[0]

class Subtract(Operations):
    def __init__(self, name = "subtract",**kwargs):
        super().__init__(name, **kwargs)

    def create(self):
        tools_in = []
        for item in self.tools_in:
            tools_in.append(item.cubit_entity_handle)

        bodies_in = []
        for item in self.bodies_in:
            bodies_in.append(item.cubit_entity_handle)

        self.cubit_entity_handle = cubit.subtract(tools_in,bodies_in)[0]

class Geometry:
    def __init__(self, name = ""):
        self.name = name

class Box(Geometry):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])

    def create(self):
        height = self.height
        width = self.width
        depth = self.depth

        entity = cubit.brick(width = width, depth = depth, height = height)

        if hasattr(self,'position'):
            cubit.move(entity,self.position)

        if hasattr(self,"direction"):
            if hasattr(self,"position"):
                position = self.position
            else:
                position = [0,0,0]

            # get the rotation angle
            dir = cubit.Dir(0,0,1) # cylinder default is along z

            normal = self.direction
            normal_v = cubit.Dir(normal[0],normal[1],normal[2])
            angle = dir.dot(normal_v)
            angle_degrees = np.degrees(np.arccos(angle))
            cubit.cmd("rotate volume %i angle %f about origin %f %f %f direction %f %f %f" % \
                      (entity.id(),angle_degrees,position[0],position[1],position[2],\
                       normal[0],normal[1],normal[2]))
            
        self.cubit_entity_handle = entity

class Cylinder(Geometry):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])

    def create(self):
        height = self.height
        radius = self.radius
        cylinder = cubit.cylinder(height = height, x_radius = radius, y_radius = radius, top_radius = radius)

        if hasattr(self,'position'):
            cubit.move(cylinder,self.position)

        if hasattr(self,"direction"):
            if hasattr(self,"position"):
                position = self.position
            else:
                position = [0,0,0]

            # get the rotation angle
            dir = cubit.Dir(0,0,1) # cylinder default is along z

            normal = self.direction
            normal_v = cubit.Dir(normal[0],normal[1],normal[2])
            angle = dir.dot(normal_v)
            angle_degrees = np.degrees(np.arccos(angle))
            cubit.cmd("rotate volume %i angle %f about origin %f %f %f direction %f %f %f" % \
                      (cylinder.id(),angle_degrees,position[0],position[1],position[2],\
                       normal[0],normal[1],normal[2]))
            
        self.cubit_entity_handle = cylinder


