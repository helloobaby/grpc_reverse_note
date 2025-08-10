### 定位SSL_write

想分析grpc的流量。抓包一般比较困难，尤其是带了双向认证。

```
int SSL_write(SSL *ssl, const void *buf, int num) 
```

```c++
    const char* request = "GET https://www.baidu.com/ HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: keep-alive\r\n\r\n";
    int ret = SSL_write(ssl, request, strlen(request));
    ...
```



SSL库一般有两个，boringssl和openssl,用的比较多的是openssl，一般boringssl是google自己的产品用的。

##### 如何在二进制文件中搜索到SSL_write函数(适用于Windows)

搜"ssl\\ssl_lib.c"字符串相关，多找几处对着源码看看就行

**GRPC协议分析**

SSL_write buf参数对应的是grpc(http2)流量。 流量可以用一些开源软件分析出protobuf的模糊结构。

**Protobuf还原**

完全还原proto文件可以从文件入手。

利用pbtk从文件中解析出原始proto文件。



