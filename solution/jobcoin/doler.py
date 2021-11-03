from datetime import datetime
from decimal import Decimal
from jobcoin import config
from jobcoin import mapper
from typing import Dict
from typing import List
import json
import random
import requests
import threading;
import time

class Doler:
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self.addressMap = mapper.SingletonMap()
        
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            # another thread could have created the instance
            # before we acquired the lock. So check that the
            # instance is still nonexistent.
            if not cls._instance:
                cls._instance = super(Doler, cls).__new__(cls)

        return cls._instance

    def sendFund(self, fromAddress: str, toAddress: str, amount: float) -> None:
        URL = config.API_TRANSACTIONS_URL
        # print("requesting from:" + URL)
        
        # print("Sending {} from {} to {}".format(amount, fromAddress, toAddress))
        response = requests.post(URL, params={"fromAddress": fromAddress, "toAddress": toAddress, "amount": amount})
        # print(response.json())
        
    def filterTransactions(self, address: str, old_ts: float, new_ts: float, transactions: List[Dict]) -> float:
        amount = Decimal(0.0)
        
        for txn in transactions:
            txn_ts = datetime.timestamp(datetime.strptime(txn["timestamp"], '%Y-%m-%dT%H:%M:%S.%f%z'))
            if txn["toAddress"] == address:
                if txn_ts > old_ts:
                    amount += Decimal(txn["amount"])
                if txn_ts > new_ts:
                    new_ts = txn_ts
                    
        return amount, new_ts
    
    def distributeFundToRealAccount(self, toAddresses: List[str], totalAmout: float) -> None:
        if totalAmout == Decimal(0.0):
            return 
        
        N = len(toAddresses)
        tripleN = N * 3
        
        for i in range(tripleN):
            random_index = random.randint(0, tripleN - 1) % N
            toAddr = toAddresses[random_index]
            partial_amount = Decimal(0.0)
            
            if i == tripleN - 1:
                partial_amount = totalAmout
            else:
                partial_amount = Decimal((random.randint(1, 1000) / 1000)) * totalAmout
                
            totalAmout -= partial_amount
            
            time.sleep(random.randint(1, 1000) * 5 / 1000)
            
            if partial_amount > 0.0:
                self.sendFund(config.HOUSE_ACCOUNT, toAddr, partial_amount)
    
    def poll(self, pseudoAddr: str) -> None:
        # Pull transactions for $pseudoAddr
        URL = "{0}/{1}".format(config.API_ADDRESS_URL, pseudoAddr)
        # print("requesting from:" + URL)
        response = requests.get(URL)
        res_json = response.json()
        book = self.addressMap.get(pseudoAddr)
        # print(json.dumps(book))
        
        # Parse response
        old_ts = book["timestamp"]
        toAddresses = book["addresses"]
        new_ts = old_ts
        balance = res_json["balance"]
        # print(res_json)
        transactions = res_json["transactions"]
        
        # Calculate $outgoingAmount to transfer to sender's real accounts
        outgoingAmount, new_ts = self.filterTransactions(pseudoAddr, old_ts, new_ts, transactions)
        # print("outgoingAmount: {}".format(outgoingAmount))
        
        # Collect fund by transfer fund into HOUSE_ACCOUNT if fund is greater than 0.0
        if outgoingAmount > Decimal(0.0):
            self.sendFund(pseudoAddr, config.HOUSE_ACCOUNT, outgoingAmount)
        
        # Update timestamp for book
        book["timestamp"] = new_ts
        
        # transfer fund to sender's real accounts
        self.distributeFundToRealAccount(toAddresses, outgoingAmount)
        
        # print("-------")
        
    def start(self) -> None:
        if self._lock.locked():
            return
        
        self._lock.acquire()
        try:
            while (True):
                # 5 seconds delay
                time.sleep(5)
                # Poll the network for transactions for each pseudoAddress
                for pseudoAddress in self.addressMap.getKeys():
                    self.poll(pseudoAddress)
        except:
            self._lock.release()