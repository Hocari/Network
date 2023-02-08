import hashlib
import time
import sqlite3

conn = sqlite3.connect('blockchain.db')
c = conn.cursor()

class Block:
    def __init__(self, previous_block_hash, transactions, nonce=0):
        self.previous_block_hash = previous_block_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = nonce
        self.block_hash = self.get_block_hash()

    def get_block_hash(self):
        block_string = f"{self.previous_block_hash}{self.transactions}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.get_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.accounts = {}
        self.create_block_table()
        self.create_users_table()

    def create_block_table(self):
        c.execute("""
        CREATE TABLE IF NOT EXISTS blockchain (
            id INTEGER PRIMARY KEY,
            previous_block_hash TEXT,
            transactions TEXT,
            timestamp TEXT,
            nonce INTEGER,
            block_hash TEXT
        );
        """)
        conn.commit()

    def get_genesis_block(self):
        return Block("0", "0")

    def add_block(self, block):
        block.previous_block_hash = self.chain[-1].block_hash
        self.add_to_db(block.previous_block_hash, block.transactions, block.timestamp, block.nonce, block.block_hash)
        self.chain.append(block)

    def add_to_db(self, previous_block_hash, transactions, timestamp, nonce, block_hash):
        c.execute("""
        INSERT INTO blockchain (previous_block_hash, transactions, timestamp, nonce, block_hash)
        VALUES (?,?,?,?,?)
        """, (str(previous_block_hash), str(transactions), str(timestamp), str(nonce), str(block_hash)))
        conn.commit()

    def mine_block(self, block):
        self.add_block(block)
        for transaction in block.transactions:
            sender = transaction["sender"]
            recipient = transaction["recipient"]
            amount = transaction["amount"]
            self.accounts[sender] -= amount
            self.accounts[recipient] += amount

    def create_users_table(self):
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            balance REAL
        );
        """)
        conn.commit()

    def update_balance(self, name, balance):
        c.execute("""
        INSERT OR REPLACE INTO users (name, balance)
        VALUES (?,?)
        """, (name, balance))
        conn.commit()

    def create_account(self, name, starting_balance):
        self.accounts[name] = starting_balance
        self.update_balance(name, starting_balance)

    def get_balance(self, name):
        return self.accounts[name]

    def transfer_funds(self, sender, recipient, amount):
        if self.accounts[sender] >= amount:
            self.pending_transactions.append({
                "sender": sender,
                "recipient": recipient,
                "amount": amount
            })
            self.update_balance(sender, self.accounts[sender] - amount)
            self.update_balance(recipient, self.accounts[recipient] + amount)
        else:
            print("Unable to process transaction: insufficient funds.")


blockchain = Blockchain()

#blockchain.create_account("Briac", 100)
#blockchain.create_account("Gabriel", 0)

#blockchain.transfer_funds("Briac", "Gabriel", 10)

#block = Block(blockchain.chain[-1].block_hash, blockchain.pending_transactions)
#blockchain.mine_block(block)

#print("Briac's balance:", blockchain.get_balance("Briac"))
#print("Gabriel's balance:", blockchain.get_balance("Gabriel"))

# Function to manually create an account
def create_account_manually():
    name = input("Enter the name of the account: ")
    balance = int(input("Enter the starting balance: "))
    blockchain.create_account(name, balance)
    print(f"Account '{name}' created with balance {balance}")

# Function to transfer funds manually
def transfer_funds_manually():
    sender = input("Enter the name of the sender: ")
    recipient = input("Enter the name of the recipient: ")
    amount = int(input("Enter the amount to transfer: "))
    blockchain.transfer_funds(sender, recipient, amount)
    print(f"{amount} sent from '{sender}' to '{recipient}'")

    block = Block(blockchain.chain[-1].block_hash, blockchain.pending_transactions)
    blockchain.mine_block(block)
    #blockchain.add_to_db(block.previous_block_hash, block.transactions, block.timestamp, block.nonce, block.block_hash)


blockchain = Blockchain()

while True:
    print("1. Create account")
    print("2. Transfer funds")
    print("3. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        create_account_manually()
    elif choice == 2:
        transfer_funds_manually()
    elif choice == 3:
        break
    else:
        print("Invalid choice")








