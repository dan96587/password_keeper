#!/usr/bin/python3

__author__ = 'jason'


class Wallet:
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

    def encrypt(self, key, outFile):
        """Encrypt data and save to disk at location outFile"""

    def decrypt(self, key, inFile):
        """Decrypt data from inFile and load into data"""
