###########################################
# DATA BASE APP                           #
# NAME: E-LIBRARY 2022                    #
# AUTHORS: JAKUB SZYMKOWIAK, JAKUB SCHMID #
######################################### #

from tkinter import *

from library import Library
from book import *


class Driver:
    def __init__(self, root):
        self.lib = Library()
        self.root = Canvas()
        self.root = root

        self.librarianLoggedIn = False

        self.entryForBooks = Entry(self.root)

        self.entryForUsers = Entry(self.root)

        self.canvas = Canvas(self.root, height=180, width=500)
        self.scrollbar = Scrollbar(self.root)
        self.list = Listbox(self.root, yscrollcommand=self.scrollbar.set)

    def search():
        return 0

    def insertBook():
        return 0

    def insertUser():
        return 0

    def searchUserButtonHandler(self):

        self.scrollbar.destroy()
        self.list.destroy()

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        foundUsers = self.lib.selectUser(self.entryForUsers.get())

        self.list = Listbox(self.root, yscrollcommand=self.scrollbar.set, width=200)

        for user in foundUsers:
            self.list.insert(END, "Imię i nazwisko: " + user.surname)
            self.list.insert(END, "Email: " + user.email)
            self.list.insert(END, "Adres: " + user.address)
            self.list.insert(END, "Numer telefonu: " + user.phoneNumber)
            self.list.insert(END, "Wypożyczone książki:")
            for copy in user.copies:
                self.list.insert(END, copy.author + ", " + copy.title)
                self.list.insert(END, str(copy.dateRent) + " - " + str(copy.dateOfReturn))

        self.list.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.list.yview)

    def searchBookButtonHandler(self):

        self.scrollbar.destroy()
        self.list.destroy()

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        foundBooks = self.lib.selectBooks(self.entryForBooks.get())

        self.list = Listbox(self.root, yscrollcommand=self.scrollbar.set, width=200)

        for book in foundBooks:
            book.title.split()
            self.list.insert(END, "Tytuł: " + book.title)
            self.list.insert(END, "Autor: " + book.author)
            self.list.insert(END, "Gatunek: " + book.genre)
            self.list.insert(END, "Rok wydania: " + book.year)
            self.list.insert(END, "Wydawca: " + book.publisher + ", " + book.city)
            self.list.insert(END, "Ocena: " + str(book.mark))
            numberOfCopies = len(book.copies)
            availableCopies = 0
            for copy in book.copies:
                if copy.isRented == 0:
                    availableCopies += 1
            self.list.insert(END, "Kopie: " + str(numberOfCopies) +
                             ", w tym dostępne: " + str(availableCopies))
            self.list.insert(END, "")

        self.list.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.list.yview)

    def addBookButtonHandler(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.root, height=180, width=500)
        self.canvas.pack()

        self.lib.insertBook(self.author.get(),
                            self.origin.get(),
                            self.title.get(),
                            self.year.get(),
                            self.genre.get(),
                            self.publisherName.get(),
                            self.publisherCity.get(),
                            self.numberOfCopies.get())

        Label(self.canvas, text="Książka została dodana do bazy").pack()

    def addUserButtonHandler(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.root, height=180, width=500)
        self.canvas.pack()

        self.lib.insertUser(self.name.get(),
                            self.email.get(),
                            self.address.get(),
                            self.phoneNumber.get())
        Label(self.canvas, text="Użytkownik został dodany do bazy").pack()

    def loginButtonHandler(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.root, height=180, width=500)
        self.canvas.pack()

        result = self.lib.login(self.username.get(), self.password.get())
        if result == True:
            self.librarianLoggedIn = True
            Label(self.root, text="Bibliotekarz został zalogowany").pack()
        else:
            Label(self.root, text="Niewłaściwa nazwa użytkownika lub hasło").pack()

    def changeUserButtonHandler(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.root, height=180, width=500)
        self.canvas.pack()

        result = self.lib.changeUser(self.title.get(), self.author.get(), self.userEmail.get())

        if result == True:
            Label(self.root, text="Operacja zakończona powodzeniem").pack()
        else:
            Label(self.root, text="Operacja nie powiodła się").pack()

    def returnBookButtonHandler(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.root, height=180, width=500)
        self.canvas.pack()

        result = self.lib.returnBook(self.title.get(), self.author.get(), self.userEmail.get())

        if result == True:
            Label(self.root, text="Operacja zakończona powodzeniem").pack()
        else:
            Label(self.root, text="Operacja nie powiodła się").pack()

    def searchBook(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.entryForBooks = Entry(self.root)
        self.entryForBooks.pack()

        searchBookButton = Button(self.root,
                                  text="Szukaj",
                                  width=20, height=1,
                                  fg="white", bg="#263D42",
                                  command=self.searchBookButtonHandler)
        searchBookButton.pack()

    def searchUser(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if self.librarianLoggedIn:
            self.entryForUsers = Entry(self.root)
            self.entryForUsers.pack()

            searchUserButton = Button(self.root,
                                      text="Szukaj",
                                      width=20, height=1,
                                      fg="white", bg="#263D42",
                                      command=self.searchUserButtonHandler)
            searchUserButton.pack()
        else:
            Label(self.root, text="Wymagane uprawnienia bibliotekarza").pack()
            Label(self.root, text="Zaloguj się, aby przeglądać użytkowników").pack()

    def changeUser(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.librarianLoggedIn:
            Label(self.root, text="Tytuł").pack()
            self.title = Entry(self.root)
            self.title.pack()
            Label(self.root, text="Autor").pack()
            self.author = Entry(self.root)
            self.author.pack()
            Label(self.root, text="Email użytkownika").pack()
            self.userEmail = Entry(self.root)
            self.userEmail.pack()

            changeUserButton = Button(self.root,
                                      text="Zatwierdź",
                                      width=20, height=1,
                                      fg="white", bg="#263D42",
                                      command=self.changeUserButtonHandler)
            changeUserButton.pack()
        else:
            Label(self.root, text="Wymagane uprawnienia bibliotekarza").pack()
            Label(self.root, text="Zaloguj się, aby móc zmienić aktualnego użytkownika książki")

    def returnBook(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.librarianLoggedIn:
            Label(self.root, text="Tytuł").pack()
            self.title = Entry(self.root)
            self.title.pack()
            Label(self.root, text="Autor").pack()
            self.author = Entry(self.root)
            self.author.pack()
            Label(self.root, text="Email użytkownika").pack()
            self.userEmail = Entry(self.root)
            self.userEmail.pack()

            returnBookButton = Button(self.root,
                                      text="Zatwierdź",
                                      width=20, height=1,
                                      fg="white", bg="#263D42",
                                      command=self.returnBookButtonHandler)
            returnBookButton.pack()
        else:
            Label(self.root, text="Wymagane uprawnienia bibliotekarza").pack()
            Label(self.root, text="Zaloguj się, aby móc zmienić aktualnego użytkownika książki")

    def addBook(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.librarianLoggedIn:
            Label(self.root, text="Autor").pack()

            self.author = Entry(self.root)
            self.author.pack()

            Label(self.root, text="Kraj pochodzenia autora").pack()
            self.origin = Entry(self.root)
            self.origin.pack()
            Label(self.root, text="Tytuł").pack()

            self.title = Entry(self.root)
            self.title.pack()

            Label(self.root, text="Rok wydania").pack()

            self.year = Entry(self.root)
            self.year.pack()

            Label(self.root, text="Gatunek").pack()

            self.genre = Entry(self.root)
            self.genre.pack()

            Label(self.root, text="Wydawca").pack()

            self.publisherName = Entry(self.root)
            self.publisherName.pack()

            Label(self.root, text="Miasto").pack()

            self.publisherCity = Entry(self.root)
            self.publisherCity.pack()

            Label(self.root, text="Liczba kopii").pack()

            self.numberOfCopies = Entry(self.root)
            self.numberOfCopies.pack()

            addBookButton = Button(self.root,
                                   text="Dodaj",
                                   width=20, height=1,
                                   fg="white", bg="#263D42",
                                   command=self.addBookButtonHandler)
            addBookButton.pack()
        else:
            Label(self.root, text="Wymagane uprawnienia bibliotekarza").pack()
            Label(self.root, text="Zaloguj się, aby dodać nową książkę").pack()

    def addUser(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.librarianLoggedIn:
            Label(self.root, text="Imię i nazwisko").pack()
            self.name = Entry(self.root)
            self.name.pack()
            Label(self.root, text="Email").pack()
            self.email = Entry(self.root)
            self.email.pack()
            Label(self.root, text="Adres").pack()
            self.address = Entry(self.root)
            self.address.pack()
            Label(self.root, text="Numer telefonu").pack()
            self.phoneNumber = Entry(self.root)
            self.phoneNumber.pack()
            addUserButton = Button(self.root,
                                   text="Dodaj",
                                   width=20, height=1,
                                   fg="white", bg="#263D42",
                                   command=self.addUserButtonHandler)
            addUserButton.pack()
        else:
            Label(self.root, text="Wymagane uprawnienia bibliotekarza").pack()
            Label(self.root, text="Zaloguj się, aby dodać nowych użytkowników").pack()

    def login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Login").pack()

        self.username = Entry(self.root)
        self.username.pack()

        Label(self.root, text="Hasło").pack()

        self.password = Entry(self.root)
        self.password.pack()

        loginButton = Button(self.root,
                             text="Dalej",
                             width=20, height=1,
                             fg="white", bg="#263D42",
                             command=self.loginButtonHandler)
        loginButton.pack()

    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.librarianLoggedIn = False
        Label(self.root, text="Bibliotekarz został wylogowany").pack()

    def infoPanel(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Jakub Szymkowiak, Jakub Schmid").pack()
        Label(self.root, text="E-Biblioteka 2022").pack()