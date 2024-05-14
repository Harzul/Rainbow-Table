import hashlib
from abc import ABC, abstractmethod
import random

random.seed(1)


class RT(ABC):
    _ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    _SIZE = len(_ALPHABET)

    @staticmethod
    @abstractmethod
    def _reduced_hash(h: str, iteration: int) -> str:
        h *= 4
        return ''.join(
            [RT._ALPHABET[int(h[(iteration + i) % 53] + h[(iteration + i) % 71], 16) % 26]
             for i in range(131, 555, 101)]
        )

    @staticmethod
    @abstractmethod
    def _get_hash(password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()

    @staticmethod
    @abstractmethod
    def _gen_word(password: str, iteration: int) -> str:
        h = RT._get_hash(password)
        return RT._reduced_hash(h, iteration)

    @staticmethod
    @abstractmethod
    def _gen_passwd(*args: int) -> str:
        passwd = ''
        for i in range(*args):
            passwd += RT._ALPHABET[random.randrange(0, RT._SIZE)]
        return passwd

    @staticmethod
    @abstractmethod
    def _gen_final_word(password: str, *args: int) -> (str, set):
        unique = set()
        word = password
        unique.add(word)
        for i in range(1, *args):
            word = RT._gen_word(word, i)
            unique.add(word)
        return word, unique


class Table(RT):
    def __init__(self, m, chain_length, word_length):
        self._m = m
        self._chain_length = chain_length
        self._word_length = word_length
        self._TABLE = {}
        self._unique = set()

    @property
    def m(self):
        return self._m

    @property
    def chain_length(self):
        return self._chain_length

    def _reduced_hash(self, h: str, iteration: int) -> str:
        return super()._reduced_hash(h, iteration)

    def _get_hash(self, password: str) -> str:
        return super()._get_hash(password)

    def _gen_word(self, password: str, iteration: int) -> str:
        return super()._gen_word(password, iteration)

    def _gen_passwd(self) -> str:
        return super()._gen_passwd(self._word_length)

    def _gen_final_word(self, password: str) -> str:
        return super()._gen_final_word(password, self._chain_length)

    def _count_collisions(self) -> None:
        print(
            f'Size: {len(self._unique)}/{self._m * self._chain_length} \t'
            f'Pure: {len(self._unique) / (self._m * self._chain_length) * 100:.2f}% \t'
            f'Collisions: {(1 - len(self._unique) / (self._m * self._chain_length)) * 100:.2f}% \t'
            f'Coverage: {len(self._unique) / (pow(super()._SIZE, self._word_length)) * 100:.2f}%'
        )

    def w2file(self, filename: str) -> None:
        with open(filename, 'w') as file:
            for k, v in self._TABLE.items():
                file.write(f'{v} {k}\n')

    def generate_table(self) -> None:
        i = 0
        while i < self._m:
            password = self._gen_passwd()
            word, unique = self._gen_final_word(password)
            hashed = self._get_hash(word)
            if self._TABLE.get(hashed, 0):
                continue
            self._unique.update(unique)
            self._TABLE[hashed] = password
            i += 1
        self._count_collisions()

    def _in_table(self, table: dict, data_hash: str) -> str:
        if x := table.get(data_hash, 0):
            return x
        for i in range(self._chain_length, 0, -1):
            iteration = i
            tmp = data_hash
            while iteration < self._chain_length:
                tmp = self._get_hash(self._reduced_hash(tmp, iteration))
                iteration += 1
            if value := table.get(tmp):
                return value
        else:
            return ''

    def _find_password(self, passwd: str, data_hash: str) -> str:
        for i in range(1, self._chain_length + 1):
            if self._get_hash(passwd) == data_hash:
                return passwd
            h = self._get_hash(passwd)
            passwd = self._reduced_hash(h, i)
        return ''

    def __call__(self, data: list[str]) -> str:
        data_hash, filename = data
        table = {}
        with open(filename, 'r') as file:
            for line in file:
                (key, val) = line.split()
                table[val] = key

        if not (passwd := self._in_table(table, data_hash)):
            return 'No such hash in table'
        return f'The password is: {self._find_password(passwd, data_hash)}'

    def __str__(self) -> str:
        for i in self._TABLE.items():
            print(i)
        for j in self._TABLE.values():
            word = j
            print(word)
            for iteration in range(1, self._chain_length):
                word = self._gen_word(word, iteration)
                print(word)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return ''
