import pytest
from project import Blockchain, time

"""
The purpose of my project is to be a tool to teach students about 
blockchains. Setting up a real blockchain is very complicated, my code is only a simple example. 
All of the test functions pass, but its not a secure form of currency. There are many 
security gaps that wouldnt be present in a real blockchain, but fixing them would
make the code to complex for beginers.
"""

def set_up_blockchain():
    # Setup the blockchain with initial transactions for Person1 and Person2
    blockchain = Blockchain()
    blockchain.add_transaction("network", "Person1", 100)  # Give Person1 initial coins
    blockchain.add_transaction("network", "Person2", 50)    # Give Person2 initial coins
    return blockchain

def test_initial_balance(blockchain):
    # Test initial balances of Person1, Person2, Person3, Miner1, and Miner2
    assert blockchain.get_balance("Person1") == 100
    assert blockchain.get_balance("Person2") == 50
    assert blockchain.get_balance("Person3") == 0
    assert blockchain.get_balance("Miner1") == 0
    assert blockchain.get_balance("Miner2") == 0
    print("test_initial_balance passed")

def test_add_transaction_valid(blockchain):
    # Test valid transactions between Person1 and Person2
    blockchain.add_transaction("Person1", "Person2", 20)
    assert blockchain.get_balance("Person1") == 80
    assert blockchain.get_balance("Person2") == 70

    # Test valid transactions between Person2 and Person3
    blockchain.add_transaction("Person2", "Person3", 15)
    assert blockchain.get_balance("Person2") == 55
    assert blockchain.get_balance("Person3") == 15
    print("test_add_transaction_valid passed")

def test_mining(blockchain):
    # Test mining a block by Miner1
    miner1 = "Miner1"

    blockchain.mine_block(miner1)
    assert len(blockchain.chain) == 2  # there should be 2 blocks, the initial block and the block that was just mined
    assert blockchain.get_balance(miner1) > 0  # Miner1 should receive a reward

    # Test mining a block by Miner2
    miner2 = "Miner2"
    blockchain.mine_block(miner2)
    assert len(blockchain.chain) == 3  # Another block should be mined
    assert blockchain.get_balance(miner2) > 0  # Miner2 should receive a reward
    print("test_mining passed")

def test_balance_after_multiple_transactions(blockchain):
    # Test multiple transactions and ensure balances are updated correctly
    print(blockchain.display_balances())
    blockchain.add_transaction("Person1", "Person2", 20)
    blockchain.add_transaction("Person2", "Person3", 15)
    blockchain.add_transaction("Person1", "Person3", 10)
    print(blockchain.display_balances())
    assert blockchain.get_balance("Person1") == 50
    assert blockchain.get_balance("Person2") == 60
    assert blockchain.get_balance("Person3") == 40
    print("test_balance_after_multiple_transactions passed")
    
def test_mining_time(blockchain):
    # Test the mining time to ensure it completes
    start_time = time.time()
    blockchain.mine_block("Miner1")
    mining_time = time.time() - start_time
    assert mining_time < 5  # Mining should take less than 5 seconds
    start_time = time.time()
    blockchain.mine_block("Miner2")
    mining_time = time.time() - start_time
    assert mining_time < 5  # Mining should take less than 5 seconds
    print("test_mining_time passed")

def run_all_tests():
    
    # makes the blockchain object
    blockchain = set_up_blockchain()
    
    # Manually calling all test functions
    test_initial_balance(blockchain)
    test_add_transaction_valid(blockchain)
    test_mining(blockchain)
    test_balance_after_multiple_transactions(blockchain)
    test_mining_time(blockchain)
    
    print("--------All tests passed!--------")

if __name__ == "__main__":
    run_all_tests()
