#!/usr/bin/python3

from Crypto.Random import random
import Wallet

class WalletManager:

    wallets = []
    realIndex = -1

    def __init__(self, wallet_paths):
        self.wallets = wallet_paths
        self.x = 4
        
    def _generate_decoy_pass(self, password):
        """Generate a fake password based on the character types in a real password"""

        # Arrays of characters to use when generating passwords
        lLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        uLetters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        symbols = ['!','@','#','$','%','^','&','*','(',')','-','_','<','>','?','/']
        
        fakePassword = ""
        # Iterate over the given password, building a fake one semi-randomly.
        for char in password:
            if char in lLetters:
                fakePassword += random.choice(lLetters)
            elif char in uLetters:
                fakePassword += random.choice(uLetters)
            elif char in numbers:
                fakePassword += random.choice(numbers)
            else:
                fakePassword += random.choice(symbols)

        return fakePassword

    def decrypt(self, password):
        self.realIndex = -1
        for (i, wallet_path) in enumerate(self.wallets):
            wallet = Wallet.Wallet(wallet_path)
            if wallet.decrypt(password):
                self.realIndex = i
                break
        if self.realIndex == -1:
            return False
        else:
            return True

    def encrypt(self, password):
        #TODO
        pass


