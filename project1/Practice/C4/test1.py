from datetime import datetime
import time
import math

n = 10000


class Test:
    def __init__(self):
        pass

    def __enter__(self):
        self.start = datetime.now()
        self.a = n ** 2
        self.b = n * math.log(n)
        with open('new_text.txt', 'w', encoding='utf-8') as file_1:
            file_1.write('Hello')
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Time passed: {(datetime.now() - self.start).total_seconds()}")
        print(f'a: {self.a}')
        print(f'b: {self.b}')
        print(f'{self.a / 13}')


with Test():
    time.sleep(0.00001)
