# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 20:15:00 2020

@author: 123
"""
import random

COLORS = ['RED', 'GREEN', 'BLUE', 'PURPLE', 'BROWN', 'YELLOW']

def create_code():
    """Return 4-element list of strings randomly chosen from
    COLORS with repetition.
    """      
    s = []
    for i in range(4):
        s.append(random.choice(COLORS))
    return s

def black_pins(guess, code):
    """guess, code: 4-element lists of strings from COLORS
    Returns the number of black pins, determined by the standard
    Mastermind rules
    """
    a=0
    for i in range(len(code)):
        if guess[i] == code[i]:
            a+=1
    return a

def score_guess(guess, code):
    """guess, code: 4-element lists of strings
    Return (b, w) where
    b is the number of black pins (exact matches), and
    w is the number of white pins (correct colors in wrong places)
    """
    blackpins = black_pins(guess, code)
    white=0; lst = []
    for i in range(len(code)):
        a=guess.count(guess[i])
        b=code.count(guess[i])
        if guess[i] not in lst:
            x=min(a,b)
            for j in range(len(code)):
                if guess[j]==code[j] and guess[i]==guess[j]:
                    x-=1
            white+=x
        lst.append(guess[i])
    return (blackpins, white)

def str_with_suffix(n):
    """Convert the integer n to a string expressing the corresponding 
    position in an ordered sequence.
    Eg. 1 becomes '1st', 2 becomes '2nd', etc.
    """
    if n<0:
        x = -n
        if x%100 == 11 or x%100 == 12 or x%100 == 13:
            return str(n) + "th"
        if x%10 == 1:
            return str(n) + "st"
        if x%10 == 2:
            return str(n) + "nd"
        if x%10 == 3:
            return str(n) + "rd"
        else:
            return str(n) + "th"
    if n%100 == 11 or n%100 == 12 or n%100 == 13:
        return str(n) + "th"
    elif n%10 == 1:
        return str(n) + "st"
    elif n%10 == 2:
        return str(n) + "nd"
    elif n%10 == 3:
        return str(n) + "rd"
    else:
        return str(n) + "th"

def input_guess():
    """Input four colors from COLORS and return as list.
    """
    lst= []
    print("Enter your guess:")
    a=1; n=0
    while n<4:
        b=str_with_suffix(a)
        a+=1
        x=input(b+" pin: ")
        if x not in COLORS:
            print("Please input a color from the list \
                      ['RED', 'GREEN', 'BLUE', 'PURPLE', 'BROWN', 'YELLOW']")
            a-=1
        else:
            lst.append(x)
            n+=1
    return lst

def one_round(code):
    """Input guess, score guess, print result, and return True iff
    user has won.
    """
    guess = input_guess()
    a=[]
    a = score_guess(guess, code)
    b=int(a[0]); w=int(a[1])
    print("Score: ",b, "black,", w, "white")
    if b == 4:
        return True
    else:
        return False
    
def play_mastermind(code):
    """Let user guess the code in rounds
    """
    n=1
    while n!=0:
        print("Round ", n)
        guess = input_guess()
        a=[]
        a = score_guess(guess, code)
        b=int(a[0]); w=int(a[1])
        print("Score: ",b, "black,", w, "white")
        if b == 4:
            print("You win!")
            n=0
        else:
            n+=1
    


        
