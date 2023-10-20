import logging
import signal
import socket
import struct
import sys

import actions
from server_parser import ServerParser


class Server:
    EXPECTED_HEADER_SIZE = 4
    DEFAULT_BUFFER_SIZE = 1024

    def __init__(self, port:int):
        self.port = port
        signal.signal(signal.SIGINT, self.handle_exit)

    def run(self):
        self.server_socket = socket.create_server(address=("", self.port),
                                            family=socket.AF_INET,
                                            reuse_port=True)
        self.server_socket.listen()

        while True:
            conn, address = self.server_socket.accept()
            logging.info(f"Connection from: {address}")

            while True:
                header = conn.recv(self.EXPECTED_HEADER_SIZE)
                if not header:
                    logging.info("Client disconnected...")
                    break

                action, message_length = self.parse_header(header)
                logging.debug(f"Action: {action:02x} Message length: {message_length:02x}")
                
                num_received = 0
                message = str()
                while(num_received < message_length):
                    num_remaining = message_length - num_received
                    if(num_remaining < self.DEFAULT_BUFFER_SIZE):
                        buffer_size = num_remaining
                    else:
                        buffer_size = self.DEFAULT_BUFFER_SIZE
                    received_bytes = conn.recv(buffer_size).decode()
                    num_received += len(received_bytes)
                    message += received_bytes

                logging.info(f"Received: {message}")
                
                response = Server.create_response(action, message)
                logging.debug(f"Response packet: {response}")
                
                if response != None:
                    conn.send(response)
                    logging.debug("Sent")
                else:
                    logging.debug("No response, not sending")

            conn.close()


    @staticmethod
    def parse_header(header) -> (int, int):
        header = struct.unpack('!L', header)[0]
        logging.debug(f"Header: {header}")
        return Server.decode_action_from_header(header), Server.decode_message_length_from_header(header)
    
    @staticmethod
    def decode_action_from_header(header:int) -> int:
        return header >> 27
    
    @staticmethod
    def decode_message_length_from_header(header:int) -> int:
        return header & 0x7FFFFFF
    
    @staticmethod
    def create_response(action:int, message:str) -> int:
        message = Server.create_response_message(action, message)
        if message == None:
            logging.info("Invalid action detected")
            return None
        logging.info(f"Response message: {message}")

        message_length = Server.create_response_message_length(message)

        response_message = message_length + message.encode()
        return response_message

    @staticmethod
    def create_response_message(action:int, message:str) -> str:
        if(action == actions.UPPERCASE):
            logging.debug("Action: UPPERCASE")
            return actions.uppercase(message)
        
        if(action == actions.LOWERCASE):
            logging.debug("Action: LOWERCASE")
            return actions.lowercase(message)
        
        if(action == actions.REVERSE):
            logging.debug("Action: REVERSE")
            return actions.reverse(message)

        if(action == actions.SHUFFLE):
            logging.debug("Action: SHUFFLE")
            return actions.shuffle(message)
        
        if(action == actions.RANDOM):
            logging.debug("Action: RANDOM")
            return actions.random(message)
        
        else:
            return None
        
    @staticmethod
    def create_response_message_length(message:str):
        message_length = len(message)
        logging.debug(f"Response message length before packing: {message_length}")
        message_length = struct.pack('!L', message_length)
        logging.debug(f"Response message length after packing: {message_length}")
        return message_length


    def handle_exit(self, sig, frame):
        logging.info("Interrupt detected, shutting down server...")
        self.server_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    args = ServerParser().parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)
    server = Server(args.port)
    server.run()
