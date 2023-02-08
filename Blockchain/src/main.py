import time
import hashlib


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty_level = 2
        self.create_genesis_block()
        self.address_balance = {}
        self.tokens = []
        self.market_tokens = {}

    def create_genesis_block(self):
        # create the first block in the chain
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.mine_block(self.difficulty_level)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def create_block(self, nonce, previous_hash):
        block = Block(len(self.chain), self.pending_transactions, time.time(), previous_hash, nonce)
        block.mine_block(self.difficulty_level)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def create_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self):
        # Create a new block from the pending transactions
        block = Block(len(self.chain) + 1, self.pending_transactions, time.time(), self.get_last_block().hash)
        # Mine the block by finding a valid nonce
        nonce = 0
        while self.valid_proof(block, nonce) is False:
            nonce += 1
        block.nonce = nonce
        # Add the mined block to the chain and clear the pending transactions
        self.chain.append(block)
        self.pending_transactions = []

    # Helper functions
    def valid_proof(self, block, nonce):
        # Calculate the hash of the block and check if it meets the difficulty requirement
        guess = f"{block}{nonce}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty_level] == "0" * self.difficulty_level
    
    def get_balance(self, address):
        return self.address_balance.get(address, 0)

    def send_funds(self, sender, recipient, amount):
        sender_balance = self.get_balance(sender)
        if sender_balance >= amount:
            self.address_balance[sender] = sender_balance - amount
            self.address_balance[recipient] = self.get_balance(recipient) + amount
            self.create_transaction(sender, recipient, amount)
            return True
        return False

    def consensus(self):
        """
        Handles the consensus mechanism for the blockchain.
        """
        # code to handle consensus mechanism ...

    def backup_blockchain(self):
        """
        Backs up the current state of the blockchain to a file.
        """
        # code to backup the blockchain to a file ...

    def load_blockchain(self):
        """
        Loads a previously backed up version of the blockchain.
        """
        # code to load a previously backed up version of the blockchain ...
        
    def get_blockchain_stats(self):
        num_blocks = len(self.chain)
        num_transactions = 0
        for block in self.chain:
            num_transactions += len(block.transactions)
        return {
            'number of blocks': num_blocks,
            'number of transactions': num_transactions
            # other statistics can be added as needed
        }
        
    def update_difficulty(self, new_difficulty):
        self.difficulty = new_difficulty

        


class Token:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty_level = 2
        Blockchain.create_genesis_block()
        self.address_balance = {}
        self.tokens = []
        self.market_tokens = {}


    def create_token(self, name, symbol, total_supply):
        # Check if the token name and symbol are unique
        for token in self.tokens:
            if token['name'] == name or token['symbol'] == symbol:
                return "Token already exists with this name or symbol"
        
        # Create the token
        new_token = {
            'name': name,
            'symbol': symbol,
            'total_supply': total_supply,
            'status': 'pending' # initial status for the token is 'pending'
        }
        self.tokens.append(new_token)
        return "Token created successfully"
        
    def approve_token(self, symbol):
        # Check if the token with the given symbol exists
        for token in self.tokens:
            if token['symbol'] == symbol:
                # Change the status of the token to 'approved'
                token['status'] = 'approved'
                return "Token approved successfully"
        return "Token with symbol not found"


    def add_token_to_market(self, token):
        self.market_tokens.append(token)

    def buy_token(self, buyer_address, token_name, amount):
        # Check if the token exists in the market
        token = None
        for t in self.market_tokens:
            if t['name'] == token_name:
                token = t
                break

        if not token:
            raise ValueError(f'Token with name "{token_name}" does not exist in the market')

        # Check if the buyer has sufficient funds
        buyer_balance = Blockchain.get_balance(buyer_address)
        if buyer_balance < token['price'] * amount:
            raise ValueError(f'Insufficient funds for buyer with address "{buyer_address}"')

        # Deduct funds from the buyer's balance and add to the seller's balance
        buyer_balance -= token['price'] * amount
        seller_balance = self.get_balance(token['seller']) + token['price'] * amount

        # Update the buyer's and seller's balances
        self.update_balance(buyer_address, buyer_balance)
        self.update_balance(token['seller'], seller_balance)

        # Update the token in the market
        token['amount'] -= amount
        if token['amount'] == 0:
            self.market_tokens.remove(token)

    def sell_token(self, seller_address, token_name, amount, price):
        # Check if the seller has the token
        token = None
        for t in self.tokens:
            if t['name'] == token_name and t['owner'] == seller_address:
                token = t
                break

        if not token:
            raise ValueError(f'Token with name "{token_name}" does not belong to the seller with address "{seller_address}"')

        # Check if the seller has sufficient tokens
        if token['amount'] < amount:
            raise ValueError(f'Seller with address "{seller_address}" does not have sufficient tokens')

        # Deduct the tokens from the seller and add to the market
        token['amount'] -= amount
        self.market_tokens.append({'name': token_name, 'seller': seller_address, 'amount': amount, 'price': price})

    def get_token_price(self, token_id):
        """Returns the current price of a token with the given ID."""
        for token in self.tokens:
            if token['id'] == token_id:
                return token['price']
        return None

    def get_market_tokens(self):
        """Returns the list of all tokens available on the cryptocurrency market."""
        return self.tokens




class Block:
    def __init__(self, transactions, timestamp, previous_hash, nonce=0):
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.generate_hash()
        self.nonce = nonce

    def generate_hash(self):
        # generate a unique hash for the block
        # ...
        return True

    def get_transactions(self):
        return self.transactions

    def validate_block(self, previous_block_hash):
        # check if the previous block hash is the same as the hash of the previous block
        if self.previous_hash != previous_block_hash:
            return False

        # validate the transactions in the block
        for transaction in self.transactions:
            if not Transaction.validate_transaction(transaction):
                return False

        return True



    
class Transaction:
    def validate_transaction(self, transaction):
        # Validate the transaction
        if not all([transaction.sender, transaction.recipient, transaction.amount]):
            # If any of the required fields are missing, return False
            return False
        if transaction.amount <= 0:
            # If the amount is not positive, return False
            return False
        # If the transaction passes all the checks, return True
        return True




class Message:
    def __init__(self):
        self.messages = {}

    def send_message(self, recipient, message):
        encrypted_message = self.encrypt(message)
        self.messages[recipient] = encrypted_message

    def get_message(self, recipient):
        encrypted_message = self.messages.get(recipient)
        if encrypted_message:
            return self.decrypt(encrypted_message)
        return None

    def encrypt(self, message):
        # Add code here to encrypt the message
        return encrypted_message

    def decrypt(self, encrypted_message):
        # Add code here to decrypt the encrypted message
        return message




class User:
    def __init__(self, address, username, email):
        self.users = {}
        self.username = username
        self.email = email
        self.transactions = []
        self.address = address
    
    def create_user(self, address, username, email):
        if address in self.users:
            return "User with this address already exists."
        
        user = {
            "address": address,
            "username": username,
            "email": email
        }
        self.users[address] = user
        return "User created successfully."
    
    def get_user(self, address):
        if address in self.users:
            return self.users[address]
        return "User not found."

    def update_user(self, new_username, new_email):
        self.username = new_username
        self.email = new_email

    def get_user_transactions(self):
        return self.transactions