#!/usr/bin/python3

__author__ = 'jason'

import Crypto.Random
from Crypto.Cipher import AES
import hashlib

class Wallet:

    # size (in bytes) of the random salt to be appended to the password
    SALT_SIZE = 16
    # data to encrypt must be a multiple of this many bytes
    AES_BLOCK_SIZE = 16
    
    def __init__(self):
        """initialize wallet with empty dictionary
            data uses form {website: [(username, password)]}
        """
        self.data = {}

    def insert(self, site, user, password):
        """Insert a new entry into the wallet by adding to "data" dictionary

            if website key already exists, add to the list
            if user already exists, error
            else create new dictionary entry

            params:
            site - string representing website name i.e. "www.google.com"
            user - string representing desired username
            password - string representing desired password  TODO: possibly create password strength requirements?
        """
        if site in self.data:
            for tuple in self.data[site]:
                if tuple[0] == user:
                    print("Username '" + user + "' already exists for website '" + site + "'")
                    return
            self.data[site].append((user, password))
        else:
            self.data[site] = [(user, password)]

    def removeUser(self, site, user):
        """Remove entry from the wallet by taking out an entry from the list of user, password pairs
            if list becomes empty, remove dictionary entry entirely
            if user doesn't exist for specified website, error

            params:
            site - string representing website name i.e. "www.google.com"
            user - string representing existing username to be removed
        """
        if site not in self.data:
            print("Invalid website, '" + site + "' is not in wallet")
            return

        removeFlag = False
        for tuple in self.data[site]:
            if tuple[0] == user:
                self.data[site].remove(tuple)
                removeFlag = True
                break

        if not removeFlag:
            print("Invalid username, '" + user + "' is not in wallet")

        if len(self.data[site]) == 0:
            del self.data[site]

    def removeSite(self, site):
        """Remove all entries for a given website by deleting dictionary entry

            params:
            site - string representing website name i.e. "www.google.com"
        """
        if site in self.data:
            del self.data[site]
        else:
            print("Invalid website, '" + site + "' is not in wallet")

    def updateUser(self, site, oldUser, newUser):
        """Change a username for a given website
            if user doesn't exist for specified website, error

            params:
            site - string representing website name i.e. "www.google.com"
            oldUser - string representing existing username to be updated
            newUser - string representing desired username
        """
        if site not in self.data:
            print("Invalid website, '" + site + "' is not in wallet")
            return

        updateFlag = False
        for tuple in self.data[site]:
            if tuple[0] == oldUser:
                newTuple = (newUser, tuple[1])
                self.data[site].remove(tuple)
                self.data[site].append(newTuple)
                udpateFlag = True
                break

        if not udpateFlag:
            print("Invalid username, '" + oldUser + "' is not in wallet")

    def updatePass(self, site, user, newPass):
        """Change a password for a given website and username
            if user doesn't exist for specified website, error

            params:
            site - string representing website name i.e. "www.google.com"
            user - string representing existing username
            newPass - string representing desired password
        """
        if site not in self.data:
            print("Invalid website, '" + site + "' is not in wallet")
            return

        updateFlag = False
        for tuple in self.data[site]:
            if tuple[0] == user:
                newTuple = (user, newPass)
                self.data[site].remove(tuple)
                self.data[site].append(newTuple)
                udpateFlag = True
                break

        if not udpateFlag:
            print("Invalid username, '" + user + "' is not in wallet")

    def printWallet(self):
        """print the entire wallet to console"""
        #TODO: better formatting
        print(str(self.data))
        print()

    def _generate_key(self, password, salt, iterations):
        """Given a binary password and salt, repeatedly take the 
        SHA-256 sum iterations number of times."""
        assert iterations > 0
        key = password + salt
        for i in range(iterations):
            key = hashlib.sha256(key).digest()
        return key

    def _pad_data(self, data, multiple):
        """Given binary data, pad it with bytes so that it's
        a multiple of AES_BLOCK_SIZE (even if it already is).
        The padding character has the value of the number of padding bytes."""
        extra_bytes = len(data) % multiple
        padding_size = multiple - extra_bytes
        padding = chr(padding_size) * padding_size
        padded_data = data + bytes(padding, 'utf-8')
        return padded_data

    def _unpad_data(self, data):
        """Given binary data, remove the padding applied by _pad_data."""
        padding_size = data[-1]
        original_data = data[:-padding_size]
        return original_data

    def _encrypt_data(self, plaintext, password, number_iterations):
        """Given binary data (with the user's websites, usernames, and passwords),
        encrypt it using AES by salting the given password and hashing it repeatedly."""
        salt = Crypto.Random.get_random_bytes(self.SALT_SIZE)
        key = self._generate_key(password, salt, number_iterations)
        cipher = AES.new(key, AES.MODE_ECB)
        padded_plaintext = self._pad_data(plaintext, self.AES_BLOCK_SIZE)
        ciphertext = cipher.encrypt(padded_plaintext)
        ciphertext_with_salt = salt + ciphertext
        return ciphertext_with_salt

    def _decrypt_data(self, ciphertext, password, number_iterations):
        """Given encrypted binary data, decrypt it using the given password 
        (reverse the process in _encrypt_data)."""
        salt = ciphertext[:self.SALT_SIZE]
        original_ciphertext = ciphertext[self.SALT_SIZE:]
        key = self._generate_key(password, salt, number_iterations)
        cipher = AES.new(key, AES.MODE_ECB)
        padded_plaintext = cipher.decrypt(original_ciphertext)
        plaintext = self._unpad_data(padded_plaintext)
        return plaintext

    def encrypt(self, key, outFile):
        """Encrypt data and save to disk at location outFile"""
        #TODO call _encrypt_data
        #TODO write to disk
        pass

    def decrypt(self, key, inFile):
        """Decrypt data from inFile and load into data"""
        #TODO call _decrypt_data
        #TODO write to disk
        pass

