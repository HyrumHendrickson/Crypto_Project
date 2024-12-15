from project import Blockchain, time

"""
My final project is designed to teach students about how blockchains work. It does nothing on its own,
its meant to be called and used by other programs. This file is desinged to demo how the final 
project works, it imports and calls the blockchain object and allows you to dirrectly call 
functions of the program. You can use this file to test the code yourself to see how it works. 
If you want to just see example inputs to the function, go to run_this_code.py
"""

def run_demo():
    blockchain = Blockchain()

    while True:
        command = input(">>>")
        if(command == "exit"):
            break
        elif(command == "help"):
            print("Available commands:")
            print("help")
            print("exit")
            print("add-person")
            print("add-transaction")
            print("mine-block")
            print("display-chain")
            print("display-balances")
        elif(command == "add-person"):
            name = input("Enter the name of the person: ")
            blockchain.add_transaction("network", name, 100)
        elif(command == "add-transaction"):
            sender = input("Enter the sender's name: ")
            recipient = input("Enter the recipient's name: ")
            amount = float(input("Enter the transaction amount: "))
            blockchain.add_transaction(sender, recipient, amount)
        elif(command == "mine-block"):
            start_time = time.time()
            blockchain.mine_block("miner")  # Miner1 mines a block
            print(f"Block mined by {"miner"} (Time: {time.time() - start_time:.2f} seconds)")
        elif(command == "display-chain"):
            blockchain.display_chain()
        elif(command == "display-balances"):
            blockchain.display_balances()
        else:
            print("Invalid command. Type 'help' for a list of available commands.")

if __name__ == "__main__":
    run_demo()