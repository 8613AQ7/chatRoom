from socket import *
import threading
import traceback

class Client:
    def __init__(self,port):
        #创建套接字 ipv4 面向连接
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.ip = gethostbyname(gethostname())
        self.port = port

        print('------客户端建立完成------')


    def connect(self):
        host = input('请输入服务端ip地址：')

        #服务器ip及端口
        #host = '180.172.122.249'
        #host = '217d37596f.51mypc.cn'
        #host = '192.168.0.198'

        try:
            print('------正在建立连接------')
            self.socket.connect((host, self.port))
        except:
            traceback.print_exc()
            print(1)
        else:
            print('------连接成功------')
        
    def receiveMessage(self,Socket):
        while True:
            data = Socket.recv(1024)
            if len(data) > 0:
                message = eval(data.decode('utf-8'))
                print('%s号: %s'%(message[1], message[0]))
            else:
                Socket.close()
                break

            
    def sendMessage(self,Socket):
        while True:
            try:
                message = str(input())
                print('%s号(自己): %s'%(self.ip, message))
                Socket.send(message.encode('utf-8'))
            except:
                break

    def join(self):
        #收发信息
        send = threading.Thread(target = self.sendMessage, args = (self.socket,))
        receive = threading.Thread(target = self.receiveMessage, args = (self.socket,))

        send.start()
        receive.start()

        send.join()
        receive.join()

def main():
    client = Client(4567)
    client.connect()
    client.join()

if __name__ == '__main__':
    main()
