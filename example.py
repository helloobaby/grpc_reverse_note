from grpc import *
from ipc_pb2_grpc import *
from typing import Iterator
import uuid
import OpenSSL
import socket
import os

dst = ('localhost', 48299) # 远程grpc服务端口
sock = socket.create_connection(dst)
context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
connection = OpenSSL.SSL.Connection(context, sock)
connection.set_connect_state()
try:
    print('connect to localhost:48299')
    connection.do_handshake()
    crts = connection.get_peer_cert_chain()
    # 只有一个自签证书
    assert len(crts) == 1
    crt=crts[0]
    pem=OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM,crt)

    # # 服务端证书利用openssl动态转储
    with open('server.crt', 'wb') as cert_file:
        cert_file.write(pem)
except Exception as e:
    print(f'error : cant get peer cert {e}')
    exit(0)

# 验证客户端公钥密钥是否匹配
# "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" x509 -noout -modulus -in client.crt | "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" md5
# "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" rsa -noout -modulus -in client.key | "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" md5

credentials = grpc.ssl_channel_credentials(open('server.crt', 'rb').read(),open('client.key', 'rb').read(),open('client.crt', 'rb').read())
channel = secure_channel('localhost:48299',credentials)
stub = IPCStub(channel)

language_setting = ipc__pb2.LanguageSetting(
        language="en_US",
        needWriteLog=True
    )

uuid = uuid.uuid4()
print(uuid)

def request_generator():
    yield ipc__pb2.IPCMsg(
        src=1001,
        dst=1000,
        request_id=str(uuid),
        type=5003,
        count=0,
        content=[language_setting.SerializeToString()]
)

for response in stub.Connection(request_generator()):
            print("resp: ", response)