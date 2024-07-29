import datetime  # Importing the datetime module to work with dates and times.
import hashlib  
from flask import Flask, request, render_template  

class Block:  
    blockNo = 0  
    data = None  
    next = None  
    hash = None  
    nonce = 0  
    previous_hash = 0*0  
    timestamp = datetime.datetime.now()  

    def __init__(self, data, name):  
        self.data = data  
        self.blockName = name  

    def hash(self):  
        h = hashlib.sha256()  
        h.update(  
            str(self.nonce).encode('utf8') +
            str(self.data).encode('utf8') +
            str(self.previous_hash).encode('utf8') +
            str(self.timestamp).encode('utf8') +
            str(self.blockName).encode('utf8'))
        return h.hexdigest()  # Returning the hexadecimal digest of the hash object.

    def __str__(self):  # Defining a method to represent Block object as a string.
        return "Block Hash: " + str(self.hash()) + "\nBlockName: " + str(self.blockName) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"


class Blockchain:  # Defining a class named Blockchain to manage the blockchain.
    diff = 10  # Setting difficulty level for mining.
    maxNonce = 2**32  # Setting maximum value for nonce.
    target = 2**(256-diff)  # Calculating target value for proof of work.

    block = Block("Genesis text", "Genesis")  # Creating the genesis block.
    dummy = head = block  # Initializing dummy and head pointers to the genesis block.

    def add(self, block):  # Method to add a new block to the blockchain.
        block.previous_hash = self.block.hash()  # Setting previous hash of the new block.
        self.block.next = block  # Setting next block of the current block.
        self.block = self.block.next  # Moving to the next block.

    def mine(self, block):  # Method to mine a new block.
        for n in range(self.maxNonce):  # Iterating through nonce values.
            if int(block.hash(), 16) <= self.target:  # Checking if hash meets the target.
                self.add(block)  # Adding the mined block to the blockchain.
                print(block)  # Printing the mined block.
                return block.blockName, block.data  # Returning the block name and data.
            else:
                block.nonce += 1  # Incrementing nonce if target is not met.

app = Flask(__name__)  
blockchain = Blockchain()  
my_dict = []  

@app.route('/')  
def my_form():  
    return render_template('index.html', content="")  

@app.route('/', methods=['POST', 'GET'])  
def my_form_post():  
    PayeeName = request.form['PayeeName']  
    AmountTransfer = request.form['AmountTransfer']  

    nm, tx = blockchain.mine(Block(AmountTransfer, PayeeName))  
    my_dict.append([nm, tx])  
    return render_template('index.html', name_list=my_dict)  

if __name__ == "__main__":  
    app.run(debug=True)  
