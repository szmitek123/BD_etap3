###########################################
# DATA BASE APP                           #
# NAME: E-LIBRARY 2022                    #
# AUTHORS: JAKUB SZYMKOWIAK, JAKUB SCHMID #
######################################### #

from SQLConnector import *
from book import Book
from user import User
from copy import Copy
from datetime import datetime, timedelta


class Library:

    def __init__(self):
        self.connection = connect(host="127.0.0.1",
                                  username="root",
                                  password="mysql12345",
                                  database="bazadanych3")

    def selectBooks(self, userdata):
        allResults = []

        query = f"""SELECT * FROM Book WHERE title='{str(userdata)}' OR genre='{str(userdata)}';"""
        foundBooks = readData(self.connection, query)
        if len(foundBooks) != 0:
            for item in foundBooks:
                id = item[0]
                title = str(item[1])
                genre = item[2]
                year = item[3]
                mark = item[4]
                publisherID = item[5]
                authorID = item[6]
                query = f"""SELECT publisher, city FROM PublisherHouse WHERE idPublisher={str(publisherID)}"""
                publisherData = readData(self.connection, query)
                publisher = publisherData
                city = publisherData[0][1]
                query = f"""SELECT surname FROM Author WHERE idAuthor={str(authorID)}"""
                author = readData(self.connection, query)
                query = f"""SELECT * FROM Copy WHERE Book_idBook={str(id)}"""
                copiesRaw = readData(self.connection, query)
                copies = []
                for item in copiesRaw:
                    idCopy = item[0]
                    dateRent = item[1]
                    dateReturn = item[2]
                    isRented = item[3]
                    copies.append(Copy(dateReturn, dateRent, isRented, idCopy, title, author[0][0]))
                author = author[0][0]
                publisher = publisher[0][0]
                allResults.append(Book(title, genre, str(year), mark, publisher, city, author, copies))

        query = f"""SELECT idAuthor, surname FROM Author WHERE surname='{str(userdata)}' OR origin='{str(userdata)}';"""
        foundAuthors = readData(self.connection, query)
        if len(foundAuthors) != 0:
            for item in foundAuthors:
                id = item[0]
                author = item[1]
                query = f"""SELECT * FROM Book WHERE Author_idAuthor='{str(id)}';"""
                foundBooks = readData(self.connection, query)
                for item in foundBooks:
                    idBook = item[0]
                    title = str(item[1])
                    genre = item[2]
                    year = item[3]
                    mark = item[4]
                    publisherID = item[5]
                    query = f"""SELECT publisher, city FROM PublisherHouse WHERE idPublisher={str(publisherID)}"""
                    publisherData = readData(self.connection, query)
                    publisher = publisherData
                    publisherCity = publisher[0][1]
                    query = f"""SELECT * FROM Copy WHERE Book_idBook={str(idBook)}"""
                    copiesRaw = readData(self.connection, query)
                    copies = []
                    for item in copiesRaw:
                        idCopy = item[0]
                        dateRent = item[1]
                        dateReturn = item[2]
                        isRented = item[3]
                        copies.append(Copy(dateReturn, dateRent, isRented, idCopy, title, author))
                    publisher = publisher[0][0]
                    allResults.append(Book(title, genre, str(year), mark, publisher, publisherCity, author, copies))
        query = f"""SELECT idPublisher, publisher, city FROM PublisherHouse WHERE publisher='{str(userdata)}';"""
        foundPublishers = readData(self.connection, query)
        if len(foundPublishers) != 0:
            for item in foundPublishers:
                id = item[0]
                publisher = item[1]
                city = item[2]
                query = f"""SELECT * FROM Book WHERE PublisherHouse_idPublisher='{str(id)}';"""
                foundBooks = readData(self.connection, query)
                for item in foundBooks:
                    idBook = item[0]
                    title = str(item[1])
                    genre = item[2]
                    year = item[3]
                    mark = item[4]
                    authorID = item[6]
                    query = f"""SELECT surname FROM Author WHERE idAuthor='{str(authorID)}';"""
                    author = readData(self.connection, query)
                    query = f"""SELECT * FROM Copy WHERE Book_idBook={str(idBook)}"""
                    copiesRaw = readData(self.connection, query)
                    copies = []
                    for item in copiesRaw:
                        idCopy = item[0]
                        dateRent = item[1]
                        dateReturn = item[2]
                        isRented = item[3]
                        copies.append(Copy(dateReturn, dateRent, isRented, idCopy, title, author[0][0]))
                    author = author[0][0]
                    allResults.append(Book(title, genre, str(year), mark, publisher, city, author, copies))
        allResults.sort(key=lambda x: x.mark, reverse=True)
        return allResults

    def selectUser(self, userdata):
        allResults = []
        query = f"SELECT * FROM Reader WHERE surname='{str(userdata)}' OR email='{str(userdata)}';"
        foundUsers = readData(self.connection, query)
        if len(foundUsers) != 0:
            for user in foundUsers:
                idUser = user[0]
                surname = user[1]
                email = user[2]
                address = user[3]
                phoneNumber = user[4]
                query = f"""SELECT * FROM Copy WHERE Reader_IdReader={idUser};"""
                copiesRaw = readData(self.connection, query)
                copies = []
                for item in copiesRaw:
                    idCopy = item[0]
                    dateRent = item[1]
                    dateReturn = item[2]
                    isRented = item[3]
                    book_IdBook = item[5]
                    query = f"""SELECT Author_idAuthor, title FROM Book WHERE idBook={book_IdBook};"""
                    foundData = readData(self.connection, query)
                    for item in foundData:
                        idAuthor = item[0]
                        title = item[1]
                        query = f"""SELECT surname FROM Author WHERE idAuthor={idAuthor}"""
                        author = readData(self.connection, query)
                        author = author[0][0]
                    copies.append(Copy(dateReturn, dateRent, isRented, idCopy, title, author))

                allResults.append(User(surname, email, address, phoneNumber, copies))

        '''query = f"SELECT * FROM Reader WHERE email='{str(userdata)}';"
        foundUsers = readData(self.connection, query)
        if len(foundUsers) != 0:
          for user in foundUsers:
            allResults.append(user)'''

        return allResults

    def insertBook(self, authorName, authorOrigin, title, year, genre, publisherName, publisherCity, mark,
                   numberOfCopies):
        query = f"""SELECT surname FROM Author WHERE surname='{authorName}';"""
        foundAuthor = readData(self.connection, query)
        if len(foundAuthor) == 0:
            query = f"""INSERT INTO Author (surname, origin) VALUES ('{authorName}', '{authorOrigin}');"""
            ret = executeQuery(self.connection, query)

        query = f"""SELECT publisher FROM PublisherHouse WHERE publisher='{publisherName}';"""
        foundPublisher = readData(self.connection, query)
        if len(foundPublisher) == 0:
            query = f"""INSERT INTO PublisherHouse (publisher, city) VALUES ('{publisherName}', '{publisherCity}');"""
            ret = executeQuery(self.connection, query)

        query = f"""SELECT title FROM Book WHERE title='{title}' AND yearPublish={year} AND genre='{genre}';"""
        foundBook = readData(self.connection, query)
        if len(foundBook) == 0:
            query = f"""SELECT idPublisher FROM PublisherHouse WHERE publisher='{publisherName}' AND city='{publisherCity}';"""
            idPublisher = readData(self.connection, query)
            query = f"""SELECT idAuthor FROM Author WHERE surname='{authorName}' AND origin='{authorOrigin}';"""
            idAuthor = readData(self.connection, query)
            query = f"""INSERT INTO Book (title, genre, yearPublish, mark, PublisherHouse_idPublisher, Author_idAuthor) 
                  VALUES ('{title}', '{genre}', '{year}', {str(mark)}, '{idPublisher[0][0]}', '{idAuthor[0][0]}');"""
            executeQuery(self.connection, query)
            query = f"""SELECT idBook FROM Book WHERE title='{title}' AND yearPublish={year} AND genre='{genre}';"""
            idBook = readData(self.connection, query)
            idBook = idBook[0][0]
            i = 0
            today = datetime.now()
            deadline = today + timedelta(days=30)
            for i in range(int(numberOfCopies)):
                query = f"""INSERT INTO Copy (dateRent, dateReturn, isRented, Reader_idReader, Book_idBook) 
                    VALUES ('{today.strftime("%Y-%m-%d")}', '{deadline.strftime("%Y-%m-%d")}', 0, 1, {idBook});"""
                executeQuery(self.connection, query)

    def insertUser(self, userName, userEmail, userAddress, userPhoneNumber):
        query = f"""SELECT surname FROM Reader WHERE surname='{userName}';"""
        foundUser = readData(self.connection, query)
        if len(foundUser) == 0:
            query = f"""INSERT INTO Reader (surname, email, address, phoneNumber) VALUES ('{userName}', '{userEmail}','{userAddress}', '{userPhoneNumber}');"""
            executeQuery(self.connection, query)

    def login(self, username, password):
        query = f"""SELECT * FROM Librarian WHERE login='{username}' AND passwd='{password}';"""
        librarian = readData(self.connection, query)
        if len(librarian) == 0:
            return False
        return True

    def changeUser(self, title, author, email):
        query = f"""SELECT idAuthor FROM Author WHERE surname='{author}';"""
        idAuthor = readData(self.connection, query)
        idAuthor = idAuthor[0][0]
        query = f"""SELECT idBook FROM Book WHERE title='{title}' AND Author_idAuthor='{idAuthor}';"""
        idBook = readData(self.connection, query)
        idBook = idBook[0][0]
        query = f"""SELECT * FROM Copy WHERE Book_idBook={idBook} AND isRented=0;"""
        availableCopies = readData(self.connection, query)
        if len(availableCopies) != 0:
            query = f"""SELECT idReader FROM Reader WHERE email='{email}';"""
            idReader = readData(self.connection, query)
            idReader = idReader[0][0]
            idCopy = availableCopies[0][0]
            today = datetime.now()
            deadline = today + timedelta(days=30)
            query = f"""UPDATE Copy 
                  SET isRented=1, Reader_idReader={idReader}, dateRent='{today.strftime("%Y-%m-%d")}', dateReturn='{deadline.strftime("%Y-%m-%d")}'
                  WHERE idCopy={idCopy};"""
            return executeQuery(self.connection, query)
        else:
            return False

    def returnBook(self, title, author, email):
        query = f"""SELECT idAuthor FROM Author WHERE surname='{author}';"""
        idAuthor = readData(self.connection, query)
        idAuthor = idAuthor[0][0]
        query = f"""SELECT idBook FROM Book WHERE title='{title}' AND Author_idAuthor='{idAuthor}';"""
        idBook = readData(self.connection, query)
        idBook = idBook[0][0]
        query = f"""SELECT * FROM Copy WHERE Book_idBook={idBook} AND isRented=1;"""
        nonavailableCopies = readData(self.connection, query)
        if len(nonavailableCopies) != 0:
            query = f"""SELECT idReader FROM Reader WHERE email='{email}';"""
            idReader = readData(self.connection, query)
            idReader = idReader[0][0]
            idCopy = nonavailableCopies[0][0]
            query = f"""UPDATE Copy 
                  SET isRented=0, Reader_idReader=NULL, dateRent='{datetime.now().strftime("%Y-%m-%d")}', dateReturn='{datetime.now().strftime("%Y-%m-%d")}'
                  WHERE idCopy={idCopy};"""
            return executeQuery(self.connection, query)
        else:
            return False


