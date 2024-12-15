import hashlib
import time
import random

"""
This program is a simplified example of how a real blockchain works, 
it does not do everything that a real blockchain would. The purpose is to use simple 
examples to teach students about blockchain technology without getting to far into the weeds.

This program does nothing by itself, its meant to be imported and used by other files.
I included an example file in this submission, the example file imports this code and
calls functions to allows you to see how it works. its called, run_this_code.py
"""

# Represents a transaction in the blockchain
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender  # Address of the sender
        self.receiver = receiver  # Address of the receiver
        self.amount = amount  # Amount of cryptocurrency being transferred

    def __repr__(self):
        return f"{self.sender} -> {self.receiver} : {self.amount} coins"

# Represents a block in the blockchain
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof, hash_value):
        self.index = index  # Position of the block in the chain
        self.previous_hash = previous_hash  # Hash of the previous block
        self.timestamp = timestamp  # Time of block creation
        self.transactions = transactions  # List of transactions in the block
        self.proof = proof  # Proof of work for the block
        self.hash = hash_value  # Hash of the current block

    def __repr__(self):
        return (
            f"Block #{self.index}\n"
            f"  Previous Hash: {self.previous_hash}\n"
            f"  Timestamp: {self.timestamp}\n"
            f"  Transactions: {self.transactions}\n"
            f"  Proof: {self.proof}\n"
            f"  Hash: {self.hash}\n"
        )
    
# Represents the blockchain itself
class Blockchain:
    def __init__(self):
        self.chain = []  # List of blocks forming the blockchain
        self.current_transactions = []  # List of pending transactions
        self.balances = {}  # Dictionary to track account balances
        self.create_genesis_block()  # Initializes the blockchain with a genesis block

    # Creates the first block in the blockchain
    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            previous_hash="0",
            timestamp=self.current_timestamp(),
            transactions=[],
            proof=100,  # Arbitrary proof for the genesis block
            hash_value="0",  # Initial hash for the genesis block
        )
        self.chain.append(genesis_block)

    # Adds a transaction to the list of pending transactions
    def add_transaction(self, sender, receiver, amount):
        sender_balance = self.get_balance(sender)  # Check sender's balance
        if sender_balance < amount and sender != "network":
            raise ValueError(f"Insufficient balance. {sender} has {sender_balance} but tried to send {amount}")

        transaction = Transaction(sender, receiver, amount)

        # Update balances
        if sender != "network":
            self.balances[sender] = self.balances.get(sender, 0) - amount
        self.balances[receiver] = self.balances.get(receiver, 0) + amount

        self.current_transactions.append(transaction)
        print(f"Transaction added: {transaction}")

    # Mines a new block for the chain
    def mine_block(self, miner_address):
        self.add_transaction("network", miner_address, 10)  # Reward miner with coins

        last_block = self.chain[-1]  # Get the last block in the chain
        proof = self.proof_of_work(last_block.proof)  # Perform proof of work

        new_block = Block(
            index=len(self.chain),
            previous_hash=last_block.hash,
            timestamp=self.current_timestamp(),
            transactions=self.current_transactions.copy(),
            proof=proof,
            hash_value=""
        )
        new_block.hash = self.calculate_hash(new_block)  # Calculate block hash

        self.chain.append(new_block)  # Add the new block to the chain
        self.current_transactions.clear()  # Clear pending transactions
        print(f"Block mined successfully: {new_block}")
        return new_block

    # Implements the proof of work algorithm [this is not how a real blockchain would do it]
    def proof_of_work(self, last_proof):
        print("Starting proof of work...")
        proof = random.randint(1000, 9999)  # Start with a random proof
        while not self.valid_proof(last_proof, proof):
            proof = random.randint(1000, 9999)  # Try a new proof
        print(f"Proof of work found: {proof}")
        return proof

    # Validates the proof of work
    def valid_proof(self, last_proof, proof):
        guess = f"{last_proof}{proof}".encode()  # encode proofs
        guess_hash = hashlib.sha256(guess).hexdigest()  # Generate hash
        return guess_hash[:2] == "00"  # Check if hash meets difficulty

    # Calculates the hash for a block
    def calculate_hash(self, block):
        block_string = f"{block.index}{block.previous_hash}{block.timestamp}{block.transactions}{block.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    # Returns the current timestamp
    def current_timestamp(self):
        return int(time.time())

    # Retrieves the balance of a given address
    def get_balance(self, address):
        return self.balances.get(address, 0)

    # Displays the entire blockchain
    def display_chain(self):
        print("Blockchain Ledger:")
        for block in self.chain:
            print(block)

    # Displays the current account balances
    def display_balances(self):
        print("\nCurrent Account Balances:")
        for address, balance in self.balances.items():
            print(f"{address}: {balance} coins")



    