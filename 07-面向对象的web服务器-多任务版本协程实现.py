import socket
import re
import gevent
from gevent import monkey

# 打补丁，让gevent失败耗时(time.sleep, 网络请求， accept， recv)操作, 自动切换到其它协程执行对应的代码
monkey.patch_all()


# 自定义http web服务器类
class HttpWebServer(object):
    def __init__(self):
        # 创建tcp服务端套接字
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 　设置端口号复用
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 给程序绑定端口号
        tcp_server_socket.bind(("", 9090))
        # 设置监听
        tcp_server_socket.listen(128)
        # 把创建的tcp服务器套接字作为当前web服务器对象的属性
        self.tcp_server_socket = tcp_server_socket

    # 处理客户端请求的操作
    @staticmethod
    def handle_client_request(service_client_socket):
        # 获取客户端发送的http请求报文数据
        http_request_data = service_client_socket.recv(4096)
        # 对二进制数据进行解码
        http_request_content = http_request_data.decode("utf-8")
        print(http_request_content)
        match_obj = re.search("/\S*", http_request_content)
        if match_obj:
            # 匹配成功，获取请求的资源连接
            request_path = match_obj.group()
            # 判断请求的路径是否是根路径，如果是根路径指定对应的文件
            if request_path == "/":
                request_path = "/index.html"

            # 打开文件读取文件中的数据
            # with open("index.html", "rb") as file:
            #     while True:
            #         file_data = file.read(1024)

            # 1. os.path.exits("static" + request_path)
            # 2. try-except

            try:
                with open("static" + request_path, "rb") as file:
                    # 读取文件中的全部数据
                    file_data = file.read()
            except Exception as e:
                # 404 没有在服务器找到请求的文件
                # 响应行
                response_line = "HTTP/1.1 404 Not Found\r\n"
                # 响应头, 提示： 响应头信息程序员也可以根据自己的需要自定义一个响应头信息
                # Content-Type: text/html;charset=utf-8： 服务器告诉浏览器数据的类型及编码格式
                response_header = "Server: PWS/1.1\r\nother:ok\r\nContent-Type: text/html;charset=utf-8\r\n"
                # 响应体
                response_body = "<h1>非常抱歉，您当前访问的网页已经不存在了</h1>"
                # 组装http响应报文数据
                response_data = (response_line + response_header + "\r\n" + response_body).encode("utf-8")

                # 发送http 响应报文数据给客户端
                service_client_socket.send(response_data)
            else:
                # 找到了请求的资源文件，发送200的状态
                # 响应行
                response_line = "HTTP/1.1 200 OK\r\n"
                # 响应头, 提示： 响应头信息程序员也可以根据自己的需要自定义一个响应头信息
                # Content-Type: text/html;charset=utf-8： 服务器告诉浏览器数据的类型及编码格式
                response_header = "Server: PWS/1.1\r\nother:ok\r\nContent-Type: text/html;charset=utf-8\r\n"
                # 响应体
                response_body = file_data
                # 组装http响应报文数据
                response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body

                # 发送http 响应报文数据给客户端
                service_client_socket.send(response_data)
        # 关闭套接字
        service_client_socket.close()

    # 启动web服务器进行工作
    def start(self):
        while True:
            # 等待接收客户端的连接请求
            service_client_socket, ip_port = self.tcp_server_socket.accept()
            # 创建协程指定对应执行任务
            gevent.spawn(self.handle_client_request, service_client_socket)

            # 提示：这里不需要加上join，因为主线程会一直运行，并且循环里面有耗时操作，会自动切换到不同协程执行代码


if __name__ == '__main__':



    # 创建web服务器对象  -》 通过web服务器类来创建
    web_server = HttpWebServer()
    # 让web服务器启动进行工作
    web_server.start()

