import os
from tkinter import *

from contacts import *

contacts_file = 'contacts.txt'


class Contacts:
    def selection(self):
        print("At %s of %d" % (self.select.curselection(), len(self.contacts)))
        return int(self.select.curselection()[0])

    def addContact(self):
        self.contacts.append([self.nameVar.get(), self.phoneVar.get()])
        self.setList()

    def updateContact(self):
        self.contacts[self.selection()] = [self.nameVar.get(), self.phoneVar.get()]
        self.setList()

    def deleteContact(self):
        del self.contacts[self.selection()]
        self.setList()

    def loadContact(self):
        name, phone = self.contacts[self.selection()]
        self.nameVar.set(name)
        self.phoneVar.set(phone)

    def __init__(self, contactsList, path):
        self.contacts = contactsList
        self.path = path

        self.root = Tk()

        self.root.winfo_toplevel().title("My Contact List")

        self.framebuttons = Frame(self.root)
        self.framebuttons.pack(fill=BOTH, expand=YES)

        Label(self.framebuttons, text="Name:").grid(row=0, column=0, sticky=N)
        self.nameVar = StringVar()
        self.name = Entry(self.framebuttons, textvariable=self.nameVar)
        self.name.grid(row=0, column=1, sticky=W)

        Label(self.framebuttons, text="Phone:").grid(row=1, column=0, sticky=N)
        self.phoneVar = StringVar()
        self.phone = Entry(self.framebuttons, textvariable=self.phoneVar)
        self.phone.grid(row=1, column=1, sticky=N)

        self.framebuttons = Frame(self.root)  # add a row of buttons
        self.framebuttons.pack()
        self.btn1 = Button(self.framebuttons, text=" Add  ", command=self.addContact)
        self.btn2 = Button(self.framebuttons, text="Update", command=self.updateContact)
        self.btn3 = Button(self.framebuttons, text="Delete", command=self.deleteContact)
        self.btn4 = Button(self.framebuttons, text=" Load ", command=self.loadContact)
        self.btn5 = Button(self.framebuttons, text=" Save ", command=self.setList)

        self.btn1.pack(side=LEFT)
        self.btn2.pack(side=LEFT)
        self.btn3.pack(side=LEFT)
        self.btn4.pack(side=LEFT)
        self.btn5.pack(side=LEFT)

        self.framebuttons = Frame(self.root)  # allow for selection of names
        self.framebuttons.pack()
        self.scroll = Scrollbar(self.framebuttons, orient=VERTICAL)
        self.select = Listbox(self.framebuttons, yscrollcommand=self.scroll.set, height=7)
        self.scroll.config(command=self.select.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.select.pack(side=LEFT, fill=BOTH)

        self.setList()

    def setList(self):
        self.contacts.sort()
        self.select.delete(0, END)
        for name, phone in self.contacts:
            self.select.insert(END, name)

        with open(self.path, 'w') as f:

            print("Writing list to file at '" + self.path + "'.")

            for contact in self.contacts:
                line = ','.join(contact)
                f.write(line + '\n')


def contactFromLine(line: str):
    lines = line.split(',')

    fname = lines[0]
    lname = lines[1]
    pn = lines[2]

    ret = [(fname + ', ' + lname), pn]
    print(ret)
    return ret


def loadListFromFile(path: str):
    ret = []
    with open(path, 'r') as f:
        for line in f:
            line = line.replace('\r', '').replace('\n', '')
            ret.append(contactFromLine(line))
    return ret


if __name__ == '__main__':
    if os.path.exists(contacts_file):
        print("'" + contacts_file + "' exists! Loading values from it...")
        contactlist = loadListFromFile(contacts_file)

    contacts = Contacts(contactlist, contacts_file)

    contacts.root.mainloop()
