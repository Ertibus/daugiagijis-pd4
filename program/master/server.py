# ./program/master/server.py

import socket
import sys
import io
try:
    from PIL import Image
except ImportError:
    import Image

class Server:
    host = "localhost"
    port = 6060
    server_socket = socket.socket()

    def bind_socket(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

        except socket.error as err:
            print("Socket Binding error: " + str(err) + ",\t Retrying...")
            self.bind_socket()

    def socket_accept(self):
        print("Waiting for client to connect")

        connection, address = self.server_socket.accept()
        print("Connection established with:\t{}:{}".format(address[0], address[1]))

        connection.send("hello client".encode('utf-8'))
        
        data = connection.recv(4096)
        if data.decode('utf-8') == "give file":
            with open("./images/1Text.jpg", 'rb') as file:
                data = file.read()
                connection.send(data)
                pass
            print("File established!")

        self.send_image()
        
        connection.close()

    def send_image(self):
        with open("./images/1Text.jpg", 'rb'):
            pass

if __name__ == '__main__':
    server = Server()
    server.bind_socket()
    server.socket_accept()

