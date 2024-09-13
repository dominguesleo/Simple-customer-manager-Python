import os
import helpers
import database as db

def init():
    while True:
        helpers.clear_screen()

        print('========================')
        print(' Welcome to the system ')
        print('========================')
        print('1) List clients')
        print('2) Search client')
        print('3) Add client')
        print('4) Edit client')
        print('5) Delete client')
        print('6) Exit')
        print('========================')

        option = input('> ')
        helpers.clear_screen()

        if option == '1':
            print('Listing clients...\n')
            for client in db.Clients.list:
                print(client)

        elif option == '2':
            print('Searching client...\n')
            dni = helpers.read_text(9, 9, 'Enter DNI (8 int and 1 char)').upper()
            client = db.Clients.search(dni)
            print(client) if client else print('Client not found')

        elif option == '3':
            print('Adding client...\n')

            dni = None
            while True:
                dni = helpers.read_text(9, 9, 'Enter DNI (8 int and 1 char)').upper()
                if helpers.validate_dni(dni, db.Clients.list):
                    break

            name = helpers.read_text(1, 50, 'Enter Name (from 2 to 50 chars)').capitalize()
            lastname = helpers.read_text(1, 50, 'Enter Lastname (from 2 to 50 chars)').capitalize()
            db.Clients.add(dni, name, lastname)
            print('Client added!')

        elif option == '4':
            print('Editing client...\n')
            dni = helpers.read_text(9, 9, 'Enter DNI (8 int and 1 char)').upper()
            client = db.Clients.search(dni)
            if client:
                name = helpers.read_text(1, 50, f'Enter Name (from 2 to 50 chars) [{client.name}]').capitalize()
                lastname = helpers.read_text(1, 50, f'Enter Lastname (from 2 to 50 chars [{client.lastname}])').capitalize()
                db.Clients.edit(client.dni, name, lastname)
                print('Client edited!')
            else:
                print('Client not found')

        elif option == '5':
            print('Deleting client...\n')
            dni = helpers.read_text(9, 9, 'Enter DNI (8 int and 1 char)').upper()
            print('Client deleted!') if db.Clients.delete(dni) else print('Client not found')
        elif option == '6':
            print('Goodbye!\n')
            break
        else:
            print('Invalid option')

        input('\nPress Enter to continue...')
