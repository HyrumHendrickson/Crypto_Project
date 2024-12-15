from project import Blockchain, time

"""
My final project is designed to teach students about how blockchains
work. it does nothing on its own, it needs to be called and used.
This code imports my final project and calls functions to demostrate
the functionality of the program, if you want to customize inputs, 
check out custom_input.py. 
"""

def run_demo():
    blockchain = Blockchain()

    blockchain.add_transaction("network", "person1", 100)
    blockchain.add_transaction("network", "person2", 50)  

    print("--------------------------------\n")
    blockchain.mine_block("miner1")  # Mine the first block
    print("--------------------------------\n")

    blockchain.add_transaction("person1", "person2", 50)  
    blockchain.add_transaction("person1", "person3", 25)    
    blockchain.add_transaction("person2", "person3", 15)
    blockchain.add_transaction("person3", "person1", 25)

    print("--------------------------------\n")
    blockchain.mine_block("miner2")  # Mine the second block
    print("--------------------------------\n")
    
    blockchain.display_chain()

if __name__ == "__main__":
    run_demo()