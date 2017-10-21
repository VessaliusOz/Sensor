import threading
import socketserver
import datetime
from handle_database import connect_to_redis


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    t = None
    wantDisconnect = False

    def handle(self):
        # 这个以后会删掉，估计没有什么用
        time_interval = (datetime.datetime.now() - self.t).seconds
        while time_interval < 10 and not self.wantDisconnect:
            # 先得到包的类型
            data_type = self.request.recv(2).decode("ascii")

            print(data_type)

            if data_type:
                # print(data_type)
                # 在得到包的长度
                repr_data_length = self.request.recv(2).decode("ascii")
                # print(repr_data_length)
                data_length = int(repr_data_length, base=16)

                print(data_length)

                # print(data_length)
                # 在得到包的长度，　注意包的长度要减去头和length字段的长度
                data_body = self.request.recv(data_length-4).decode("ascii")
                # 将数据体分配到相应的处理类
                connect_to_redis(data_type, data_body)

                # 这里是否要考虑心跳包的回复呢，如果是，就要回一个心跳包，重新构造一个心跳包(包括各种信息)
                # 判断还没有开始写,
                # 要做包的应答

                # if data_type == "00":
                self.request.sendall("yes")

                # 开启一个线程，处理连接异常断开的情况
                cur_thread = threading.current_thread()
                response = "{}: {},{},{}".format(cur_thread.name, data_type, data_length, data_body)
                print(response)

                self.request.sendall(response.encode("ascii"))
            else:
                print(threading.currentThread().name, " no data")
                break

    def setup(self):
        print(threading.currentThread(), " start")
        self.t = datetime.datetime.now()
        self.request.sendall(b"Hello there")

    def finish(self):
        self.wantDisconnect = True
        print(threading.currentThread(), " end")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


HOST, PORT = "", 50001

server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
server.serve_forever()


