import socket
import threading
import logging

from tcp_server import Server

class TestServer:
    logging.basicConfig(level=logging.DEBUG)

    server = None
    if __name__ != "__main__":
        server = Server(8083)
        server_thread = threading.Thread(target=server.run)
        server_thread.start()
    
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8083))


    def test_hello_world_uppercase(self):
        logging.info("Action: UPPERCASE Message: Hello world")
        self.client.send(b"\x08\x00\x00\x0bHello World")
        received = self.client.recv(1024)
        logging.info(f"Received: {received}")
        assert received == b"\x00\x00\x00\x0bHELLO WORLD"


    def test_hello_world_lowercase(self):
        logging.info("Action: LOWERCASE Message: HELLO WORLD")
        self.client.send(b"\x10\x00\x00\x0bHELLO WORLD")
        received = self.client.recv(1024)
        logging.info(f"Received: {received}")
        assert received == b"\x00\x00\x00\x0bhello world"


    def test_hello_world_reverse(self):
        logging.info("Action: REVERSE Message: Hello World!")
        self.client.send(b"\x20\x00\x00\x0cHello World!")
        received = self.client.recv(1024)
        logging.info(f"Received: {received}")
        assert received == b"\x00\x00\x00\x0c!dlroW olleH"


    def test_hello_world_shuffle(self):
        input = b"\x40\x00\x00\x0cHello World!"
        logging.info(f"Action: SHUFFLE Message: Hello World!")
        self.client.send(input)
        received = self.client.recv(1024)
        logging.info(f"Received: {received}")
        assert received != input
        assert len(received) != None

    
    def test_hello_world_random(self):
        input = b"\x80\x00\x00\x0cHello World!"
        logging.info("Action: RANDOM Message: Hello World!")
        self.client.send(input)
        received = self.client.recv(1024)
        logging.debug(f"Received: {received}")
        assert received != input
        assert len(received) != None


    def test_the_lan_before_time_reverse(self):
        self.client.send(b"\x20\x00\x00\x13The Lan Before Time")
        logging.info("Action: REVERSE Message: The Lan Before Time")
        received = self.client.recv(1024)
        logging.info(f"Received: {received}")
        assert received == b"\x00\x00\x00\x13emiT erofeB naL ehT"


    def test_error(self):
        self.client.send(b"\x28\x00\x00\x13The Lan Before Time")
        logging.info("Action: ERROR Message: The Lan Before Time")
        received = self.client.recv(1024)
        logging.info(f"Received: {received}")
        assert received == b"\x00\x00\x00\x05error"
    

if __name__ == "__main__":
    test = TestServer()
    test.test_the_lan_before_time_reverse()
    test.test_hello_world_lowercase()
    test.test_hello_world_random()
    test.test_hello_world_reverse()
    test.test_hello_world_shuffle()
    test.test_hello_world_uppercase()
