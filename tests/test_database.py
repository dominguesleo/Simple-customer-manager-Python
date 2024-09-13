import copy
import unittest
import database as db
import helpers
import config
import csv

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clients.list = [
            db.Client('12345678A', 'John', 'Doe'),
            db.Client('87654321B', 'Jane', 'Doe'),
            db.Client('15275693C', 'Alice', 'Smith'),
        ]

    def test_search_client(self):
        exits_client = db.Clients.search('12345678A')
        inexistent_client = db.Clients.search('00000000Z')
        self.assertIsNotNone(exits_client)
        self.assertIsNone(inexistent_client)

    def test_add_client(self):
        new_client = db.Clients.add('00000001Z', 'Bob', 'Smith')
        self.assertEqual(len(db.Clients.list), 4)
        self.assertEqual(new_client.dni, '00000001Z')
        self.assertEqual(new_client.name, 'Bob')
        self.assertEqual(new_client.lastname, 'Smith')

    def test_edit_client(self):
        exits_client = copy.copy(db.Clients.search('15275693C'))
        edited_client = db.Clients.edit('15275693C', 'Alice', 'Brown')
        self.assertEqual(exits_client.name, 'Alice')
        self.assertEqual(edited_client.lastname, 'Brown')

    def test_delete_client(self):
        deleted_client = db.Clients.delete('87654321B')
        research_client = db.Clients.search('87654321B')
        self.assertEqual(deleted_client.dni, '87654321B')
        self.assertIsNone(research_client)

    def test_validate_dni(self):
        self.assertTrue(helpers.validate_dni('00000000A', db.Clients.list))
        self.assertFalse(helpers.validate_dni('12345678A', db.Clients.list))
        self.assertFalse(helpers.validate_dni('2345678A', db.Clients.list))
        self.assertFalse(helpers.validate_dni('12345678', db.Clients.list))

    def test_write_csv(self):
        db.Clients.delete('12345678A')
        db.Clients.delete('15275693C')
        db.Clients.edit('87654321B', 'Louise', 'Doyle')

        dni,nombre,apellido = None,None,None
        with open(config.DATABASE_PATH, newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            dni,nombre,apellido = next(reader)

        self.assertEqual(dni, '87654321B')
        self.assertEqual(nombre, 'Louise')
        self.assertEqual(apellido, 'Doyle')
