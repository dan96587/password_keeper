#!/usr/bin/python3

from Crypto.Random import random
from random import randint
import Wallet
import re
from os import path, listdir
from shutil import rmtree

class WalletManager:

    wallets = []
    realIndex = -1
    wallet = None
    NUM_DECOYS = 5

    def __init__(self, wallet_folder_path, wallet_file_base):
        self.wallet_folder_path = wallet_folder_path
        # find the absolute paths for all existing wallets
        self.wallets = []
        filenameRE = r"^" + wallet_file_base + "\d+$"
        for wallet_file in listdir(wallet_folder_path):
            if re.match(filenameRE, wallet_file) != None:
                self.wallets.append(path.join(wallet_folder_path, wallet_file))
        
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

    def generate_decoy_wallets(self):
        """Create a new list of decoy wallets based on the real wallet and replace the wallet list with the new list."""
        if self.wallet is None:
            print("Error, wallet not decrypted")
            return

        newWallets = []
        for x in range(self.NUM_DECOYS):
            newWallets.append(Wallet.Wallet(self.create_wallet_path()))

        # generate fake password for each password in real wallet and insert into decoy wallets
        for website in wallet.data:
            for userpass in wallet.data[website]:
                for curWallet in newWallets:
                    curWallet.insert(website, userpass[0], self._generate_decoy_pass(userpass[1]))

        # insert real wallet into random position in wallet list
        newWallets.insert(randint(0,self.NUM_DECOYS), self.wallet)
        self.wallets = newWallets

    def create_wallet_path(self):
        """Create a random file path for a new wallet."""
        #TODO
        pass

    def decrypt(self, password):
        """Iterate over the wallets, attempting to decrypt each and returning boolean success."""
        self.realIndex = -1
        for (i, wallet_path) in enumerate(self.wallets):
            wallet = Wallet.Wallet(wallet_path)
            if wallet.decrypt(password):
                self.realIndex = i
                self.wallet = wallet
                break
        if self.realIndex == -1:
            return False
        else:
            return True

    def delete(self):
        """Prompt for confirmation then delete all wallet data."""
        response = input("Are you sure you want to delete your wallet? [y/N]")
        if len(response) == 0 or response[0].upper() != 'Y':
            print("Aborting delete operation")
        else:
            rmtree(self.wallet_folder_path)
            print("Wallet deleted (was at " + self.wallet_folder_path + ")")
        return

