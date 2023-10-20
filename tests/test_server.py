import socket
import threading
import logging

from tcp_server import Server


class TestServer:
    logging.basicConfig(level=logging.DEBUG)

    UPPERCASE = 1 
    LOWERCASE = 2
    REVERSE = 4
    SHUFFLE = 8
    RANDOM = 16

    DEFAULT_BUFFER_SIZE = 1024

    server = None
    if __name__ != "__main__":
        server = Server(8083)
        server_thread = threading.Thread(target=server.run)
        server_thread.start()
    
    
    @staticmethod
    def receive_message(connected_socket, message_length):
        num_received = 0
        message = str()
        while(num_received < message_length):
            num_remaining = message_length - num_received
            if(num_remaining < TestServer.DEFAULT_BUFFER_SIZE):
                buffer_size = num_remaining
            else:
                buffer_size = TestServer.DEFAULT_BUFFER_SIZE
            received_bytes = connected_socket.recv(buffer_size).decode()
            num_received += len(received_bytes)
            message += received_bytes
        
        return message

    @staticmethod
    def create_request(action, message):
        message_length = len(message)
        header = (action << 27) | message_length
        header_bytes = header.to_bytes(4, byteorder='big')
        return header_bytes + message.encode('utf-8')

    @staticmethod
    def send_and_receive(action, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 8083))

        full_message = TestServer.create_request(action, message)
        client.send(full_message)

        response_header = client.recv(4)  # Receive the header
        response_length = int.from_bytes(response_header, byteorder='big') & 0x7FFFFFFF

        response_message = Server.receive_message(client, response_length)  # Receive the message
        client.close()
        print(response_message)
        return response_message


    def test_hello_world_uppercase(self):
        response = self.send_and_receive(self.UPPERCASE, "hello world")
        assert response == "HELLO WORLD"


    def test_hello_world_lowercase(self):
        response = self.send_and_receive(self.LOWERCASE, "HELLO WORLD")
        assert response == "hello world"


    def test_hello_world_reverse(self):
        response = self.send_and_receive(self.REVERSE, "Hello World!")
        assert response == "!dlroW olleH"


    def test_hello_world_shuffle(self):
        message = "Hello World!"
        response = self.send_and_receive(self.UPPERCASE, message)
        assert len(response) == len(message)
        assert response != message

    
    def test_hello_world_random(self):
        message = "Hello World!"
        response = self.send_and_receive(self.UPPERCASE, "Hello World!")
        assert response != message
        assert len(response) != None


    def test_the_lan_before_time_reverse(self):
        response = self.send_and_receive(self.REVERSE, "The Lan Before Time")
        assert response == "emiT erofeB naL ehT"


    def test_error(self):
        response = self.send_and_receive(12, "The Lan Before Time")
        assert response == "error"


    def test_book_of_alma_upper(self):
        with open('tests/input_large.txt', 'r') as file:
            text = file.read()
            response = self.send_and_receive(self.UPPERCASE, text)
            assert response == text.upper()
    
    def test_book_of_alma_reverse(self):
        with open('tests/input_large.txt', 'r') as file:
            text = file.read()
            response = self.send_and_receive(self.REVERSE, text)
            assert response == text[::-1]


    def test_book_of_alma_shuffle(self):
        with open('tests/input_large.txt', 'r') as file:
            text = file.read()
            response = self.send_and_receive(self.REVERSE, text)
            assert len(response) == len(text)
            assert response != text


if __name__ == "__main__":
    test = TestServer()
    test.test_the_lan_before_time_reverse()
    test.test_hello_world_lowercase()
    test.test_hello_world_random()
    test.test_hello_world_reverse()
    test.test_hello_world_shuffle()
    test.test_hello_world_uppercase()
