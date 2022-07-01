from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, company):
        self._items = items
        self._capacity = company

    @abstractmethod
    def add(self, title, count):
        pass

    @abstractmethod
    def remove(self, title, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, count):
        if title in self._items:
            self._items[title] += count
        else:
            self._items[title] = count
        self._capacity -= count

    def remove(self, title, count):
        res = self._items[title] - count
        if res > 0:
            self._capacity += count
            self._items[title] = res
        else:
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        return self._capacity

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def unique_items_count(self):
        return len(self._items.keys())


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, data):
        self.data = self._split_data(data)
        self.store_ = self.data[4]
        self.shop_ = self.data[6]
        self.amount = int(self.data[1])
        self.product = self.data[2]

    @staticmethod
    def _split_data(data):
        return data.split(' ')

    def __repr__(self):
        return f'Deliver {self.amount} {self.product} from {self.store_} to {self.shop_}'


def main():
        print(f'Hello! This program shows the abstract movement of goods between store and shop.\n '
              f'Enter your request in the format: "Deliver [quantity] [product] from [store] to [shop]"\n '
              f'You can also change final places for delivery: from [shop] to [store]\n '
              f'Now we have such products: \n'
              f'flakes\ncoffee\njuice\ncookie\ncrisps\nsausage')
        user_input = input('Enter your request:  ')
        if user_input == 'stop':
            exit()
        request = Request(user_input)

        store_ = store if request.store_ == 'store' else shop
        shop_ = store if request.store_ == 'store' else shop

        if request.product in store_.items:
            print(f'Item in location \"{request.store_}\"')
        else:
            print(f'There is no item in location \"{store_}\"')

        if store_.items[request.product] >= request.amount:
            print(f'Enough quantity in location \"{request.store_}\"')
        else:
            print(f'{request.amount - store_.items[request.product]} '
                  f'missing from location \"{request.store_}\"')

        if shop_.get_free_space >= request.amount:
            print(f'Enough space in location \"{request.shop_}\"')
        else:
            print(f'Enough space in location is: {shop_.get_free_space}')
            print(f'Not enough space in location \"{request.shop_}\":'
                  f' {request.amount - shop_.get_free_space} missing')

        if request.shop_ == 'shop' \
                and shop_.unique_items_count == 5 \
                and request.product not in shop_.items:
            print('There are enough unique items in shop')

        print('__' * 10)
        store.remove(request.product, request.amount)
        print(f'Courier took {request.amount} {request.product} from {request.store_}')
        print(f'Courier delivering {request.amount} {request.product} '
              f'from {request.store_} to {request.shop_}')

        shop.add(request.product, request.amount)
        print(f'Courier delivered {request.amount} {request.product} to {request.shop_}')
        print('__' * 10)
        print('In store:')
        for title, count in store.items.items():
            print(f'{title}: {count}')
        print(f'Free space: {store.get_free_space}')
        print('__' * 10)
        print('In shop:')
        for title, count in shop.items.items():
            print(f'{title}: {count}')
        print(f'Free space: {shop.get_free_space}')
        print('__' * 10)


if __name__ == '__main__':

    store = Store()
    shop = Shop()


    store_items = {
        'coffee': 9,
        'flakes': 12,
        'juice': 5,
        'cookie': 18,
        'crisps': 23,
        'sausage': 6,
    }

    store.items = store_items
    main()




