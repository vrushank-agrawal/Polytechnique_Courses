# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:47:51 2020

@author: 123
"""

#!/bin/python3

import math
import os
import random
import re
import sys



def countSubstrings(s, queries):
    final=[]
    for i in range(len(queries)):
        x=queries[i]
        a=x[0]
        b=x[1]
        temp=''
        for j in range(a,b,1):
            temp=temp+s[j]
        subs=(b-a+1)*(b-a+2)//2
        lst=[]
        nos=1
        for j in range(len(temp)//nos):
            pos1=0; pos2=nos
            for l in range(len(temp)//nos):
                element=''
                for k in range(pos1,pos2):
                    element=element+temp[k]
                if element in lst:
                    subs-=1
                if pos2<len(temp):
                    pos1+=1; pos2+=1
                lst.append(element)
            nos+=1
        final.append(subs)
    return final
        
    
                    
def move_queen(n, updated_row, updated_col, r , c, obs):
    p = 0
    while True:
        r = updated_row(r)
        c = updated_col(c)
        key = (r - 1) * n + c
        if (c < 1 or c > n or r < 1 or r > n) or (key in obs):
            return p
        p += 1
    return p
            
def queensAttack(n, k, r_q, c_q, obstacles):
    obs = {}
    for b in obstacles:
        obs[(b[0] - 1) * n + b[1]] = None

    p = 0
    dr = [-1, -1, -1, 0, 0 , 1 , 1,1]
    dc = [0, -1, 1, 1, -1 , 0 , 1,-1]

    for i in range(8):
        p += move_queen(n, (lambda r: r + dr[i]), (lambda c: c + dc[i] ), r_q, c_q, obs)

    return p
    


def commonChild(s1, s2):
    array = [[0 for i in range(len(s1))] for j in range(len(s2))]
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                array[i][j]+=1
    print(array)
    sm=[sum(array[i]) for i in range(len(s1))]
    print(sm)
    mx=max(sm)
    return mx
    

def commonChil(s1, s2):
    m=[0 for i in range(len(s1))]; n=[]; y=0; temp='one'
    for k in range(len(s1)):
        x=0
        for i in range(y,len(s1)):
            for j in range(x,len(s2)):
                if s1[i]==s2[j] and s1[i]!=temp:
                    x=j
                    temp=s1[i]
                    m[k]+=1
                    break
        y=k;
    mx1=max(m)
    y=0; temp='one'
    n=[0 for i in range(len(s2))]
    for k in range(len(s1)):
        x=0
        for i in range(y,len(s2)):
            for j in range(x,len(s1)):
                if s1[i]==s2[j] and s1[i]!=temp:
                    x=j
                    temp=s1[i]
                    n[k]+=1
                    break
        y=k
    mx2=max(n)
    a=max(mx1,mx2)
    return a