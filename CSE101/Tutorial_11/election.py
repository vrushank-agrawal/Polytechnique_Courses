# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:40:29 2020

@author: 123
"""

class Vote:
    """A single vote object.
    Data attributes:
    - preference_list: a list of the preferred parties for this voter,
      in descending order of preference.
    """
    def __init__(self, preference_list):
        self.preference_list=preference_list
        
    def __str__(self):
        if self.preference_list==[]: 
            return 'Blank'
        return ' > '.join(self.preference_list)
        
    def __repr__(self):
        return 'Vote({})'.format(self.preference_list)
    
    def first_preference(self):
        if self.preference_list==[]: 
            return None
        return self.preference_list[0]
    
    def preference(self, names):
        """Return the item in names that occurs first in the preference list,
        or None if no item in names appears.
        """
        for party in self.preference_list:
            if party in names:
                return party
        return None
        
    
class Election:
    """A basic election class.
    
    Data attributes:
    - parties: a list of party names
    - blank: a list of blank votes
    - piles: a dictionary with party names for keys
      and lists of votes (allocated to the parties) for values
    - dead: list of dead votes
    """
    
    def __init__(self, parties):
        self.parties = parties
        self.blank = []
        self.piles = {name:[] for name in self.parties}
        self.dead = []
    
    
    def add_vote(self, vote):
        """Append the vote to the corresponding pile."""
        party=vote.first_preference()
        if party in self.piles: 
            self.piles[party].append(vote)
        else: 
            self.blank.append(vote)
        
        
    def status(self):
        """Return the current status of the election:
        a dictionary mapping each of the party names in the piles
        to the number of votes in their pile.
        """
        return {i: len(j) for i,j in self.piles.items()}
    
    
    def add_votes_from_file(self, filename):
        """Append each of the votes in the file to the correct pile."""
        with open (filename, 'r') as f1:
            for line in f1.readlines():
                if line == '\n': 
                    vote=Vote([])
                else: 
                    vote=Vote(line.strip().split(' '))
                self.add_vote(vote)
    
    
    def first_past_the_post_winner(self):
        """Return the winner of this election under
        the first-past-the-post system, or None if
        the election is tied.
        """
        temp=(None, -1)
        for i,j in self.piles.items():
            if temp[1]<len(j): 
                temp=(i, len(j))
            elif temp[1]==len(j): 
                temp=(None, len(j))
        return temp[0]
    
    
    def weighted_status(self):
        """
        Returns a dictionary with keys being the parties
        and the values being the number of points 
        (counted using the weighted scheme) they got
        """
        dict_weight_votes={party:0 for party in self.parties}
        for party,votes in self.piles.items():
            for lst in votes:
                for pos,vote in enumerate(lst.preference_list):
                    dict_weight_votes[vote]+=(5-pos)
        return dict_weight_votes


    def weighted_winner(self):
        """
        Return the winner of this election under
        the weighted voting scheme.
        """
        weight_list=[(-j,i) for i,j in self.weighted_status().items()]
        return sorted(weight_list)[0][1]

    
    def eliminate(self, party):
        """Remove the given party from piles, and redistribute its 
        votes among the parties not yet eliminated, according to 
        their preferences.  If all preferences have been eliminated, 
        then add the vote to the dead list.
        """
        vote_lists=self.piles.pop(party)
        for i in vote_lists:
            new_party=i.preference(self.piles)
            if new_party == None: 
                self.dead.append(i)
            else: 
                self.piles[new_party].append(i)


    def round_loser(self):
        """Return the name of the party to be eliminated from the next round."""
        # party_vote_list=[(j,i) for i,j in self.status().items()]
        # new_list=sorted(party_vote_list)
        # final_list=new_list.copy()
        # for i in range(len(new_list)-1):
        #     if new_list[i][0]==new_list[i+1][0]:
        #         i_firsts = [k for k in self.piles[new_list[i][1]] if k.first_preference()==new_list[i][1]]
        #         i_1_firsts = [k for k in self.piles[new_list[i+1][1]] if k.first_preference()==new_list[i+1][1]]
        #         if len(i_firsts)<len(i_1_firsts):
        #             final_list.remove(new_list[i])
        #         elif len(i_firsts)>len(i_1_firsts):
        #             final_list.remove(new_list[i+1])
        #         elif len(i_firsts)==len(i_1_firsts):
        #             temp_list=[(-i,j) for (i,j) in new_list]
        #             final_list.remove(sorted(temp_list, reverse=True)[-1])
        # return final_list[0][1]
        t=(None,None)
        for i,j in self.status().items():
            if t[0] == None or j < t[1]: 
                t=(i, j)
            elif j==t[1]:
                j_firsts = [k for k in self.piles[i] if k.first_preference()==i]
                t_firsts = [k for k in self.piles[t[0]] if k.first_preference()==t[0]]
                if len(j_firsts)==len(t_firsts):
                    if i<t[0]: 
                        t=(i,j)
                elif len(j_firsts)<len(t_firsts):
                    t = (i,j)
        return t[0]
    
    
    def preferential_winner(self):
        """Run a preferential election based on the current piles of votes,
        and return the winning party.
        """
        while  len(self.piles)>1:
            self.eliminate(self.round_loser())
        return (self.piles.popitem())[0]

            
  