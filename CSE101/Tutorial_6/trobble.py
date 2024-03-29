"""
Created on Tue Nov  3 10:10:51 2020

@author: 123
"""

import random

class Trobble:
    """Trobbles: simplified digital pets.

    Data Attributes:
    name -- the Trobble's name.
    sex -- 'male' or 'female'.
    age -- an integer between 0 (dead) and 10 (full health) inclusive
    health -- a non-negative integer (0 is dead)
    hunger -- a non-negative integer (0 is not hungry)
    """
    
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        self.health = 10
        self.age = 0
        self.hunger = 0
    
    def __str__(self):
        """Give a string representation of the Trobble object's status, in the
        form '_name_: _sex_, health _health_, hunger _hunger_, age _age_'
        where _name_, _sex_, _health_, _hunger_ and _age_ are the values of
        the data attributes with the same name.
        """
        return '{}: {}, health {}, hunger {}, age {}'.format(
                self.name, self.sex, self.health, self.hunger, self.age)
   
    def next_turn(self):
        """End the turn for the instance and recompute the attribute values
        for the next turn.
        """
        if self.health <= 0:
            return
        self.age += 1
        self.hunger += self.age
        self.health = max(0, self.health-(self.hunger // 20))

    def feed(self):
        """Feed the instance to decrease the hunger by 25
        with a minimum value of 0.
        """
        self.hunger = max(0, self.hunger-25)
    
    def cure(self):
        """Increase the health of the instance by 5 up to the maximum of 10.
        """
        self.health = min(10, self.health+5)

    def is_alive(self):
        """Return True if the health of the instance is positive,
        otherwise False.
        """
        return self.health > 0

def get_name():
    return input('Please give your new Trobble a name: ')

def get_sex():
    sex = None
    while sex is None:
        prompt = 'Is your new Trobble male or female? Type "m" or "f" to choose: '
        choice = input(prompt)
        if choice == 'm':
            sex = 'male'
        elif choice == 'f':
            sex = 'female'
    return sex

def get_action(actions):
    while True:
        prompt = f"Type one of {', '.join(actions.keys())} to perform the action: "
        action_string = input(prompt)
        if action_string not in actions:
            print('Unknown action!')
        else:
            return actions[action_string]
        
def play():
    name = get_name()
    sex = get_sex()
    trobble = Trobble(name, sex)
    actions = {'feed': trobble.feed, 'cure': trobble.cure}
    while trobble.is_alive():
        print('You have one Trobble named ' + str(trobble))
        action = get_action(actions)
        action()
        trobble.next_turn()
    print(f'Unfortunately, your Trobble {trobble.name} has died at the age of {trobble.age}')

def mate(trobble1, trobble2, name_offspring):
    """Check if the given Trobbles can procreate and if so give back a new
    Trobble that has the sex of trobble1 and the name 'name_offspring'.
    Otherwise, return None.
    """
    if trobble1.age < 4 or trobble2.age < 4:
        return None
    if trobble1.sex == trobble2.sex:
        return None
    return Trobble(name_offspring, trobble1.sex)

def choose_trobble(trobbles):
    """ choose a trobble"""
    while True:
        name = input(f"Choose one of the following trobbles {', '.join(trobbles.keys())}\n")
        if name not in trobbles:
            print('Unkown name')
        else: return trobbles[name]
        
def rand_mate(trobble1, trobbles):
    """Check if the given Trobbles can procreate and if so give back a new
    Trobble that has the sex of trobble1 and the name 'name_offspring'.
    Otherwise, return None.
    """
    if trobble1.age < 4:
        return None
    for i,j in trobbles.items():
        if j.age>3 and j.sex!=trobble1.sex:
            new_name=input('Please enter name of new trobble')
            return Trobble(new_name, random.choice(trobble1.sex, j.sex))

def multi_play():
    name1= get_name()
    sex1 = get_sex()
    if sex1=='male':
        sex2='female'
    else: sex2='male'
    print(f'Trobble 2 is {sex2}')
    name2= get_name()
    trobble1 = Trobble(name1, sex1)
    trobble2 = Trobble(name2, sex2)
    trobbles={trobble1.name: trobble1, trobble2.name: trobble2}
    trobble=choose_trobble(trobbles)
    actions = {'feed': trobble.feed, 'cure': trobble.cure, 'mate': 'rand_mate'}
    while len(trobbles)!=0:
        action=get_action(actions)
        if str(action)=='rand_mate':
            prompt = rand_mate(trobble, trobbles)
            if prompt==None: print('Mating not possible!')
            else: 
                print(prompt)
                trobbles[prompt.name] = prompt
        else: action()
        temp=[]
        for i,j in trobbles.items():
            j.next_turn()
            if not j.is_alive(): temp.append(i)
        for i in temp: del trobbles[i]
        print(f'There are {len(trobbles)} pets still alive')
        if len(trobbles)==0: break
        trobble=choose_trobble(trobbles)
    print('Unfortunately all the trobbles have died')