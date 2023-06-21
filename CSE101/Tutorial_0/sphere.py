# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 16:31:31 2020

@author: 123
"""

import math
r_str = input("please enter the radius:")
r = float(r_str)

v = (4/3)*math.pi*(r**3)

print('The volume of the sphere of radius', r_str, 'is:', v)