import json
import socket

# Define the path to the socket file (should match the server's socket path)
socket_path = './socket.sock'

def send_request(request):
    """
    Connect to the server's UNIX domain socket and send a request.
    """
    # Create a UNIX domain socket client
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client.connect(socket_path)

        # Send the request
        request_json = json.dumps(request) + '\n'
        client.sendall(request_json.encode('utf-8'))

        # Receive and decode the response
        response_json = client.recv(1024).decode('utf-8')

        # Parse the response as JSON
        response = json.loads(response_json)

        return response
    finally:
        client.close()

# Example request
request = {
    'id': 42,
    'method': 'echo',
    'params': {
        'message': 'Hello'
    }
}

# Send the request and receive the response
response = send_request(request)

# Print the response
print(response)
