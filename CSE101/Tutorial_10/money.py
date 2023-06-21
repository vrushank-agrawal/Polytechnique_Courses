"""
Created on Wed Nov 11 19:09:37 2020

@author: 123
"""

class Account:
    """A basic savings account.
    Data attributes:
        owner - owners' name (a string)
        IBAN - the accounts' identification number (a string)
        balance - the current amount of money in the account (an integer)
    """
    def __init__(self, owner, IBAN, balance):
        self.owner = owner
        self.IBAN = IBAN
        self.balance = int(balance)
    
    def __str__(self):
        return 'Owner: {}\nIBAN: {}\nbalance: {}'.format(self.owner,self.IBAN,self.balance)

    def __eq__(self, other):
        return self.IBAN==other.IBAN
    
    def deposit(self, amount):
        """Deposits a given amount to the account."""
        if amount<=0: return (False, 'Amount must be positive.')
        self.balance+=amount
        return (True, self.balance)
    
    def withdraw(self, amount):
        """Withdraws a given amount from the account."""
        if amount<=0: return (False, 'Amount must be positive.')
        if amount>self.balance: return (False, 'Insufficient funds.')    
        self.balance-=amount
        return (True, self.balance)
        
class Bank:
    """A simple savings bank.
    Data attributes:
        name - the bank's name
        accounts - a dictionary of accounts, keyed by their IBANs
    """
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.partner_banks = []

    def __str__(self):
        if len(self.accounts)==0:
            return 'Bank {} has no accounts.'.format(self.name)
        temp='Bank {} has the following accounts:\n'.format(self.name)
        temp+='\n\n'.join([str(i) for i in self.accounts.values()])
        return temp
    
    def link_bank(self, bank):
        """Add bank to the list of partner banks."""
        self.partner_banks.append(bank)
        
    def open_account(self, owner, IBAN, balance):
        """Create an account with the given information and add it to 
        the accounts dictionary of the bank.
        If there is already an account with the IBAN at the Bank, do not
        change the accounts dictionary, but return 'IBAN already taken!'.
        """
        for iban in self.accounts:
            if IBAN==iban: return 'IBAN already taken.'
        self.accounts[IBAN]=Account(owner, IBAN, balance)

    def close_account(self, IBAN):
        """Close the account with the given IBAN, print the message
        'The account was closed.', and return its balance.
        If no account in the bank has this IBAN,
        then print 'Account not found!' and return None.
        """
        for iban,acc in self.accounts.items():
            if iban==IBAN:
                print('The account was closed.')
                self.accounts.pop(iban)
                return acc.balance
        return 'Account not found.'

    def holds_account(self, IBAN):
        """True if an account with the given IBAN is held in this bank
        (False otherwise).
        """
        if IBAN in self.accounts: return True
        return False

    def deposit_to(self, IBAN, amount):
        """Deposit the given amount to the account with the given IBAN,
        if it exists (otherwise, print a warning and return None).
        """
        if IBAN not in self.accounts: return (False, 'IBAN not found.')
        return self.accounts[IBAN].deposit(amount)

    def withdraw_from(self, IBAN, amount):
        """Withdraw the given amount from the account with the given IBAN,
        if it exists (otherwise, print a warning and return None).
        """
        if IBAN not in self.accounts: return (False, 'IBAN not found.')
        return self.accounts[IBAN].withdraw(amount)   

    def transfer(self, sender_IBAN, receiver_IBAN, amount):
        """Transfer amount from the sender's to the receiver's accounts."""
        if not self.holds_account(sender_IBAN): return 'Sender not found.'
        if not self.holds_account(receiver_IBAN): return 'Receiver not found.'
        (val, statement) = self.accounts[sender_IBAN].withdraw(amount)
        if val==False: return statement
        self.accounts[receiver_IBAN].deposit(amount)
        return 'Transfer successful.'
    
    def transfer_inter(self, sender_IBAN, receiver_IBAN, amount):
        """Transfer amount from the sender's to the receiver's accounts."""
        if self.holds_account(sender_IBAN) and self.holds_account(receiver_IBAN): 
            return self.transfer(sender_IBAN, receiver_IBAN, amount)
        if not self.holds_account(sender_IBAN): return 'Sender not found.'
        (value, statement) = self.accounts[sender_IBAN].withdraw(amount)
        if value==False: return statement                    #checks if withdrawal is successful
        for bank in self.partner_banks:
            if bank.holds_account(receiver_IBAN):
                bank.deposit_to(receiver_IBAN, amount)
                return 'Transfer successful.'
        self.accounts[sender_IBAN].deposit(amount)
        return 'Receiver not found.'

def create_bank_from_file(filename):
    """Create a bank with name and accounts specified by the given filename."""
    with open(filename, 'r') as bank_file:
        bank_name=bank_file.readline().strip()
        b=Bank(bank_name)
        for line in bank_file:
            temp1=line.strip().split(' ')                       #splits the line into list items
            temp=[value for value in temp1 if value!='']        #removes '' from the list items
            b.accounts[temp[1]] = Account(temp[0], temp[1], temp[2])
        return b

def total_balances(banks):
    """Returns a dictionary of owner:total pairs, where owner ranges
    over all account owners in every bank in the given list of banks,
    and total is the sum of all of that owner's account balances.
    """
    final_money={}
    for bank in banks:
        for iban,acc in bank.accounts.items():
            if acc.owner not in final_money:        #checking for name of person in final_money
                final_money[acc.owner]=0
            final_money[acc.owner]+=acc.balance
    return final_money