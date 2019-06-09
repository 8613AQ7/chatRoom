from socket import *
import threading
import traceback





#将用户i的信息转发给所有用户
def transfer(clientSend):
    global clients
    clientSocket, clientInfo = clientSend

    count = 0 #记录ip地址中'.'的个数 来找到第四位作为学号
    number = ''
    for letter in str(clientInfo[0]):
        if count == 3:
            number += letter
        if letter ==  '.':
            count += 1

    while True:
        try:
            #接受信息
            message = clientSocket.recv(1024).decode('utf-8')

            #转发信息 附带发送者学号
            for otherclients in clients:
                if otherclients != clientSend:
                    otherclients[0].send(repr((message , number)).encode('utf-8'))
        except:
            #traceback.print_exc() 错误信息
            
            #将用户从用户列表中删去 结束该线程
            clients.remove(clientSend)

            print('用户%s断开连接 当前连接人数为 %d\n'%(str(clientInfo[0]), len(clients)))
            
            clientSocket.close()
            
            break



def main():
    #创建套接字 ipv4 面向连接
    serverSocket = socket(AF_INET, SOCK_STREAM)
    print('当前主机的IP为: ' + gethostbyname(gethostname()))

    #自身端口
    host = ''
    port = 4567

    #绑定
    serverSocket.bind((host, port))
    #开启监听
    serverSocket.listen(40)
    print('------服务端建立完成------\n')
    while True:
        try:
            # 响应连接 记录对象与地址
            newClient = clientSocket, clientInfo = serverSocket.accept()
            clients.append(newClient)
            newProcess = threading.Thread(target = transfer, args = (newClient, ))
            newProcess.start()
        except:
            print('------用户%s尝试连接失败------\n'% str(clientInfo[0]))
        else:
            print('用户%s已连接成功  当前连接人数为 %d\n' % (str(clientInfo[0]), len(clients)))

    #避免主线程结束后关闭子线程
    for each in process:
        each.join()

    print('------本次通信结束------\n')
    serverSocket.close()
    input()

if __name__ == '__main__':
    # 记录所有client对象 便于每个线程转发信息
    clients = []
    process = []
    main()
