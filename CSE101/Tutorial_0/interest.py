# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 16:36:29 2020

@author: 123
"""

p = float(input('Write your initial investment:'))
r = float(input("Type the rate of annual interest: "))
n = float(input('The number of times the interest will be compounded per year:'))
y = float(input('Total number of years of investment are:'))

total = p*((1+(r/100)*(1/n))**(n*y))

print('Your expected return is:', total)