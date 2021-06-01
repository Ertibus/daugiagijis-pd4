# ./program/master/server.py

import socket
import io
import os
import time

from PIL import Image
import pytesseract

import tqdm


class Client:
    HOST = "localhost"
    SERVER_PORT = 6060
    BUFFER_SIZE = 8192
    MAX_WORKERS = 5

    SEPARATOR = "<SEPARATOR>"

    client_socket = socket.socket()

    images_list = []

    def read_image(self, image:Image):
        text = pytesseract.image_to_string(image, lang='eng')
        return text


    def connect(self):
        self.client_socket.connect((self.HOST, self.SERVER_PORT))
        print("Waiting for message from server")
        data = self.client_socket.recv(self.BUFFER_SIZE)
        msg = data.decode('utf-8')
        if msg.split(' ')[0] == "hello_client":
            print("Connection established! I'm: {}".format(msg.split(' ')[1]))
            self.client_socket.send("hello_server".encode('utf-8'))
            while True:
                msg = self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                if msg == 'WORK':
                    self.recieve_images()
                    results = self.process_images()
                    self.return_results(results)
                elif msg == "NJOB" or not msg:
                    break
                else:
                    raise ValueError("Response Mismatch")

    def recieve_images(self):
        while True:
            self.client_socket.send('INFO'.encode('utf-8'))
            file_info = self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8')

            if file_info == 'DONE':
                break;

            filename, filesize = file_info.split(self.SEPARATOR)

            filename = os.path.basename(filename)
            filesize = int(filesize)

            self.client_socket.send('DATA'.encode('utf-8'))
            image_stream = io.BytesIO()
            downloaded=0
            with tqdm.tqdm(range(filesize), f"Receiving {filename}:", unit="B", unit_scale=True, unit_divisor=1024, position=1) as progress:
                while downloaded < filesize:
                    buffer_read = self.client_socket.recv(self.BUFFER_SIZE)
                    image_stream.write(buffer_read)
                    progress.update(len(buffer_read))
                    downloaded+=len(buffer_read)
            img_data = image_stream
            rcv_img = Image.open(img_data)
            self.images_list.append(rcv_img)


    def process_images(self):
        read_text = ""
        pbar = tqdm.tqdm(self.images_list, "Processing images:")
        for image in pbar:
            read_text += self.tesseract(image)
            self.client_socket.send("TEXT".encode('utf-8'))
            msg = self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            if msg != 'CHEK':
                raise ValueError("Response Mismatch")

        pbar.close()
        return read_text


    def tesseract(self, image:Image):
        while True:
            with open('test_lock', 'rb') as lock:
                lock_read = lock.read()
                if lock_read == b'0':
                    break;
                time.sleep(0.01)
        with open('test_lock', 'wb') as lock:
            lock.write(b'1')
        ret_val = pytesseract.image_to_string(image, lang='eng')
        with open('test_lock', 'wb') as lock:
            lock.write(b'0')
        return ret_val


    def return_results(self, result):
        print("Sending back the results..\n")
        del self.images_list[:]
        self.client_socket.send("SCND".encode('utf-8'))
        msg = self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
        if msg != 'SEND':
            raise ValueError("Response Mismatch")
        self.client_socket.sendall(result.encode('utf-8'))

if __name__ == '__main__':
    client = Client()
    client.connect()
    #print(pytesseract.image_to_string(Image.open('./images/1Text.jpg'), lang='eng'))
    
