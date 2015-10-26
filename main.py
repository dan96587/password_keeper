#!/usr/bin/python3

__author__='mleeds95'

import Wallet
import WalletManager
import configparser
from sys import exit
from os import path, mkdir, listdir

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
    password = ""
    full_paths = []
    wallet_file_base = config.get("FILESYSTEM", "WalletFile")
    if len(listdir(wallet_folder_path)) == 0:
        print("Creating a new password wallet...")
        wallet_filename = wallet_file_base + "0"
        wallet_path = path.join(wallet_folder_path, wallet_filename)
        wallet = Wallet.Wallet(wallet_path)
        password = input("Enter a master password:")
        binary_password = bytes(password, "utf-8")
        wallet.encrypt(binary_password)
        print("Encrypted wallet data written to disk.")

    # Initialize the wallet manager with the wallet folder and base file name
    walletManager = WalletManager.WalletManager(wallet_folder_path, wallet_file_base)
    if len(walletManager.wallets) == 1:
        walletManager.generate_decoys(password)
        walletManager.encrypt_decoys(password)

    # Now attempt to decrypt existing wallets
    decryption_success = False
    print("Decrypting password data...")
    while not decryption_success:
        password = input("Enter your master password:")
        binary_password = bytes(password, "utf-8")
        decryption_success = walletManager.decrypt(binary_password)

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
        elif user_input.split()[0] == "print":
            if len(user_input.split()) != 2:
                print("Usage: print <website url>|all")
            else:
                walletManager.wallet.print_site_data(user_input.split()[1])
            continue
        elif user_input.split()[0] == "add":
            if len(user_input.split()) != 4:
                print("Usage: add <website url> <username> <password>")
            else:
                walletManager.wallet.insert(user_input.split()[1], user_input.split()[2], user_input.split()[3])
                walletManager.regenerate_decoys(password)
            continue
        elif user_input.split()[0] == "delete":
            if len(user_input.split()) != 2:
                print("Usage: delete <website url>|all")
            elif user_input.split()[1] == "all":
                walletManager.delete()
                break # exit
            else:
                walletManager.wallet.remove_site(user_input.split()[1])
                walletManager.regenerate_decoys(password)
            continue
        elif user_input.split()[0] == "update":
            if len(user_input.split()) != 5:
                print("Usage: update user|pass <site> <user> <new user/pass>")
            elif user_input.split()[1] == "user":
                walletManager.wallet.update_user(user_input.split()[2], user_input.split()[3], user_input.split()[4])
                walletManager.regenerate_decoys(password)
            elif user_input.split()[1] == "pass":
                walletManager.wallet.update_pass(user_input.split()[2], user_input.split()[3], user_input.split()[4])
                walletManager.regenerate_decoys(password)
            else:
                print("Usage: update user|pass <site> <user> <new user/pass>")
            continue
        elif user_input == "save":
            walletManager.wallet.encrypt(binary_password)
            walletManager.encrypt_decoys(password)
            break
        else:
            print_help()
            continue
    return

def print_help():
    print()
    print("Usable commands:\n")
    print("help -- print a list of commands")
    print("exit -- exit password_keeper")
    print("print <website url>|all -- print username/password pair(s) for the given site, or all to stdout")
    print("add <website url> <username> <password> -- add a username/password pair to the stored data")
    print("delete <website url>|all -- delete a specific site's data or all your data")
    print("update user|pass <site> <user> <new user/pass> -- update website/password data")
    print("save -- save changes to the disk and exit")
    print()

if __name__=="__main__":
    main()

