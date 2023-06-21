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
