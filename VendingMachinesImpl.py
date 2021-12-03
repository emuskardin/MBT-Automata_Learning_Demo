from abc import ABC, abstractmethod


class AbstractVendingMachine(ABC):

    @abstractmethod
    def add_coin(self, coin):
        pass

    @abstractmethod
    def push_button(self, order):
        pass

    @abstractmethod
    def reset(self):
        pass


class VendingMachine(AbstractVendingMachine):
    def __init__(self, max_coins=5):
        self.coin_count = 0
        self.max_coins = max_coins

    def add_coin(self, coin):
        if self.coin_count + coin > self.max_coins:
            return 'coin_returned'
        self.coin_count += coin
        return 'coin_added'

    def push_button(self, order):
        if order == 'coke':
            if self.coin_count >= 2:
                self.coin_count -= 2
                return 'Coke'
            else:
                return 'No_Action'
        if order == 'peanuts':
            if self.coin_count >= 3:
                self.coin_count -= 3
                return 'Peanuts'
            else:
                return 'No_Action'
        if order == 'water':
            if self.coin_count >= 1:
                self.coin_count -= 1
                return 'Water'
            else:
                return 'No_Action'

    def reset(self):
        self.coin_count = 0


class VendingMachineMutant1(AbstractVendingMachine):
    def __init__(self, max_coins=5):
        self.coin_count = 0
        self.max_coins = max_coins

    def add_coin(self, coin):
        if self.coin_count + coin > self.max_coins:
            return 'coin_returned'
        self.coin_count += coin
        return 'coin_added'

    def push_button(self, order):
        if order == 'coke':
            if self.coin_count >= 2:
                self.coin_count -= 2
                return 'Coke'
            else:
                return 'No_Action'
        if order == 'peanuts':
            if self.coin_count >= 3:
                self.coin_count -= 3
                return 'Peanuts'
            else:
                return 'No_Action'
        if order == 'water':
            if self.coin_count >= 1:
                return 'Water'
            else:
                return 'No_Action'

    def reset(self):
        self.coin_count = 0


class VendingMachineMutant2(AbstractVendingMachine):
    def __init__(self, max_coins=5):
        self.coin_count = 0
        self.max_coins = max_coins

    def add_coin(self, coin):
        if self.coin_count + coin > self.max_coins:
            return 'coin_returned'
        self.coin_count += coin
        return 'coin_added'

    def push_button(self, order):
        if order == 'coke':
            if self.coin_count >= 2:
                self.coin_count -= 2
                return 'Coke'
            else:
                return 'No_Action'
        if order == 'peanuts':
            if self.coin_count >= 3:
                self.coin_count -= 1
                return 'Peanuts'
            else:
                return 'No_Action'
        if order == 'water':
            if self.coin_count >= 1:
                self.coin_count -= 1
                return 'Water'
            else:
                return 'No_Action'

    def reset(self):
        self.coin_count = 0
