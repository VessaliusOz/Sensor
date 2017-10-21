import threading
import socketserver
import datetime
from sensor.handle_database import connect_to_redis
from binascii import hexlify


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    t = None
    wantDisconnect = False

    def handle(self):
        # 这个以后会删掉，估计没有什么用
        time_interval = (datetime.datetime.now() - self.t).seconds
        while time_interval < 10 and not self.wantDisconnect:
            # 先得到包的类型
            data = self.request.recv(1024)

            if data:
                print(data)
                # b'\x00\x13\x01\x02\x03\'
                # 变为　'0013010203'　字符串
                try:
                    binary_to_string = hexlify(data).decode("ascii")
                except:
                    self.request.sendall("wrong data")
                    break
                print(binary_to_string)
                data_type = binary_to_string[0:2]
                # 得到数据包的长度
                data_length = int(binary_to_string[2:4], base=16)
                # print(data_lengt-*h)
                # 验证长度
                if len(binary_to_string) != 2*data_length:
                    self.request.sendall("wrong data")
                    break

                else:
                    data_body = binary_to_string[4:]
                    # 将数据体分配到相应的处理类
                    data_handler = connect_to_redis(data_type, data_body)
                    try:
                        data_handler.insert_into_redis()
                    except:
                        print("unknown type")
                        break

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


