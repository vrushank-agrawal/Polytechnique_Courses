#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 14:11:59 2018

@author: smith
"""

class Vote:
    """A single vote object.
    Data attributes:
    - preference_list: a list of the preferred parties for this voter,
      in descending order of preference.
    """

    def __init__(self, preference_list):
        self.preference_list = preference_list

    def __repr__(self):
        return 'Vote({})'.format(self.preference_list)

    def __str__(self):
        if self.preference_list == []:
            return 'Blank'
        return ' > '.join(self.preference_list)

    def first_preference(self):
        """The first preference of this vote."""
        if self.preference_list == []:
            return None
        return self.preference_list[0]

    def preference(self, choices):
        """The party among the choices preferred by this vote,
        or None if none of the parties is preferred.
        """
        for pref in self.preference_list:
            if pref in choices:
                return pref
        return None


class Election:
    """A basic election class.
    Data attributes:
    - parties: a list of party names
    - blank: a list of blank votes
    - piles: a dictionary with party names for keys
      and lists of votes (allocated to the parties) for values
    - dead: a list of dead votes
    """

    def __init__(self, parties):
        self.parties = parties
        self.blank = []
        self.piles = {name:[] for name in self.parties}
        self.dead = []

    def add_vote(self, vote):
        """Append the vote to the corresponding pile."""
        party = vote.first_preference()
        if party in self.piles:
            self.piles[party].append(vote)
        else:
            self.blank.append(vote)

    def add_votes_from_file(self, filename):
        """Append each of the votes in the list to the corresponding pile."""
        with open(filename) as file:
            for line in file:
                vote = Vote(line.split())
                self.add_vote(vote)

    def status(self):
        """Return the current status of the election:
        a dictionary mapping each of the party names in the piles to
        the number of votes in their pile.
        """
        return {party: len(votes) for (party, votes) in self.piles.items()}

    def first_past_the_post_winner(self):
        """Return the winner of this election under
        the first-past-the-post system, or None if
        the election is tied.
        """
        (winner, highest) = (None, -1)  # -1 is < any possible number of votes
        for (party, total) in self.status().items():
            if total > highest:  # Update winner
                (winner, highest) = (party, total)
            elif total == highest:  # Max total so far gives a tie: no winner
                winner = None
        return winner

    def eliminate(self, party):
        """Remove the given party from piles, and redistribute its votes
        among the parties not yet eliminated, according to their preferences.
        If all preferences have already been eliminated, then add the vote to
        the dead list.
        """
        votes = self.piles.pop(party)
        for vote in votes:
            pref = vote.preference(self.piles)
            if pref is not None:
                self.piles[pref].append(vote)
            else:
                self.dead.append(vote)

    def round_loser(self):
        """Return the name of the party to be eliminated in the next round
        of a preferential election."""
        (loser, lowest) = (None, None)
        for (party, total) in self.status().items():
            if loser is None:  # Will only happen in first iteration
                (loser, lowest) = (party, total)
            elif total < lowest:
                (loser, lowest) = (party, total)
            elif total == lowest:
                # Exercise 8: tiebreaking rules
                # first tiebreaker: comparing number of first preferences
                party_first = sum([1 for vote in self.piles[party]
                                   if vote.first_preference() == party])
                loser_first = sum([1 for vote in self.piles[loser]
                                   if vote.first_preference() == loser])
                if party_first < loser_first:
                    (loser, lowest) = (party, total)
                elif party_first == loser_first:
                    # second tiebreaker: alphabetical order
                    if party < loser:
                        (loser, lowest) = (party, total)
        return loser

    def preferential_winner(self):
        """Run a preferential election based on the current piles of votes,
        and return the winning party.
        """
        while len(self.piles) > 1:
            self.eliminate(self.round_loser())
        (winner, votes) = self.piles.popitem()
        # Equivalently: winner = list(self.piles)[0]  # Make list of keys, get first/only element
        # Equivalently: winner = list(self.piles).pop()  # Make list of keys, get last/only element
        # Equivalently: winner = [p for p in self.piles][0]  # Make list of keys, get first/only element
        return winner
