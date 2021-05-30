import socket
import os

from PIL import Image
import pytesseract


class Client:
    host = "localhost"
    server_port = 6060
    client_socket = socket.socket()

    def read_image(self, image:Image):
        text = pytesseract.image_to_string(image, lang='eng')
        return text


    def connect(self):
        self.client_socket.connect((self.host, self.server_port))
        data = self.client_socket.recv(4096)
        if data.decode('utf-8') == "hello client":
            print("Connection established!")
        self.client_socket.send("give file".encode('utf-8'))

        while data:
            data = self.client_socket.recv(4096)
            with open('test.jpg', 'ab') as file:
                file.write(data)


if __name__ == '__main__':
    client = Client()
    client.connect()
    #print(pytesseract.image_to_string(Image.open('./images/1Text.jpg'), lang='eng'))
    