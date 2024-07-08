from threading import Thread
from serv import bezdarnost

def start(x, y):
  thread1 = Thread(target=bezdarnost, args=(x1, x2))
  thread1.start()
