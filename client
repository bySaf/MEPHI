import math, socket

HOST = ("192.168.11.103", 9090)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)
print("Connected to", HOST)

msg = client.recv(1024)
print(msg.decode('UTF-8'))

arr = list(map(int, msg.split()))

x, y = arr[0], arr[1]
