import os

global DbVar

class database():
   def __init__(self):
      self.database = []
      self.node = []
      self.TxMessage = []
      self.TxMessageIndex = []
      self.TxMessageSignal = []
      self.RxMessage = []
      self.RxMessageIndex = []
      self.RxMessageSignal = []


def InitDb():
   global DbVar
   DbVar = database() 
   return DbVar


def db():
   global DbVar
   return DbVar

