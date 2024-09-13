import csv
import config

class Client:
    def __init__(self, dni, name, lastname):
        self.dni = dni
        self.name = name
        self.lastname = lastname

    def __str__(self):
        return f'{self.dni} {self.name} {self.lastname}'

class Clients:

    list = []
    with open(config.DATABASE_PATH, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for dni, name, lastname in reader:
            client = Client(dni, name, lastname)
            list.append(client)

    @staticmethod
    def search(dni):
        for c in Clients.list:
            if c.dni == dni:
                return c
        return None

    @staticmethod
    def add(dni, name, lastname):
        c = Client(dni, name, lastname)
        Clients.list.append(c)
        Clients.save()
        return c

    @staticmethod
    def edit(dni, name, lastname):
        c = Clients.search(dni)
        if c:
            c.name = name
            c.lastname = lastname
            Clients.save()
        return c

    @staticmethod
    def delete(dni):
        c = Clients.search(dni)
        if c:
            Clients.list.remove(c)
            Clients.save()
        return c

    @staticmethod
    def save():
        with open(config.DATABASE_PATH, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for c in Clients.list:
                writer.writerow([c.dni, c.name, c.lastname])