from queue import Queue
from time import sleep
from threading import Thread
from random import randint


class Table:
    def __init__(self, number: int, guest=None):
        self.number = number
        self.guest = guest


class Guest(Thread):
    def __init__(self, name: str):
        Thread.__init__(self)
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables: Table):
        self.tables = {table.number: table for table in tables}
        self.queue = Queue()

    def guest_arrival(self, *guests: Guest):
        for guest in guests:
            for x, y in self.tables.items():  # x - table number, y - an object of the Guest class
                if y.guest is None:
                    y.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {x}')
                    break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() and any([table.guest for table in self.tables.values()]):
            for x, y in self.tables.items():  # x - table number, y - an object of the Guest class
                if y.guest is not None:
                    if not y.guest.is_alive():
                        print(f'{y.guest.name} покушал(-а) и ушёл(ушла).\nСтол номер {x} свободен.')
                        if not self.queue.empty():
                            self.tables[x].guest = self.queue.get()
                            self.tables[x].guest.start()
                            print(f'{y.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {x}.')
                        else:
                            self.tables[x].guest = None


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
