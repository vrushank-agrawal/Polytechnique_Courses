# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 23:51:08 2020

@author: 123
"""

def lcm(a, b) :
    if a%b==0: 
        return a
    return ((lcm(b, a%b) * a)//(a%b))


def is_palindrome(word):
    if len(word)<=1: 
        return True
    if word[0]!=word[-1]: 
        return False
    new_word=word[1:-1]
    return (is_palindrome(new_word))


def binary_search(sorted_list, lower, upper, element):
    """Return the position of the element in the sublist of sorted_list 
    starting at position lower up to (but excluding) position upper if it 
    appears there. Otherwise return -1.
    """
    if upper>lower:
            mid=(lower+upper)//2
            if element<sorted_list[mid]:
                return (binary_search(sorted_list, lower, mid, element))
            if element>sorted_list[mid]:
                return (binary_search(sorted_list, mid+1, upper, element))
            if sorted_list[mid]==element:
                return mid
    return -1

    
def read_positive_integer(text, position):
    """Read a number starting from the given position, return it and the first
    position after it in a tuple. If there is no number at the given position
    then return None.
    """
    new_text=''
    if text[position] not in '0123456789':
        return None
    for i in range(position, len(text)):
        if text[i] in '0123456789':
            new_text+=text[i]
            position+=1
        if text[i] not in '0123456789':
            break
    return (int(new_text), position)


def evaluate(expression, position):
    """Evaluate the expression starting from the given position. Return
    the value and the first position after the read sub-expression. If the 
    string starting at the given expression is not an arithmetic expression, 
    return None.
    """
    if expression[position].isnumeric():
        return read_positive_integer(expression, position)
    if expression[position]=='(':
        val1=evaluate(expression, position+1)
        op=expression[val1[1]]
        val2=evaluate(expression, val1[1]+1)
        if op=='+':
            val = val1[0] + val2[0]
        elif op=='-':
            val = val1[0] - val2[0]
        elif op=='*':
            val = val1[0] * val2[0]
        return (val, val2[1]+1)
