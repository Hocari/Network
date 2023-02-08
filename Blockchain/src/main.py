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
        buyer_balance = self.get_balance(buyer_address)
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