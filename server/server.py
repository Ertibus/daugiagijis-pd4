# ./program/master/server.py

import socket
import io

import time
import threading

from PIL import Image

class Server:

    RETRY_COUNT = 5
    WORK_SIZE = 5
    BUFFER_SIZE = 4096

    host = "localhost"
    port = 6060
    server_socket = socket.socket()

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

    def bind_socket(self, attempt=0):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

        except socket.error as err:
            if self.RETRY_COUNT > attempt:
                print("Socket Binding error: " + str(err) + ", Retrying...")
                self.bind_socket(attempt+1)
            else:
                raise Exception("Socket Binding error: " + str(err) + ", Max Retry tries reached. :(")


    def accept_connections(self):
        self.close_connections()

        while True:
            connection, address = self.server_socket.accept()

            client_id = len(self.active_connections)

            self.active_connections.append(connection)
            self.active_addresses.append(address)

            print("Connection established with: [ {}:{} ]\n".format(address[0], address[1]))
            connection.send("hello_client {}".format(client_id).encode('utf-8'))

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
                break
            elif msg == 'send_image':
                self.send_images()
                continue
            for connection in self.active_connections:
                connection.send(msg.encode('utf-8'))
        
    def send_images(self):
        for i, connection in enumerate(self.active_connections):
            connection.send("send work".encode('utf-8'))

            for ii in range(5):                
                data = connection.recv(self.BUFFER_SIZE)
                if data.decode('utf-8') == 'ready':
                    connection.send("catch".encode('utf-8'))

                    img = Image.open(f'./images/{ii + 1}Text.jpg')
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG')
                    connection.send(buffer.getvalue())

            data = connection.recv(self.BUFFER_SIZE)
            if data.decode('utf-8') == 'ready':
                connection.send("end".encode('utf-8'))
            

if __name__ == '__main__':
    server = Server()
    try:
        server.start()
    except Exception as err:
        print(err)

