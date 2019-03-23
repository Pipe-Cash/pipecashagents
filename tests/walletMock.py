import decimal
import time

class MockWallet:
    def __init__(self):
        self.logs = []

        self.__balance = 0

        self.id = 0
        self.transactions = []

        self.privKey = "KzsiurdHMQYdD2Wm8rLz3Xz5k7LCby7dmCvpEQoFxhuxNTXoHJBx"
        self.pubKey = "$149vgRXB9ouVCxPq8Fx9E7QqHhreRUGruo"

    def start(self, log):
        self.logs.append("start")

    def checkBalance(self):
        self.logs.append("checkBalance " + str(self.__balance))
        return self.__balance

    def send(self, amount, address):
        self.logs.append("send %s to %s" % (amount, address))
        self.addTransaction(-amount)

    def getReceiveAddress(self):
        self.logs.append("getReceiveAddress " + self.pubKey)
        return self.pubKey

    def getLatestTransactions(self, num=10, skip=0):
        self.logs.append("getLatestTransactions " + str([skip, num]))
        return self.transactions[skip: num]

    def addTransaction(self, amount):
        self.id = self.id + 1
        self.transactions.append(
            {
                'amount': decimal.Decimal(amount),
                'time': time.time(),
                'id': self.id,
                'confirmations': 0,
            }
        )
        self.__balance = self.__balance + amount

    def addBlock(self, count=1):
        for tx in self.transactions:
            tx['confirmations'] = tx['confirmations'] + count

