#!/usr/bin/env python3

###########################################
# DATA BASE APP                           #
# NAME: E-LIBRARY 2022                    #
# AUTHORS: JAKUB SZYMKOWIAK, JAKUB SCHMID #
######################################### #

from tkinter import *

from driver import Driver

root = Tk()
root.title("Biblioteka")
root.geometry('800x800')

canvas = Canvas(root, height = 180, width = 500)

driver = Driver(canvas)
driver.infoPanel()

infoPanel = Button(root,
                   text = "Informacje o aplikacji",
                   width=20, height=1,
                   fg="white", bg="#263D42",
                   command = driver.infoPanel)
infoPanel.pack()

bookSearcher = Button(root,
                      text = "Wyszukiwanie książek",
                      width = 20, height = 1,
                      fg = "white", bg = "#263D42",
                      command = driver.searchBook)
bookSearcher.pack()

addBook = Button(root,
                 text = "Dodawanie książek",
                 width = 20, height = 1,
                 fg = "white", bg = "#263D42",
                 command = driver.addBook)
addBook.pack()

userSearcher = Button(root,
                      text="Przeglądanie użytkowników",
                      width = 20, height = 1,
                      fg = "white", bg = "#263D42",
                      command = driver.searchUser)
userSearcher.pack()

userAdd = Button(root,
                      text="Dodawanie użytkowników",
                      width = 20, height = 1,
                      fg = "white", bg = "#263D42",
                      command = driver.addUser)
userAdd.pack()

changeUser = Button(root,
                      text="Wypożyczenia",
                      width = 20, height = 1,
                      fg = "white", bg = "#263D42",
                      command = driver.changeUser)
changeUser.pack()

returnBook = Button(root,
                      text="Zwroty",
                      width = 20, height = 1,
                      fg = "white", bg = "#263D42",
                      command = driver.returnBook)
returnBook.pack()

login = Button(root,
                      text="Zaloguj się",
                      width = 20, height = 1,
                      fg = "white", bg = "#263D42",
                      command = driver.login)
login.pack()

logout = Button(root,
                      text="Wyloguj się",
                      width = 20, height = 1,
                      fg = "white", bg = "#263D42",
                      command = driver.logout)
logout.pack()
driver.root.pack()


root.mainloop()
