# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 13:35:33 2020

@author: 123
"""

def name_of_month(m):
    """Given an integer m between 1 and 12 inclusive,
    indicating a month of the year, returns the name of that month.
    For example: name_of_month(1) == 'January' and name_of_month(12) == 'December'.
    If the month does not exist (that is, if m is outside the legal range),
    then this function returns None.
    """
    if m < 1 or m > 12:  # Non-existent month
        return None
    elif m == 1:
        return "January"
    elif m == 2:
        return "February"
    elif m == 3:
        return "March"
    elif m == 4:
        return "April"
    elif m == 5:
        return "May"
    elif m == 6:
        return "June"
    elif m == 7:
        return "July"
    elif m == 8:
        return "August"
    elif m == 9:
        return "September"
    elif m == 10:
        return "October"
    elif m == 11:
        return "November"
    elif m == 12:
        return "December"
    
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
    
def is_leap_year(y):
    """ Return True if y is a leap year, False otherwise. 
    """
    if y%400 == 0:
        return True
    elif y%100 == 0:
        return False
    elif y%4 == 0:
        return True
    else:
        return False
    
def number_of_days(m,y):
    """Returns the number of days in month m of year y.
    """
    if m==1 or m==3 or m==5 or m==7 or m==8 or m==10 or m==12:
        return 31
    if m==4 or m==6 or m==9 or m==11:
        return 30
    if m==2:
        if is_leap_year(y) == True:
            return 29
        else:
            return 28

def date_string(d,m,y):
    """
    Returns the date as a string sentence
    """
    if name_of_month(m) == None:
        return "Nonexistent date"
    elif d > number_of_days(m,y) or d < 0:
        return "Nonexistent date"
    else:
        return "The " + str_with_suffix(d) + " of " + name_of_month(m) + ", " + str(y)

def time_string(n):
    """
    Returns seconds as a string in the form of days, hours,
    minutes, and seconds elapsed
    """    
    d = n//86400
    if d==0:
        w = ""
    elif d==1:
        w = str(d)+" day, "
    else:
        w = str(d)+" days, "
    h = n%86400
    h = h//3600
    if h==0:
        w = w
    else:
        if h==1:
            w = w + str(h)+" hour, "
        else:
            w = w + str(h)+" hours, "
    m = n%3600
    m = m//60
    if m==0:
        w = w
    else:
        if m==1:
            w = w + str(m)+" minute, "
        else:
            w = w + str(m)+" minutes, "
    s = n%60
    if d==0 and h==0 and m==0 and s==0:
        w = "0 seconds"
    elif s==0:
        w = w
    else:
        if s==1:
            w = w + str(s)+" second"
        else:
            w = w + str(s)+" seconds"   
    return w