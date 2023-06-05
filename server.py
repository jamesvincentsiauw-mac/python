import json
import os
import socket
import sys


class RequestHandler:
    def handle_request(self, request):
        method = request.get('method')
        params = request.get('params', {})
        request_id = request.get('id')

        if method == 'echo':
            message = params.get('message')
            response = {
                'id': request_id,
                'result': {
                    'message': message
                }
            }
            return response

        return {'id': request_id, 'result': {}}


class Server:
    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.request_handler = RequestHandler()

    def start(self):
        # Create the socket server
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        print(f"Server started. Listening on socket: {self.socket_path}")

        # Listen for incoming connections
        server.listen()
        print("Waiting for incoming connections...")

        # Start accepting client connections
        while True:
            client_socket, _ = server.accept()
            print("Client connected.")

            self.handle_client_connection(client_socket)

    def handle_client_connection(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Split received data into individual messages
            messages = data.strip().split('\n')
            for message in messages:
                try:
                    request = json.loads(message)
                    print(f"Received request: {request}")

                    response = self.request_handler.handle_request(request)
                    print(f"Sending response: {response}")

                    response_json = json.dumps(response) + '\n'
                    client_socket.sendall(response_json.encode('utf-8'))
                except ValueError:
                    # Invalid message received, disconnect
                    break

        client_socket.close()


if __name__ == '__main__':
    # Get the socket path from command line arguments
    if len(sys.argv) < 2:
        print("Please provide the path to the socket file as the first argument.")
        sys.exit(1)

    socket_path = sys.argv[1]

    # Create the server instance and start it
    server = Server(socket_path)
    server.start()
