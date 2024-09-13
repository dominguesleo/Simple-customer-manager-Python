import database as db
import helpers
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")


class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Create Client')
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack( padx=20, pady=10)

        Label(frame, text='DNI (8 int and 1 upper char)').grid(row=0, column=0)
        Label(frame, text='Name (from 2 to 50 chars)').grid(row=0, column=1)
        Label(frame, text='Last Name (from 2 to 50 chars)').grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind('<KeyRelease>', lambda event: self.validate(event, 0))

        name = Entry(frame)
        name.grid(row=1, column=1)
        name.bind('<KeyRelease>', lambda event: self.validate(event, 1))

        lastname = Entry(frame)
        lastname.grid(row=1, column=2)
        lastname.bind('<KeyRelease>', lambda event: self.validate(event, 2))

        frame = Frame(self)
        frame.pack(pady=10)

        create = Button(frame, text='Create', command=self.create_client)
        create.configure(state=DISABLED)
        create.grid(row=0, column=0)
        Button(frame, text='Cancel', command=self.close).grid(row=0, column=1)

        self.correct_fields = [0, 0, 0]
        self.create = create
        self.dni = dni
        self.name = name
        self.lastname = lastname

    def create_client(self):
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(),
            values=(self.dni.get(), self.name.get(), self.lastname.get())
        )
        db.Clients.add(self.dni.get(), self.name.get(), self.lastname.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        value = event.widget.get()
        valid = helpers.validate_dni(value, db.Clients.list) if index == 0 \
            else (value.isalpha() and len(value) >= 2 and len(value) <= 50)
        event.widget.configure(bg = 'green' if valid else 'red')

        self.correct_fields[index] = valid
        self.create.configure(state=NORMAL if self.correct_fields == [1, 1, 1] else DISABLED)

class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Edit Client')
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack( padx=20, pady=10)

        Label(frame, text='DNI (not editable )').grid(row=0, column=0)
        Label(frame, text='Name (from 2 to 50 chars)').grid(row=0, column=1)
        Label(frame, text='Last Name (from 2 to 50 chars)').grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)
        name = Entry(frame)
        name.grid(row=1, column=1)
        name.bind('<KeyRelease>', lambda event: self.validate(event, 0))
        lastname = Entry(frame)
        lastname.grid(row=1, column=2)
        lastname.bind('<KeyRelease>', lambda event: self.validate(event, 1))

        client = self.master.treeview.focus()
        data = self.master.treeview.item(client, 'values')
        dni.insert(0, data[0])
        dni.configure(state=DISABLED)
        name.insert(0, data[1])
        lastname.insert(0, data[2])

        frame = Frame(self)
        frame.pack(pady=10)

        edit = Button(frame, text='Update', command=self.edit_client)
        edit.grid(row=0, column=0)
        Button(frame, text='Cancel', command=self.close).grid(row=0, column=1)

        self.correct_fields = [1, 1]
        self.edit = edit
        self.dni = dni
        self.name = name
        self.lastname = lastname

    def edit_client(self):
        client = self.master.treeview.focus()
        self.master.treeview.item(client, values=(self.dni.get(), self.name.get(), self.lastname.get()))
        db.Clients.edit(self.dni.get(), self.name.get(), self.lastname.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        value = event.widget.get()
        valid = (value.isalpha() and len(value) >= 2 and len(value) <= 50)
        event.widget.configure(bg = 'green' if valid else 'red')

        self.correct_fields[index] = valid
        self.edit.configure(state=NORMAL if self.correct_fields == [1, 1] else DISABLED)


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Customer Manager')
        self.build()
        self.center()

    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Name', 'Last Name')

        treeview.column('#0', width=0, stretch=NO)
        treeview.column('DNI', anchor=CENTER)
        treeview.column('Name', anchor=CENTER)
        treeview.column('Last Name', anchor=CENTER)

        treeview.heading('DNI', text='DNI', anchor=CENTER)
        treeview.heading('Name', text='Name', anchor=CENTER)
        treeview.heading('Last Name', text='Last Name', anchor=CENTER)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview['yscrollcommand'] = scrollbar.set

        for client in db.Clients.list:
            treeview.insert(
                parent='', index='end', iid=client.dni,
                values=(client.dni, client.name, client.lastname)
            )

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text='Add', command=self.add).grid(row=0, column=0)
        Button(frame, text='Edit', command=self.edit).grid(row=0, column=1)
        Button(frame, text='Delete', command=self.delete).grid(row=0, column=2)

        self.treeview = treeview

    def delete(self):
        client = self.treeview.focus()
        if client:
            data = self.treeview.item(client, 'values')
            confirm = askokcancel(
                title='Delete',
                message=f'Are you sure you want to delete {data[0]} {data[1]} {data[2]}?',
                icon=WARNING)
            if confirm:
                self.treeview.delete(client)
                db.Clients.delete(data[0])

    def add(self):
        CreateClientWindow(self)

    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)


if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()