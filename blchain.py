import datetime  # Importing the datetime module to work with dates and times.
import hashlib  # Importing the hashlib module to perform secure hash and message digest algorithms.
from flask import Flask, request, render_template  # Importing Flask framework for web application development, along with request handling and rendering HTML templates.

class Block:  # Defining a class named Block for creating blocks in the blockchain.
    blockNo = 0  # Initializing the block number.
    data = None  # Initializing data attribute of the block.
    next = None  # Initializing next attribute of the block.
    hash = None  # Initializing hash attribute of the block.
    nonce = 0  # Initializing nonce attribute of the block.
    previous_hash = 0*0  # Initializing previous_hash attribute of the block.
    timestamp = datetime.datetime.now()  # Setting timestamp to the current date and time using datetime module.

    def __init__(self, data, name):  # Defining constructor for the Block class.
        self.data = data  # Assigning data attribute of the block.
        self.blockName = name  # Assigning blockName attribute of the block.

    def hash(self):  # Defining a method to calculate hash of the block.
        h = hashlib.sha256()  # Creating a SHA-256 hash object.
        h.update(  # Updating hash object with concatenated data.
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

app = Flask(__name__)  # Creating a Flask application instance. ---------------------------------------------------------------------------------------------------
blockchain = Blockchain()  # Creating a Blockchain instance.
my_dict = []  # Initializing a list to store mined blocks.

@app.route('/')  # Route decorator for root URL.-------------------------------------------------------------------------------------------------------------------
def my_form():  # Function to handle GET requests.-----------------------------------------------------------------------------------------------------------------
    return render_template('index.html', content="")  # Rendering the HTML template with no content.---------------------------------------------------------------

@app.route('/', methods=['POST', 'GET'])  # Route decorator for root URL with POST and GET methods.----------------------------------------------------------------
def my_form_post():  # Function to handle POST requests.-----------------------------------------------------------------------------------------------------------
    PayeeName = request.form['PayeeName']  # Getting PayeeName from form data.-------------------------------------------------------------------------------------
    AmountTransfer = request.form['AmountTransfer']  # Getting AmountTransfer from form data.----------------------------------------------------------------------

    nm, tx = blockchain.mine(Block(AmountTransfer, PayeeName))  # Mining a new block. nm will be blockName and tx will be data (l.50)------------------------------
    my_dict.append([nm, tx])  # Appending block name and data to dictionary.---------------------------------------------------------------------------------------
    return render_template('index.html', name_list=my_dict)  # Rendering HTML template with updated data.----------------------------------------------------------

if __name__ == "__main__":  # Checking if the script is being run directly.----------------------------------------------------------------------------------------
    app.run(debug=True)  # Running the Flask application in debug mode.--------------------------------------------------------------------------------------------
