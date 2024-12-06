use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH, Instant};
use rand::Rng;
use sha2::{Sha256, Digest};

/// Represents a single transaction in the blockchain
#[derive(Debug, Clone)]
pub struct Transaction {
    /// The sender's address
    sender: String,
    /// The receiver's address
    receiver: String,
    /// The amount of cryptocurrency being transferred
    amount: u32,
}

/// Represents a block in the blockchain
#[derive(Debug, Clone)]
pub struct Block {
    /// The index of the block
    index: u32,
    /// The hash of the previous block
    previous_hash: String,
    /// The timestamp of when the block was created
    timestamp: u64,
    /// A list of transactions included in the block
    transactions: Vec<Transaction>,
    /// The proof of work for the block
    proof: u32,
    /// The hash of the block
    hash: String,
}

/// Represents the entire blockchain
pub struct Blockchain {
    /// The actual chain of blocks
    chain: Vec<Block>,
    /// Pending transactions waiting to be mined
    current_transactions: Vec<Transaction>,
    /// Tracks account balances
    balances: HashMap<String, u32>,
}

impl Blockchain {
    /// Creates a new blockchain with a genesis block
    pub fn new() -> Blockchain {
        let mut blockchain = Blockchain {
            chain: Vec::new(),
            current_transactions: Vec::new(),
            balances: HashMap::new(),
        };
        blockchain.create_genesis_block();
        blockchain
    }

    /// Creates the first block in the blockchain
    fn create_genesis_block(&mut self) {
        let genesis_block = Block {
            index: 0,
            previous_hash: String::from("0"),
            timestamp: Self::current_timestamp(),
            transactions: vec![],
            proof: 100, // Arbitrary proof for the genesis block
            hash: String::from("0"), // Initial hash for genesis block
        };
        self.chain.push(genesis_block);
    }

    /// Adds a new transaction to the pending transactions
    pub fn add_transaction(&mut self, sender: &str, receiver: &str, amount: u32) -> Result<(), String> {
        // Check if sender has sufficient balance
        let sender_balance = self.get_balance(sender);
        if sender_balance < amount && sender != "network" {
            return Err(format!("Insufficient balance. Sender {} has {} but tried to send {}", 
                               sender, sender_balance, amount));
        }

        let transaction = Transaction {
            sender: sender.to_string(),
            receiver: receiver.to_string(),
            amount,
        };
        
        // Update balances
        if sender != "network" {
            *self.balances.entry(sender.to_string()).or_insert(0) -= amount;
        }
        *self.balances.entry(receiver.to_string()).or_insert(0) += amount;

        self.current_transactions.push(transaction);
        println!("Transaction added: {} -> {} : {} coins", sender, receiver, amount); // Progress update
        Ok(())
    }

    /// Mines a new block and adds it to the blockchain
    pub fn mine_block(&mut self, miner_address: &str) -> Block {
        // Add mining reward
        self.add_transaction("network", miner_address, 10)
            .expect("Mining reward transaction failed");

        let last_block = self.chain.last().unwrap();
        let proof = self.proof_of_work(last_block.proof);

        let new_block = Block {
            index: self.chain.len() as u32,
            previous_hash: last_block.hash.clone(),
            timestamp: Self::current_timestamp(),
            transactions: self.current_transactions.clone(),
            proof,
            hash: String::from(""),
        };

        // Calculate the new block's hash
        let block_hash = Self::calculate_hash(&new_block);
        let mut new_block = new_block;
        new_block.hash = block_hash;

        // Add the new block to the chain and reset the current transactions
        self.chain.push(new_block.clone());
        self.current_transactions.clear();

        println!("Block mined successfully: {:?}", new_block); // Block mined update
        new_block
    }

    /// Implements Proof of Work consensus mechanism
    fn proof_of_work(&self, last_proof: u32) -> u32 {
        let mut proof = rand::thread_rng().gen_range(1000..9999); // Random initial proof
        println!("Starting proof of work...");
        while !self.valid_proof(last_proof, proof) {
            proof = rand::thread_rng().gen_range(1000..9999);
        }
        println!("Proof of work found: {}", proof); // Proof found update
        proof
    }

    /// Validates the proof of work
    fn valid_proof(&self, last_proof: u32, proof: u32) -> bool {
        let guess = format!("{}{}", last_proof, proof);
        let guess_hash = Sha256::digest(guess.as_bytes());
        let guess_hash_str = format!("{:x}", guess_hash);

        // Check if the hash starts with "00" (lower difficulty)
        &guess_hash_str[..2] == "00"  // Reduced difficulty
    }

    /// Calculates the hash for a block
    fn calculate_hash(block: &Block) -> String {
        let block_string = format!(
            "{}{}{}{:?}{}",
            block.index, block.previous_hash, block.timestamp, block.transactions, block.proof
        );
        let hash = Sha256::digest(block_string.as_bytes());
        format!("{:x}", hash)
    }

    /// Gets the current Unix timestamp
    fn current_timestamp() -> u64 {
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs()
    }

    /// Retrieves the balance of a given account
    pub fn get_balance(&self, address: &str) -> u32 {
        *self.balances.get(address).unwrap_or(&0)
    }

    /// Displays the entire blockchain
    pub fn display_chain(&self) {
        println!("Blockchain Ledger:");
        for block in &self.chain {
            println!("Block #{}", block.index);
            println!("  Previous Hash: {}", block.previous_hash);
            println!("  Timestamp: {}", block.timestamp);
            println!("  Transactions:");
            for transaction in &block.transactions {
                println!("    {} -> {} : {} coins", transaction.sender, transaction.receiver, transaction.amount);
            }
            println!("  Proof: {}", block.proof);
            println!("  Hash: {}", block.hash);
            println!();
        }
    }

    /// Displays the current account balances
    pub fn display_balances(&self) {
        println!("\nCurrent Account Balances:");
        for (address, balance) in &self.balances {
            println!("{}: {} coins", address, balance);
        }
    }
}

fn main() {
    // Start total runtime timer
    let total_start = Instant::now();

    // Create a new blockchain
    let mut blockchain = Blockchain::new();

    // Simulate initial coin distribution
    blockchain.add_transaction("network", "Alice", 100).unwrap();
    blockchain.add_transaction("network", "Bob", 50).unwrap();

    // Simulate some transactions
    println!("Initial Transactions:");
    blockchain.add_transaction("Alice", "Bob", 20).unwrap();
    blockchain.add_transaction("Bob", "Charlie", 15).unwrap();

    // Mine blocks with timing
    println!("\nMining Blocks:");
    let miner1 = "Miner1";
    let block1_start = Instant::now();
    let _first_block = blockchain.mine_block(miner1);
    let block1_duration = block1_start.elapsed();
    println!("Block mined by {} (Time: {:?})", miner1, block1_duration);

    let miner2 = "Miner2";
    let block2_start = Instant::now();
    let _second_block = blockchain.mine_block(miner2);
    let block2_duration = block2_start.elapsed();
    println!("Block mined by {} (Time: {:?})", miner2, block2_duration);

    // Display blockchain details
    blockchain.display_chain();
    blockchain.display_balances();

    // Demonstrate balance tracking and transaction validation
    println!("\nBalance Checks:");
    println!("Alice's Balance: {} coins", blockchain.get_balance("Alice"));
    println!("Bob's Balance: {} coins", blockchain.get_balance("Bob"));
    println!("Charlie's Balance: {} coins", blockchain.get_balance("Charlie"));
    println!("Miner1's Balance: {} coins", blockchain.get_balance(miner1));
    println!("Miner2's Balance: {} coins", blockchain.get_balance(miner2));

    // Demonstrate transaction validation
    println!("\nTransaction Validation Test:");
    match blockchain.add_transaction("Alice", "Bob", 1000) {
        Ok(_) => println!("Transaction succeeded"),
        Err(e) => println!("Transaction failed: {}", e),
    }

    // Print total runtime
    let total_duration = total_start.elapsed();
    println!("\nTotal Simulation Runtime: {:?}", total_duration);
}
