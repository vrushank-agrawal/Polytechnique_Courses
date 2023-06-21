# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 21:02:38 2020

@author: 123
"""
import random

class Card:
    """French playing cards.

    Class attributes:
    suit_names -- the four suits Clubs, Diamonds, Hearts, Spades
    rank_names -- the 13 ranks in each suit: Two--Ten, Jack, Queen, King, Ace
    Data attributes:
    suit, rank -- the Card's suit and rank, as indices into the lists above
    """
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
             "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

    def __init__(self, suit, rank):
        self.suit=suit
        self.rank=rank
    
    def __str__(self):
        """Returns a readable string representation."""
        return '{} of {}'.format(self.rank_names[self.rank], self.suit_names[self.suit])
    
    def __eq__(self, other):
        return ((self.suit, self.rank) == (other.suit, other.rank))
    
    def matching_card(self):
        """Return the card which matches self."""
        return Card(3-self.suit, self.rank)

class Deck:
    """A deck of Cards.

    Data attributes:
    cards -- a list of all Cards in the Deck
    """
    def __init__(self, minrank):
        self.cards=[]
        for j in range(4):
            for i in range(13-minrank):
                self.cards.append(Card(j,minrank+i))        
        if Card(0,10) in self.cards: self.cards.remove(Card(0,10))
    
    def __str__(self):
        return ', '.join([str(i) for i in self.cards])
        
    def pop(self):
        """Remove and return last card from deck."""
        if len(self.cards)!=0:
            return self.cards.pop()
    
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
        
class Player:
    """A player of the card game.

    Data attributes:
    name -- the name of the player
    cards -- a list of all the player's cards (their "hand")
    """ 
    def __init__(self, name):
        self.name=name
        self.cards=[]
        
    def __str__(self):
        if self.cards==[]:
            return 'Player {} has no cards'.format(self.name)
        return 'Player {} has: '.format(self.name) + ', '.join([str(i) for i in self.cards])
    
    def add_card(self, card):
        """Add card to player's hand."""
        self.cards.append(card)
    
    def num_cards(self):
        """Return number of cards in player's hand."""
        return len(self.cards)
    
    def remove_card(self, i):
        """Remove and return i'th card from player's hand."""
        return self.cards.pop(i)
    
    def remove_matches(self):
        """Remove all pairs of matching cards."""
        times = 0
        original_cards = self.cards[:]
        for card in original_cards:
            for match_card in original_cards:
                if card==match_card.matching_card() and match_card in self.cards:
                    print('Player {}: {} matches {}'.format(self.name, card, match_card))
                    self.cards.remove(card)
                    self.cards.remove(match_card)
                    times+=1
        return times

class CardGame:
    """A class for playing card games.

    Data attributes:
    players -- a list of Player objects which participate in the game
    deck -- a Deck of Cards used for playing
    numcards -- number of Cards in the game
    """
    def __init__(self, players, minrank):
        """Data atributes initialisation."""
        self.players=[Player(i) for i in players]
        self.deck=Deck(minrank)
        self.numcards=len(self.deck.cards)
    
    def __str__(self):
        """String representing each player and all of their cards."""
        return '\n'.join([str(i) for i in self.players])
    
    def shuffle_deck(self):
        """Shuffle the game's deck."""
        self.deck.shuffle()
        
    def deal_cards(self):
        """Deal all cards in the deck to the players, round-robin."""
        for i in range(self.numcards):
            for j in self.players:
                if len(self.deck.cards)==0: break
                j.add_card(self.deck.cards.pop())
    
    def simple_play(self):
        """Play a simple matching game.
        For each player, remove all matching pairs.
        Winners are the players with the most matches.
        """
        matches=[player.remove_matches() for player in self.players]
        high = max(matches)
        winner_names = []
        for i in range(len(matches)):
            if matches[i] == high:
                winner_names.append(self.players[i].name)
        if len(winner_names) == 1: print(f'The winner is {winner_names[0]}')
        else : print('The winners are ' + ' and '.join(winner_names))
        return winner_names