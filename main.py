#!/usr/bin/python3

__author__='mleeds95'

import Wallet
import WalletManager

def main():
    """
    This is the main user interface that allows users to manage their
    wallets (each of which holds website, username, and password tuples).
    """
    #TODO decrypt data
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
        elif user_input == "list":
            list_wallets()
            continue
        elif user_input == "add":
            add_wallet()
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
    print("list -- list all wallets")
    print("add -- add a wallet")
    print("delete -- delete a wallet")
    print("update -- update a wallet")
    print()

def list_wallets():
    pass
    #TODO

def add_wallet():
    pass
    #TODO

def delete_wallet():
    pass
    #TODO

def update_wallet():
    pass
    #TODO


if __name__=='__main__':
    main()

