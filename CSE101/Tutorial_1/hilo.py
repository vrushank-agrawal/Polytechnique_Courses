# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:28:04 2020

@author: 123
"""

def play_hilo(x,n):
    """A simple guessing game.
    The player has to guess the target value x in at most n attempts.
    """
    print('Guess what number I am thinking of?')
    g = x-1
    while (x!=g and n!=0):
        print ("You have ", n," turns left")
        g = int(input())
        n = n-1
        if g==x:
            return "Congratulations!"
        elif g>x:
            print("Lower")
        elif g<x:
            print("Higher")
    
    if g!=x:
        return "You lose!"

def play_random_hilo(a,b,n):
    """Play the hilo game with the target value x chosen 
    randomly from the interval [lower,upper].
    """
    
    import random
    x = random.randint(a,b)
    print('Guess what number I am thinking of?')
    g = x-1
    while (x!=g and n!=0):
        print ("You have ", n," turns left")
        g = int(input())
        n = n-1
        if g==x:
            return "Congratulations!"
        elif g>x:
            print("Lower")
        elif g<x:
            print("Higher")
    
    if g!=x:
        return "You lose!"
    
def warmer_or_colder(a,b,n):
    """ 
    Tells you if the guess is high or low
    """
    
    import random
    x = random.randint(a,b)
    print('Guess what number I am thinking of?')
    g = int(input())
    while (x!=g and n!=0):
        print ("You have ", n," turns left")
        g = int(input())
        n = n-1
        if g==x:
            return "Congratulations!"
        elif g>x:
            print("Lower")
        elif g<x:
            print("Higher")
    
    if g!=x:
        return "You lose!"
     