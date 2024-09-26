import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
    # msg = input('Введите сообщение\n')
# while msg != 'exit':
sock.connect(('192.168.0.108', 56943))
msg = input('Введите сообщение\n')
sock.send(msg.encode('utf-8'))
data = sock.recv(1024).decode('utf-8')
print(str(data))
sock.close()
# except:
#     print('Подключение прервано')