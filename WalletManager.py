#!/usr/bin/python3

from Crypto.Random import random
import Wallet
import re
from os import path, listdir, rename
from shutil import rmtree
from tempfile import gettempdir

class WalletManager:

    wallets = []
    realIndex = -1
    wallet = None
    NUM_DECOYS = 5

    def __init__(self, wallet_folder_path, wallet_file_base, passwords_file_path, use_passwords_file):
        self.use_passwords_file = use_passwords_file
        self.wallet_folder_path = wallet_folder_path
        self.wallet_file_base = wallet_file_base
        # find the absolute paths for all existing wallets
        self.wallets = []
        filenameRE = r"^" + wallet_file_base + "\d+$"
        for wallet_file in listdir(wallet_folder_path):
            if re.match(filenameRE, wallet_file) != None:
                self.wallets.append(Wallet.Wallet(path.join(wallet_folder_path, wallet_file)))
        # if necessary, read human-made passwords from the given path
        if self.use_passwords_file:
            with open(passwords_file_path) as f:
                self.human_passwords = [line.strip() for line in f.readlines()]
        
    def _generate_decoy_pass(self, password):
        """ Generate a fake password based on the character types in the real password """
        # Arrays of characters to use when generating passwords
        lLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        uLetters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        symbols = ['!','@','#','$','%','^','&','*','(',')','-','_','<','>','?','/']
        
        fake_password = ""
        # Iterate over the given password, building a fake one semi-randomly.
        for char in password:
            if char in lLetters:
                fake_password += random.choice(lLetters)
            elif char in uLetters:
                fake_password += random.choice(uLetters)
            elif char in numbers:
                fake_password += random.choice(numbers)
            else:
                fake_password += random.choice(symbols)

        return fake_password

    def _generate_decoy_pass(self):
        """ Generate a fake password by choosing a real one from the given list. """
        random_index = random.randint(0, len(self.human_passwords) - 1)
        return self.human_passwords[random_index]

    def generate_decoys(self, password):
        """Create empty decoy wallets."""

        assert len(self.wallets) == 1

        for x in range(1, self.NUM_DECOYS + 1):
            new_wallet_path = path.join(self.wallet_folder_path, self.wallet_file_base + str(x))
            new_wallet = Wallet.Wallet(new_wallet_path)
            if self.use_passwords_file:
                decoy_pass = self._generate_decoy_pass()
            else:
                decoy_pass = self._generate_decoy_pass(password)
            binary_password = bytes(decoy_pass, "utf-8")
            new_wallet.encrypt(binary_password)
            self.wallets.append(new_wallet)

        new_real_index = random.randint(1, self.NUM_DECOYS)
        # swap the file names for the real wallet and a random one.
        real_wallet = self.wallets[0]
        real_wallet_path = real_wallet.path
        swap_wallet = self.wallets[new_real_index]
        swap_wallet_path = swap_wallet.path
        rename(swap_wallet_path, path.join(gettempdir(), swap_wallet_path))
        rename(real_wallet_path, swap_wallet_path)
        real_wallet.path = swap_wallet_path
        rename(path.join(gettempdir(), swap_wallet_path), real_wallet_path)
        swap_wallet.path = real_wallet_path

        # swap the wallet objects indices in our list
        self.wallets.insert(new_real_index, self.wallets[0])
        self.wallets.pop(0)
        self.wallets.insert(0, self.wallets[new_real_index])
        self.wallets.pop(new_real_index + 1)

        self.realIndex = new_real_index

    def regenerate_decoys(self, password):
        """Create a new list of decoy wallets based on the real wallet and replace the wallet list with the new list."""

        assert(self.wallet is not None)

        for (i, current_wallet) in enumerate(self.wallets):
            if i == self.realIndex:
                continue # don't overwrite the user's data
            current_wallet.reset()
            # generate fake password for each password in real wallet and insert into decoy
            for website in self.wallet.data:
                for userpass in self.wallet.data[website]:
                    if self.use_passwords_file:
                        decoy_pass = self._generate_decoy_pass()
                    else:
                        decoy_pass = self._generate_decoy_pass(userpass[1])
                    current_wallet.insert(website, userpass[0], decoy_pass)

    def decrypt(self, password):
        """Iterate over the wallets, attempting to decrypt each and returning boolean success."""
        self.realIndex = -1
        for (i, current_wallet) in enumerate(self.wallets):
            if current_wallet.decrypt(password):
                self.realIndex = i
                self.wallet = current_wallet
                return True
        return False

    def encrypt_wallets(self, password):
        """Encrypt all the wallets. The real wallet must be encrypted too
           so the files' last modified times don't give it away."""
        for (i, wallet) in enumerate(self.wallets):
            if i == self.realIndex:
                wallet.encrypt(bytes(password, "utf-8"))
            else:
                if self.use_passwords_file:
                    decoy_pass = self._generate_decoy_pass()
                else:
                    decoy_pass = self._generate_decoy_pass(password)
                binary_password = bytes(decoy_pass, "utf-8")
                wallet.encrypt(binary_password)
        self.realIndex = -1

    def delete(self):
        """Prompt for confirmation then delete all wallet data."""
        response = input("Are you sure you want to delete your wallet? [y/N]")
        if len(response) == 0 or response[0].upper() != 'Y':
            print("Aborting delete operation")
        else:
            rmtree(self.wallet_folder_path)
            print("Wallet deleted (was at " + self.wallet_folder_path + ")")
        return

