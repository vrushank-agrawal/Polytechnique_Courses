# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:02:51 2020

@author: 123
"""
import math

def print_recipe(recipe):
    """Pretty print recipe, which is a dictionary whose keys are
    ingredients and whose values are their corresponding amounts.
    """
    for i,v in recipe.items():
        print(f'{i}: {v}')

def read_recipe(recipe_file_name):
    """Read recipe file 'recipe_file_name', and return ingredients as a
    dictionary whose keys are ingredients and whose values are the
    corresponding amounts.
    """
    with open(recipe_file_name, 'r') as f:
        dict_recipe={}
        for line in f:
            if line!='\n':
                a=line.strip().split(',')
                dict_recipe[a[0].strip()]=int(a[1].strip())
    return dict_recipe

def write_recipe(recipe, recipe_file_name):
    """Write recipe to a file named recipe_file_name."""
    with open(recipe_file_name, 'w') as f:
        for i,j in recipe.items():
            f.write(f'{i},{j}'+'\n')
    
def read_fridge(fridge_file_name):
    """Read fridge file 'fridge_file_name', and return the ingredients
    held in the given fridge as an ingredient=amount dictionary.
    """
    with open(fridge_file_name, 'r') as f:
        items={}
        for line in f:
            if line!='\n':
                a=line.strip().split(',')
                if a[0].strip() in items:
                    items[a[0].strip()]+=int(a[1].strip())
                else:
                    items[a[0].strip()]=int(a[1].strip())
    return items

def is_cookable(recipe_file_name, fridge_file_name):
    """Return True if the contents of the fridge named fridge_file_name
    are sufficient to cook the recipe named recipe_file_name.
    """
    recipe=read_recipe(recipe_file_name)
    fridge=read_fridge(fridge_file_name)
    for i,v in recipe.items():
        if i not in fridge or v>fridge[i]:
            return False
    return True
    
def add_recipes(recipes):
    """Return a dictionary representing the sum of all of
    the recipe dictionaries in recipes.
    """
    ingreds={}
    for recipe in recipes:
       for i in recipe:
           if i not in ingreds:
               ingreds[i]=0
           ingreds[i]+=recipe.get(i,0)
    return ingreds

def create_shopping_list(recipe_file_names, fridge_file_name):
    """Return the shopping list (a dictionary of ingredients and
    amounts) needed to cook the recipes named in recipe_file_names,
    after the ingredients already present in the fridge named
    fridge_file_name have been used.
    """
    recipes=[read_recipe(i) for i in recipe_file_names]
    ingredients=add_recipes(recipes)
    fridge=read_fridge(fridge_file_name)
    items_needed={}
    for i in ingredients:
        if i not in fridge or fridge[i]<ingredients[i]:
            items_needed[i]=ingredients[i]-fridge.get(i, 0)
    return items_needed

def total_price(shopping_list, market_file_name):
    """Return the total price in millicents of the given shopping_list
    at the market named market_file_name.
    """
    market=read_fridge(market_file_name)
    price=0
    for i,v in shopping_list.items():
        price+=(v*market.get(i,0))
    return price

def find_cheapest(shopping_list, market_file_names):
    """Return the name of the market in market_file_names
    offering the lowest total price for the given shopping_list,
    together with the total price.
    """
    markets=[read_fridge(i) for i in market_file_names]
    prices=[0 for i in range(len(markets))]
    for market in markets:
        for i,v in shopping_list.items():
            prices[markets.index(market)]+=(v*market.get(i,0))
    return (market_file_names[prices.index(min(prices))], min(prices))

def update_fridge(fridge_file_name, recipe_file_names, market_file_names, new_fridge_file_name):
    """Compute the shopping list for the given recipes after the
    ingredients in fridge fridge_file_name have been used; find the cheapest
    market; and write the new fridge contents to new_fridge_file_name.
    Print the shopping list, the cheapest market name, and the total
    amount to be spent at that market.
    """
    shopping_list=create_shopping_list(recipe_file_names, fridge_file_name)
    print('Shopping list:')
    print_recipe(shopping_list)
    where_to_go=find_cheapest(shopping_list, market_file_names)
    print(f'Market: {where_to_go[0]}')
    print(f'Total cost: {where_to_go[1]}')
    with open(new_fridge_file_name, 'w') as new_fridge:
        fridge=add_recipes([shopping_list, read_fridge(fridge_file_name)])
        for i,v in fridge.items():
            new_fridge.write(f'{i},{v}\n')
    
def distributed_shopping_list(shopping_list, market_file_names):
    """Distribute shopping_list across the markets named in market_file_names
    to minimize the total cost.
    """
    items_and_markets={'markets': [read_recipe(i) for i in market_file_names], 'cheap': {}}
    for name in market_file_names:
        items_and_markets['cheap'][name]={}
    for i,v in shopping_list.items():
        cost=math.inf
        for market in items_and_markets['markets']:
            if market[i]<cost:
                cost=market[i]
                pos=items_and_markets['markets'].index(market)
        items_and_markets['cheap'][market_file_names[pos]][i]=v
    return items_and_markets['cheap']