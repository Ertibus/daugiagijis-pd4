# ./program/master/server.py

import socket
import os
import io

from PIL import Image
import pytesseract


class Client:
    HOST = "localhost"
    SERVER_PORT = 6060
    BUFFER_SIZE = 8192

    client_socket = socket.socket()

    images_list = []

    def read_image(self, image:Image):
        text = pytesseract.image_to_string(image, lang='eng')
        return text


    def connect(self):
        self.client_socket.connect((self.HOST, self.SERVER_PORT))
        while True:
            print("Waiting for message from server")
            data = self.client_socket.recv(self.BUFFER_SIZE)
            msg = data.decode('utf-8')
            
            if msg.split(' ')[0] == "hello_client":
                print("Connection established! I'm: {}".format(msg.split(' ')[1]))
            elif msg == "send work":
                self.recieve_images()
                results = self.process_images()
                self.return_results(results)
                

    def recieve_images(self):
        while True:
            print("Ready to recieve work")
            self.client_socket.send("ready".encode('utf-8'))
            data = self.client_socket.recv(self.BUFFER_SIZE)
            msg = data.decode('utf-8')
            if msg == "catch":
                img_data=b''
                while True:
                    buffer = self.client_socket.recv(self.BUFFER_SIZE)
                    img_data += buffer
                    if len(buffer) < self.BUFFER_SIZE:
                        break;
                rcv_img = Image.open(io.BytesIO(img_data))
                self.images_list.append(rcv_img)
            if msg == "end":
                print("Recieved work files!")
                break;

    def process_images(self):
        result = ""
        for image in self.images_list:
            print("processing image..")
            result += pytesseract.image_to_string(image, lang='eng')
        return result

    def return_results(self, result):
        print("writing results..")
        with open("resultfile.txt", "w") as file:
            file.write(result)

if __name__ == '__main__':
    client = Client()
    client.connect()
    #print(pytesseract.image_to_string(Image.open('./images/1Text.jpg'), lang='eng'))
    
