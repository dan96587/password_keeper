#!/usr/bin/python3

__author__='mleeds95'

import Wallet
import WalletManager
import configparser
from sys import exit
from os import path, mkdir, listdir
import re
from shutil import rmtree

CONFIG_FILE = "config.ini"

def main():
    """
    This is the main user interface that allows users to manage their
    wallet (each of which holds website, username, and password tuples).
    """

    # First, read the config file
    global config
    config = configparser.ConfigParser()
    try:
        configFile = open(CONFIG_FILE)
    except FileNotFoundError:
        print("Error: Configuration file " + CONFIG_FILE + " missing.")
        exit(1)
    config.read_file(configFile)

    # Make a folder for wallet data if it doesn't exist.
    wallet_folder_path = path.expanduser(config.get("FILESYSTEM", "WalletFolder"))
    if not path.isdir(wallet_folder_path):
        mkdir(wallet_folder_path)

    # Make an empty wallet if none exist.
    full_paths = []
    if len(listdir(wallet_folder_path)) == 0:
        print("Creating a new password wallet...")
        wallet_filename = config.get("FILESYSTEM", "WalletFile") + "0"
        wallet_path = path.join(wallet_folder_path, wallet_filename)
        wallet = Wallet.Wallet(wallet_path)
        password = input("Enter a master password:")
        binary_password = bytes(password, 'utf-8')
        wallet.encrypt(binary_password)
        #TODO generate decoy wallets and randomize the files' names
        print("Encrypted wallet data written to disk.")
        full_paths.append(wallet_path)
        del wallet, password, binary_password
    else:
        # find the absolute paths for all existing wallets
        for wallet_file in listdir(wallet_folder_path):
            filenameRE = r"^" + config.get("FILESYSTEM", "WalletFile") + "\d+$"
            if re.match(filenameRE, wallet_file) != None:
                full_paths.append(path.join(wallet_folder_path, wallet_file))

    # Initialize the wallet manager with the paths above.
    walletManager = WalletManager.WalletManager(full_paths)

    # Now attempt to decrypt existing wallets
    decryption_success = False
    print("Decrypting password data...")
    while not decryption_success:
        password = input("Enter your master password:")
        binary_password = bytes(password, 'utf-8')
        decryption_success = walletManager.decrypt(binary_password)
    del password, binary_password

    print("Welcome to password_keeper. Type 'help' for a list of commands or 'exit' to exit.")
    while True:
        # Prompt for input
        print(">", end="")
        try:
            user_input = input()
        except EOFError:
            print()
            break
        # Process command
        if user_input == "exit":
            break
        elif user_input == "help":
            print_help()
            continue
        elif user_input == "read":
            read_wallet()
            continue
        elif user_input == "delete":
            delete_wallet()
            continue
        elif user_input == "update":
            update_wallet()
            continue
        else:
            print_help()
            continue
    return

def print_help():
    print()
    print("Usable commands:\n")
    print("help -- print a list of commands")
    print("exit -- exit password_keeper")
    print("read -- read website/password data")
    print("delete -- delete all your data")
    print("update -- update website/password data")
    print()

def read_wallet():
    pass
    #TODO

def delete_wallet():
    global config
    response = input("Are you sure you want to delete your wallet? [y/N]")
    if len(response) == 0 or response[0].upper() != 'Y':
        print("Aborting delete operation")
        return
    else:
        wallet_folder_path = path.expanduser(config.get("FILESYSTEM", "WalletFolder"))
        rmtree(wallet_folder_path)
        print("Wallet deleted (was at " + wallet_folder_path + ")")
        return

def update_wallet():
    pass
    #TODO


if __name__=='__main__':
    main()

