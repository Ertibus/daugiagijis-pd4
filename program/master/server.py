# ./program/master/server.py

import socket
import sys

import time
import threading

class Server:
    host = "localhost"
    port = 6060
    server_socket = socket.socket()

    NUMBER_OF_THREADS = 5
    active_connections = []
    active_addresses = []

    def start(self):
        self.bind_socket()
        
        connection_thread = threading.Thread(target=self.accept_connections)
        connection_thread.deamon = True
        connection_thread.start()

        master_thread = threading.Thread(target=self.send_msg_all)
        master_thread.deamon = True
        master_thread.start()

    def bind_socket(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

        except socket.error as err:
            print("Socket Binding error: " + str(err) + ",\t Retrying...")
            self.bind_socket()

    def accept_connections(self):
        self.close_connections()

        while True:
            connection, address = self.server_socket.accept()

            self.active_connections.append(connection)
            self.active_addresses.append(address)

            print("\nConnection established with: [ {}:{} ]".format(address[0], address[1]))

            connection.send("hello client".encode('utf-8'))

            if len(self.active_connections) == 0:
                break
    def close_connections(self):
        for conn in self.active_connections:
            conn.close()
        del self.active_connections[:]
        del self.active_addresses[:]

    def send_msg_all(self):
        while True:
            msg = input("Message to send:")
            if msg == 'quit':
                self.close_connections()
                break;
            for connection in self.active_connections:
                connection.send(msg.encode('utf-8'))
        
    def send_image(self):
        with open("./images/1Text.jpg", 'rb'):
            pass

if __name__ == '__main__':
    server = Server()
    server.start()

