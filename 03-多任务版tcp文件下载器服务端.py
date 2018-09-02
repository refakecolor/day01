import socket
import os
import threading
import time


# 处理客户端请求下载文件的操作
def handle_client_request_data(ip_port, service_client_socket):
    print("客户端连接成功了:", ip_port)
    # 接收客户端的请求信息
    file_name_data = service_client_socket.recv(1024)
    # 对二进制数据进行解码
    file_name = file_name_data.decode("utf-8")
    # 判断文件是否存在
    if os.path.exists(file_name):
        # 文件存在
        # 打开文件, with open 关闭文件操作不需要程序员自己去做，有系统去做
        with open(file_name, "rb") as file:
            # 读取文件数据
            while True:
                # 循环读取文件数据
                file_data = file.read(1024)
                if file_data:
                    # 表示读到数据，然后把数据发送给客户端
                    service_client_socket.send(file_data)
                    time.sleep(1)
                else:
                    print("请求的文件数据发送完成")
                    break

    else:
        print("下载的文件服务器不存在")

    # 终止和这个客户端服务
    service_client_socket.close()


if __name__ == '__main__':
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口号
    tcp_server_socket.bind(("", 8080))
    # 设置监听，把主动套接字变成被动套接字，服务端套接字只负责接收客户端的连接请求
    tcp_server_socket.listen(128)
    # 循环调用accept可以支持多个客户端连接服务端，但是不能同时多个客户端连接服务器端，因为是同步下载的
    # 一个客户端下载完成以后另外一个客户端才能和服务端建立连接下载对应的文件
    while True:
        # 等待接收客户端的连接请求
        service_client_socket, ip_port = tcp_server_socket.accept()
        print(id(service_client_socket))

        # handle_client_request_data(ip_port, service_client_socket)
        # 创建子线程，专门服务与客户端
        sub_thread = threading.Thread(target=handle_client_request_data, args=(ip_port, service_client_socket))
        # 启动子线程执行对应的任务
        sub_thread.start()
