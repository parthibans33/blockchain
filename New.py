from datetime import datetime
from eth_account import Account
from web3 import Web3
from mnemonic import Mnemonic
import hashlib
import json
from random import randrange
from datetime import datetime
from mysql.connector import Error
import mysql.connector 



class Wallet:
    def __init__(self) -> None:
        Account.enable_unaudited_hdwallet_features()
        self.infura_url = "https://kovan.infura.io/v3/1b6c0ac430c04d9ea18aabe4d787763d"
        self.w3 = Web3(Web3.HTTPProvider(self.infura_url))
        mnemo =Mnemonic("english").generate(strength=128)
        self.acc = self.w3.eth.account.from_mnemonic(mnemo)
        self.wallet_address='0x0d6421B15e07D11738de942D0a49CC9E8AafC1e4'
        self.wallet_key ='f753b0d910c4e86c3926606bd551f052d6c26c594f985b754fc306a639fdf612'
        self.Wallet_Details()
        pass

    def Wallet_Details(self):
        print(f'Wallet Address: {self.wallet_address} \nPrivate Key: {self.wallet_key}')
        balance = self.w3.eth.get_balance(self.wallet_address)
        print(f'Wallet Account Balance  : {balance}')
        self.block_no =self.w3.eth.blockNumber
        print(f'Block Number :{self.block_no}')

    
    
    def made_transactions(self):  
        self.accounts=[]
        i=0
        while i<100:
            mnem =Mnemonic("english").generate(strength=128)
            newac = self.w3.eth.account.from_mnemonic(mnem)
            add =newac.address
            self.accounts.append(add)
            i+=1
            continue
                
        # nonce =self.w3.eth.getTransactionCount(self.wallet_address)
        # random_add = self.accounts[randrange(0,100)]
        amu =float(input("Enter the Amount in Ether:"))
        self.time = datetime.now()
        transac = dict(nonce =self.w3.eth.getTransactionCount(self.wallet_address),to='0x90144867fFBf78D7d3C104835bD95B1aaeBc7a4E',
        gas = 21000,value=self.w3.toWei(amu, 'ether'),gasPrice=self.w3.toWei('5 ', 'gwei'))
        signtransc =self.w3.eth.account.sign_transaction(transac,self.wallet_key)
        self.transhash    =self.w3.eth.send_raw_transaction(signtransc.rawTransaction)
        self.t=self.w3.toHex(self.transhash)
        # transaction_detail = {
        #     'Transaction_Hash': hashlib.sha256(self.t),
        #     'From_Address': self.wallet_address,
        #     'To_Address':random_add,
        #     'Amount' : value,
        #     'Timestamp': self.time
        # }
        # print(json.dumps(transaction_detail, indent=4))
        # pass
        # return self.t

    
class Details_Add(Wallet):

        def __init__(self) -> None:
            
            super().__init__()
            ask_wal = str(input('Do you want do some transations  type(y/n):'))
            if ask_wal.lower()=='y':
                Wallet.made_transactions(self)
            else:
                print(')):')
            
            self.transac_recepit = self.w3.eth.get_transaction(self.transhash)
            if self.wallet_address == self.transac_recepit['from']:
                    preblock = int((self.block_no)-1)
                    self.preblock_hash = hashlib.sha256()
            else:
                print('Transaction Not Found')

            


                 

class Database(Details_Add,Wallet):

    def __init__(self) -> None:
        super().__init__()
        
        try:
            
            dbconnect = mysql.connector.connect(host='localhost',
                                                database = '7bits_task',
                                                user='root',
                                                password='parthiban')
            if  dbconnect.is_connected():
                    cursor = dbconnect.cursor()    
            print('Database Connected')
            transactions = 'CREATE TABLE transactions (id INT AUTO_INCREMENT PRIMARY KEY,Transaction_hash VARCHAR(255),from_address VARCHAR(255),to_address VARCHAR(255),Timestamp VARCHAR(255))'
            blocks = 'CREATE TABLE blocks (id INT AUTO_INCREMENT PRIMARY KEY,Block_hash VARCHAR(255),Present_hash VARCHAR(255),Timestamp VARCHAR(255),Process VARCHAR(255))'
            cursor.execute(blocks)
            cursor.execute(transactions)
            print('Table Created')

            
            cursor.execute('SHOW TABLES')
            for x in cursor:
                print(x)
            cursor.execute('SHOW COLUMNS FROM blocks')
            print([column[0] for column in cursor.fetchall()])
            cursor.execute('SHOW COLUMNS FROM transaction')
            print([column[0] for column in cursor.fetchall()])



            cursor.execute("""INSERT INTO blocks(Block_hash,Present_hash,Timestamp,Processs) 
            values (%s, %s, %s, %s)""",(self.transac_recepit["blockhash"],self.preblock_hash,
            self.time, self.j))
            cursor.execute("""INSERT INTO transactions(Transaction_hash,from_address,to_address,Timestamp) 
            values (%s, %s, %s, %s)""",(self.t,self.transac_recepit['from'],self.transac_recepit['to'],
            self.time))



            bl_data = "select * from blocks"
            cursor.execute(bl_data)
            block_data = cursor.fetchall()
            block =  json.loads(block_data)
            print(block)
            tr_data = "select * from transactions"
            cursor.execute(tr_data)
            trans_data = cursor.fetchall()
            Transaction =  json.loads(trans_data)
            print(Transaction)

        except Error as e:
            print("Error while connecting to MySQL", e)
        
    
    
        dbconnect.close()
    pass
            


            

wl = Details_Add()
