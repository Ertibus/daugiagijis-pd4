# ./program/master/server.py

import socket
import io
import os
import math

import time
import threading

from PIL import Image

class Server:

    RETRY_COUNT = 5
    RETRY_WAIT = 2 #seconds
    WORK_SIZE = 5
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    host = "localhost"
    port = 6060
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_list = []

    processed= 0 # 0 - Listening, 1 - Processing

#           START METHODS
    def start(self):
        self._work_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._socket_lock = threading.Lock()
        self.bind_socket()

        directory='./images'
        self.image_paths = self.get_image_paths(directory)
        self.create_work()


        with open('out/results.txt', 'w') as fd:
            pass
        
        connection_thread = threading.Thread(target=self.accept_connections)
        connection_thread.start()

        #time.sleep(5)


    def get_image_paths(self, dir_path):
        file_list = []
        for file in os.listdir(dir_path):
            file_list.append(dir_path + "/" + file)
        return file_list

#           SOCKET METHODS
    # Bind socket to host and port
    def bind_socket(self, attempt=0):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

        except socket.error as err:
            if self.RETRY_COUNT > attempt:
                print("Socket Binding error: " + str(err) + ", Retrying...")
                time.sleep(self.RETRY_WAIT)
                self.bind_socket(attempt+1)
            else:
                raise Exception("Socket Binding error: " + str(err) + ", Max Retry tries reached. :(")

    # Listen for connections and add them to connection list
    def accept_connections(self):
        self.close_connections()
        self._state_lock.acquire()
        while True:
            connection, address = self.server_socket.accept()

            client_id = len(self.client_list)

            new_connection = dict()
            new_connection['connection'] = connection
            new_connection['address'] = address

            self.client_list.append(new_connection)
            th_client = threading.Thread(target=self.client_logic, args=(new_connection, ))

            print("Connection established with: [ {}:{} ]\n".format(address[0], address[1]))
            connection.send("hello_client {}".format(client_id).encode('utf-8'))
            data = connection.recv(self.BUFFER_SIZE)
            if data.decode('utf-8') == 'hello_server':
                print("Client said hello")
                if self._state_lock.locked():
                    self._state_lock.release()
                th_client.start()
                pass
            print("Switching server state")

    # Close all active connections and clear client_list
    def close_connections(self):
        for conn in self.client_list:
            conn['connection'].close()
        del self.client_list[:]

        
#           CLIENT LOGIC
    def client_logic(self, connection_dict):
        print('init client')
        while self.work_load_list:
            try:
                self._state_lock.acquire()
                self._state_lock.release()
                print('looking for a job')
                job = self.find_work()
                while job:
                    print('found a job')
                    self.send_images(connection_dict, job)
                    job = self.find_work()
            except Exception as err:
                print(str(err))
                break;
        connection_dict['connection'].close()

                

    def create_work(self):
        self.work_load_list = []
        for i in range(math.ceil(len(self.image_paths) / self.WORK_SIZE)):
            self.work_load_list.append(self.image_paths[self.WORK_SIZE*i:self.WORK_SIZE*i+self.WORK_SIZE])

    def find_work(self):
        self._work_lock.acquire()
        if len(self.work_load_list) > 0:
            work = self.work_load_list.pop()
        else:
            work = None
        self._work_lock.release()
        print(len(self.work_load_list))
        return work

    def append_work(self, work):
        self._work_lock.acquire()
        print('Appending work')
        self.work_load_list.append(work)
        self._work_lock.release()

    def send_images(self, worker, work_load):
        ret_stream = io.BytesIO()
        try:
            connection = worker['connection']
            address = worker['address']

            print("Started sending data over: {}".format(address))
            connection.send('WORK'.encode('utf-8'))
            self._socket_lock.acquire()
            for wrk_image in work_load:                
                print(wrk_image + " SENDING")
                msg = connection.recv(self.BUFFER_SIZE).decode('utf-8')
                if msg != 'INFO':
                    raise ValueError('Connection mismatch')

                img = Image.open(wrk_image)
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG')

                filesize = buffer.getbuffer().nbytes
                connection.send(f'{wrk_image}{self.SEPARATOR}{filesize}'.encode('utf-8'))

                msg = connection.recv(self.BUFFER_SIZE).decode('utf-8')
                if msg != 'DATA':
                    raise ValueError('Connection mismatch')

                connection.send(buffer.getvalue())

            self._socket_lock.release()
            msg = connection.recv(self.BUFFER_SIZE).decode('utf-8')
            if msg != 'INFO':
                raise ValueError('Connection mismatch')

            connection.send('DONE'.encode('utf-8'))
            print("Done sending data over: {}".format(address))

            while True:
                msg = connection.recv(self.BUFFER_SIZE).decode('utf-8')
                if msg == 'TEXT':
                    connection.send('CHEK'.encode('utf-8'))
                    print("x")
                elif msg == 'SCND':
                    connection.send('SEND'.encode('utf-8'))
                    while True:
                        buffer = connection.recv(self.BUFFER_SIZE)
                        ret_stream.write(buffer)
                        if len(buffer) < self.BUFFER_SIZE:
                            break
                    break
                else:
                    raise ValueError('Unexpected respone from client')

        except Exception as err:
            if self._socket_lock.locked():
                self._socket_lock.release()
            self.append_work(work_load)
            raise Exception(str(err))
        


        self.processed += 5
        header = "\n\n===========================================\n\t{}{}\tImages:{}\n=======================================\n\n".format(self.processed - 5, self.processed, work_load)
        self.write_result(header + ret_stream.getvalue().decode('utf-8'))


    def write_result(self, result):
        self._write_lock.acquire()
        print("Writing results")
        with open('out/results.txt', 'a') as fd:
            fd.write(result)
        self._write_lock.release()

            

if __name__ == '__main__':
    server = Server()
    server.start()

