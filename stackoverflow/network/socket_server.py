import socket
import select
import errno


class Link:
    def __init__(self, connection, address):
        # for connection
        self.connection = connection
        self.address = address
        # for read buffer
        self.read_buff = ''
        # for write buffer
        self.write_buff = ''


class SocketServer:
    def __init__(self, serv_addr, port, handler):
        self.__links = dict()
        self.__addr = serv_addr
        self.__port = port
        self.__handler = handler
        self.__socket = None

    def server_init(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #set socket address reused
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind and listen
        self.__socket.bind((self.__addr, self.__port))
        self.__socket.listen(1)
        #set non-blocking socket
        self.__socket.setblocking(False)

    def serve_forever(self):
        epoll = select.epoll()
        epoll.register(self.__socket.fileno(), select.EPOLLIN | select.EPOLLET)

        while True:
            events = epoll.poll()
            for fileno, event in events:
                if fileno == self.__socket.fileno():
                    while True:
                        try:
                            connection, link_address = self.__socket.accept()
                            connection.setblocking(0)
                            epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
                            link = Link(connection, link_address)
                            self.__links[connection.fileno()] = link
                        except socket.error, err:
                            if err.errno == errno.EAGAIN:
                                break

                elif event & select.EPOLLIN:
                    link = self.__links[fileno]
                    error = 0
                    if link:
                        while True:
                            try:
                                buff = link.connection.recv(1024)
                                if buff is not None and len(buff) > 0:
                                    link.read_buff += buff
                                else:
                                    break
                            except socket.error, err:
                                error = err.errno
                                break

                        if error != errno.EAGAIN:
                            link.read_buff = ''
                            continue

                        link.write_buff += self.__handler(link.addr, link.read_buff)

                        link.read_buff = ''
                        if len(link.write_buff):
                            epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)

                elif event & select.EPOLLOUT:
                    link = self.__links[fileno]
                    if link:
                        while True:
                            try:
                                send_size = link.connection.send(link.write_buff)
                                if send_size > 0:
                                    link.write_buff = link.write_buff[send_size:]
                                else:
                                    break
                            except socket.error, err:
                                if err.errno == errno.EAGAIN:
                                    break

                        link.write_buff = ''
                        epoll.modify(fileno, select.EPOLLIN | select.EPOLLET)

                elif event & select.EPOLLHUP:
                    link = self.__links[fileno]
                    epoll.unregister(fileno)
                    link.connection.close()
                    self.__links.pop(fileno)
                    del link
