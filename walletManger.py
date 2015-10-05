import random

class walletManager:

    wallets = []
    fakePassword = ""

    def __init__(self):
        self.x = 4
        self.password = ""
        
    def generate(self,password):
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
                fakePassword += random.choice(lLetters)
            elif char in uLetters:
                fakePassword += random.choice(uLetters)
            elif char in numbers:
                fakePassword += random.choice(numbers)
            else:
                fakePassword += random.choice(symbols)

    def decrypt(self):
        pass

    def encrypt(self):
        pass


