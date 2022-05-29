###########################################
# DATA BASE APP                           #
# NAME: E-LIBRARY 2022                    #
# AUTHORS: JAKUB SZYMKOWIAK, JAKUB SCHMID #
######################################### #

class User:

  def __init__(self, surname, email, address, phoneNumber, copies):
    self.surname     = surname
    self.email       = email
    self.address     = address
    self.phoneNumber = phoneNumber
    self.copies      = copies

