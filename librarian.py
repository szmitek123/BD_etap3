###########################################
# DATA BASE APP                           #
# NAME: E-LIBRARY 2022                    #
# AUTHORS: JAKUB SZYMKOWIAK, JAKUB SCHMID #
######################################### #

class Librarian:
  def __init__(self, surname, login, passwd) -> None:
      self.surname = surname
      self.login = login
      self.password = passwd