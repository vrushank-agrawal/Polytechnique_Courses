#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: adinamarlenapanchea
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
        self.balance = balance

    def __str__(self):
        res = 'Owner: {}\nIBAN: {}\nbalance: {}'.format(
            self.owner,
            self.IBAN,
            self.balance)
        return res

    def __eq__(self, other):
        return self.IBAN == other.IBAN

    def deposit(self, amount):
        """Deposits a given amount to the account."""
        if amount <= 0:
            return (False, 'Amount must be positive.')
        self.balance += amount
        return (True, self.balance)

    def withdraw(self, amount):
        """Withdraw a given amount to the account."""
        if amount <= 0:
            return (False, 'Amount must be positive.')
        elif self.balance < amount:
            return (False, 'Insufficient funds.')
        self.balance -= amount
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
        self.partners = []

    def __str__(self):
        """Return string representation of the entire bank"""
        if self.accounts == {}:
            return 'Bank {} has no accounts.'.format(self.name)
        res = 'Bank {} has the following accounts:\n'.format(self.name)
        res += '\n\n'.join([str(acct) for acct in self.accounts.values()])
        return res

    def link_bank(self, bank):
        """Add bank to the list of partner banks."""
        self.partners.append(bank)

    def open_account(self, owner, IBAN, balance):
        """Create an account with the given information and add it to
        the accounts dictionary of the bank.
        If there is already an account with the IBAN at the Bank, do not
        change the accounts dictionary, but return 'IBAN already taken!'.
        """
        if IBAN in self.accounts:
            return 'IBAN already taken!'
        self.accounts[IBAN] = Account(owner, IBAN, balance)

    def close_account(self, IBAN):
        """Close the account with the given IBAN, print the message
        'The account was closed.', and return its balance.
        If no account in the bank has this IBAN,
        then print 'Account not found!' and return None.
        """
        if IBAN not in self.accounts:
            print('Account not found!')
            return None
        account = self.accounts.pop(IBAN)
        print('The account was closed!')
        return account.balance

    def holds_account(self, IBAN):
        """True if an account with the given IBAN is held in this bank
        (False otherwise).
        """
        return IBAN in self.accounts

    def get_balance(self, IBAN):
        """The current balance of the account with the given IBAN,
        or None if that account is not held in this bank.
        """
        if not self.holds_account(IBAN):
            return None
        return self.accounts[IBAN].balance

    def deposit_to(self, IBAN, amount):
        """Deposit the given amount to the account with the given IBAN,
        if it exists (otherwise, print a warning and return None).
        """
        if not self.holds_account(IBAN):
            return (False, 'IBAN not found.')
        return self.accounts[IBAN].deposit(amount)

    def withdraw_from(self, IBAN, amount):
        """Withdraw the given amount from the account with the given IBAN,
        if it exists (otherwise, print a warning and return None).
        """
        if not self.holds_account(IBAN):
            return (False, 'IBAN not found.')
        return self.accounts[IBAN].withdraw(amount)

    def transfer(self, sender_IBAN, receiver_IBAN, amount):
        """Transfer amount from the sender's to the receiver's accounts."""
        if not self.holds_account(sender_IBAN):
            return 'Sender not found.'
        receiver_bank = None
        if self.holds_account(receiver_IBAN):
            receiver_bank = self
        else:
            for bank in self.partners:
                if bank.holds_account(receiver_IBAN):
                    receiver_bank = bank
                    break
        if receiver_bank is None:
            return 'Receiver not found.'
        (ok, message) = self.withdraw_from(sender_IBAN, amount)
        if not ok:
            return message
        (ok, message) = receiver_bank.deposit_to(receiver_IBAN, amount)
        if not ok:  # should never occur...
            return message
        return 'Transfer successful.'

def create_bank_from_file(filename):
    """Create a bank with name and accounts specified by the given filename."""
    with open(filename) as file:
        bank_line = file.readline().strip()
        bank = Bank(bank_line)
        for line in file:
            (owner, iban, balance) = line.strip().split()
            bank.accounts[iban] = Account(owner, iban, int(balance))
        return bank

def total_balances(banks):
    """Returns a dictionary of owner:total pairs, where owner ranges
    over all of the account owners in all of the banks, and total is
    the sum of all of that owner's account balances.
    """
    totals = {}
    for bank in banks:
        for account in bank.accounts.values():
            if account.owner not in totals:
                totals[account.owner] = account.balance
            else:
                totals[account.owner] += account.balance
    return totals
