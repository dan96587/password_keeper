#!/usr/bin/python3

from Crypto.Random import random

class WalletManager:

    wallets = []
    fakePassword = ""
    realIndex = -1

    def __init__(self):
        self.x = 4
        self.password = ""
        
    def generate(self, password):
        """Generate fake passwords and use them to fill wallets"""

        #Arrays of characters to use when generating passwords
        lLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        uLetters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        symbols = ['!','@','#','$','%','^','&','*','(',')','-','_','<','>','?','/']
        
        
        #Initialize self.password to the password input
        self.password = password

        #Look through an input string 
        #Make fake passwords using a random function and the lists above
        #For every wallet create N fake passwords

        for char in password:
            if char in lLetters:
                self.fakePassword += random.choice(lLetters)
            elif char in uLetters:
                self.fakePassword += random.choice(uLetters)
            elif char in numbers:
                self.fakePassword += random.choice(numbers)
            else:
                self.fakePassword += random.choice(symbols)

    def decrypt(self, password):
        realIndex = -1
        for (i, wallet) in enumerate(wallets):
            if wallet.decrypt(password):
                self.realIndex = i
        if realIndex == -1:
            return False
        else:
            return True

    def encrypt(self, password):
        #TODO
        pass


