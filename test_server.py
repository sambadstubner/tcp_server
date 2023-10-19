import socket
import threading

from tcp_server import Server

class TestServer:
    if __name__ != "__main__":
        server = Server(8083)
        server_thread = threading.Thread(target=server.run)
        server_thread.start()
    
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8083))

    def test_hello_world_uppercase(self):
        self.client.send(b"\x40\x00\x00\x0bHello World")
        received = self.client.recv(1024)
        print(received)
        assert  received == b"\x40\x00\x00\x0bHELLO WORLD"

    def test_the_lan_before_time_reverse(self):
        self.client.send(b"\x20\x00\x00\x13The Lan Before Time")
        received = self.client.recv(1024)
        print(received)
        assert received == b"\x00\x00\x00\x13emiT erofeB naL ehT"

if __name__ == "__main__":
    test = TestServer()
    test.test_the_lan_before_time_reverse()
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(("localhost", 8083))
    # client.send(b"\x40\x00\x00\x0bHello World")
    # print(client.recv(1024))
