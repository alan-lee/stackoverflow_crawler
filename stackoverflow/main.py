from data.msg_handler import process_msg
from network.socket_server import SocketServer

if __name__ == '__main__':
    server = SocketServer('0.0.0.0', 8877, process_msg)
    server.server_init()
    server.serve_forever()