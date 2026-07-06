# 错误处理
### 全局变量errno

    extern int errno;

    系统预定义的整型全局变量。

    在库函数和系统调用出错的时errno自动被设置，然后可以根据errno的值找到描述错误的字符串。

    注意
        #include <errno.h>


### strerror

    char *strerror(int errnum);

    strerror函数将错误代码转换为错误信息

    注意
        #include <string.h>
    参数
        errnum - 错误代码
    返回值
        成功 - 找到错误的编号，返回描述错误的字符串的首地址
        失败 - 找不到错误的编号，返回“Unknown error nnn”字符串的首地址
### perror

    void perror(const char *s);

    perror函数将错误信息打印到标准错误流

    注意
        #include <stdio.h>
    参数
        s - 自定义字符串用来接收strerror的返回值
    返回值
        成功 - 0
        失败 - -1

# 动态加载

### dlopen

    void *dlopen(const char *filename, int flags);
    将动态库加载到内存

    注意
        #include <dlfcn.h>
    参数
        filename - 共享库名 如果只给定文件的名字。按照动态链接器的搜索路径找动态库文件LD LIBRARY_PATH指定的路径下或者默认路径下找
        flags - 加载方式
            RTLD_LAZY - 延迟加载 使用共享库中的符号(如调用库中的函数)时才加载
            RTLD_NOW - 立即加载 函数返回的时候，已经加载到内存
    返回值
        成功 - 返回动态库加载到内存的地址句柄
        失败 - NULL 可以使用dlerror(3)函数诊断错误的原因
### dlclose

    int dlclose(void *handle);
    关闭动态库

    注意
        #include <dlfcn.h>
        仅仅使动态库的引用计数减一，并不一定从内存移除。只有引用计数为0的时候，才从内存移除。
    参数
        handle - 动态库的句柄
    返回值
        成功 - 0
        失败 - -1 可以使用dlerror(3)函数诊断错误的原因
### dlsym

    void *dlsym(void *handle, const char *symbol);
    获取动态库中的符号

    注意
        #include <dlfcn.h>
    参数
        handle - 动态库的句柄
        symbol - 符号名
            函数名
            全局变量名
            静态局部变量名
    返回值
        成功 - 符号的地址
        失败 - NULL 可以使用dlerror(3)函数诊断错误的原因

### dlerror

    const char *dlerror(void);
    获取动态库的错误信息

    注意
        #include <dlfcn.h>
    返回值
        成功 - 错误信息
        失败 - NULL

# 内存管理
# 进程管理
# 进程间通信
# 线程管理及线程间通信
# 文件管理
# 网络编程
### 数据结构ip地址

    struct sockaddr{                                       //通用地址家族
        sa_family_t sa_family;
        char	sa_data[14];
    }
    struct sockaddr_in {                                    //ipv4地址家族
        sa_family_t 	sin_family; /* address family: AF INET */
        in_port_t 	sin_port; /* port in network byte order */
        struct in_addr 	sin_addr; /* internet address */
    }
    struct in_addr{ 
        uint32 t 	s_addr;/* address in network byte order */
    }
    struct sockaddr_in6 {                                   //IPV6地址家族
        sa family_t	sin6_family; /* AF INET6 */
        in_port_t	sin6_port;/* port number */
        uint32_t 	sin6_flowinfo: /* IPv6 flow information */
        struct in6_addr sin6_addr; /* Iv6 address */
        uint32_t 	sin6_scope_id; /* Scope ID (new in 2.4) */
    }
    struct in6_addr{
        unsigned char s6_addr[16]; /* IPv6 address */
    }

## IP地址转换

### xtox

    unsigned long int htonl(unsigned long int hostlong);        将主机字节序转换为网络字节序
    unsigned short int htons(unsigned short int hostshort);     将主机字节序转换为网络字节序
    unsigned long int ntohl(unsigned long int netlong);         将网络字节序转换为主机字节序
    unsigned short int ntohs(unsigned short int netshort);      将网络字节序转换为主机字节序


### inet_ntop

    const char *inet_ntop(int af, const void *src, char *dst, socklen_t size);
    将ipv4和ipv6的地址从二进制转换到文本格式

    参数
        af - 具体的地址族
            AF_INET - ipv4
            AF_INET6 - ipv6
        src - 指定具体的二进制格式的ip地址
        dst - 转换后的结果存放在这里
        size - 定dst指向空间的有效大小
    返回值
        成功 - 转换后的ip地址
        失败 - NULL errno被设置为相应的错误值

### inet_pton

    int inet_pton(int af, const char *src, void *dst);
    将ipv4和ipv6的地址从文本格式转换为二进制格式

    参数
        af - 具体的地址族
            AF_INET - ipv4
            AF_INET6 - ipv6
        src - 指定具体的文本格式的ip地址
        dst - 转换后的结果存放在这里
    返回值
        成功 - 0 ip地址无效返回0
        失败 - -1 errno被设置为相应的错误值


### socket

    int socket(int domain, int type, int protocol);
    创建一个套接字 返回该设备的文件描述符

    参数
        domain - 具体的地址族
            AF_INET - ipv4
            AF_INET6 - ipv6
        type - 套接字类型
            SOCK_STREAM - 流式套接字TCP
            SOCK_DGRAM - 数据报套接字UDP
            SOCK_RAW - 原始套接字
        protocol - 具体的协议
            IPPROTO_TCP - tcp协议
            IPPROTO_UDP - udp协议
            IPPROTO_RAW - 原始套接字
    返回值
        成功 - 返回新的用于socket设备的描述符
        失败 - -1 errno被设置为相应的错误值

### bind

    int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    将套接字绑定到指定的地址

    参数
        sockfd - 套接字描述符
        addr - 具体的地址
        addrlen - 地址的长度
    返回值
        成功 - 0
        失败 - -1 errno被设置为相应的错误值

### listen

    int listen(int sockfd, int backlog);
    监听套接字

    参数
        sockfd - 套接字描述符
        backlog - 指定未决连接的最大数 客户端已经成功连接服务器，但是服务器还没有接收的连接称为未决连接
    返回值
        成功 - 0
        失败 - -1 errno被设置为相应的错误值

### accept

    int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
    未决队列中接收一个连接 自动创建一个套接字用于通讯并返回该套接字

    参数
        sockfd - 套接字描述符
        addr - 客户端的地址
        addrlen - 地址的长度
    返回值
        成功 - 返回新的套接字描述符
        失败 - -1 errno被设置为相应的错误值

### connect

    int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    使用套接字向服务器发起连接

    参数
        sockfd - 套接字描述符
        addr - 服务器的地址
        addrlen - 地址的长度
    返回值
        成功 - 0
        失败 - -1 errno被设置为相应的错误值

### recvfrom

    ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags, struct sockaddr *src_addr, socklen_t *addrlen);
    从套接字接收数据 并保存源地址

    注意
        src_addr和addrlen是可选的 如果不需要保存源地址 可以传递NULL
        需要包含头文件
        #include <sys/types.h>
        #include <sys/socket.h>
    参数
        sockfd - 指定了从哪个socket上接收消息
        buf - 指定了存放消息的缓存地址
        len - 指定了buf的有效空间大小
        flags - 标志位
        src_addr - 存放消息的来源地址
        addrlen - 消息的来源地址的的长度
    返回值
        成功 - 返回接收到的字节数
        失败 - -1 errno被设置为相应的错误值

### sendto

    ssize_t sendto(int sockfd, const void *buf, size_t len, int flags, const struct sockaddr *dest_addr, socklen_t addrlen);
    发送数据到指定的地址

    注意
        需要包含头文件
        #include <sys/types.h>
        #include <sys/socket.h>
    参数
        sockfd - 指定了从哪个socket上发送消息
        buf - 指定了发送的消息
        len - 指定了buf的有效空间大小
        flags - 标志位
        dest_addr - 指定了发送消息的目的地址
        addrlen - 消息的目的地址的长度
    返回值
        成功 - 返回发送的字节数
        失败 - -1 errno被设置为相应的错误值


# IO模型
### 五种IO模型

    阻塞IO Blocking I/O
    非阻塞IO Non-blocking I/O
    IO多路复用 I/O Multiplexing     内核一个线程同时监控多个文件描述符(底层用轮询查询多个文件描述符)
        select  最大值受限      小规模      每次都遍历所有
        poll    最大值不受限    中规模      每次都遍历所有
        epoll   最大值不受限    大规模      事件驱动机制只返回发生事件的文件描述符
    信号驱动IO Signal-driven I/O    内核通过信号通知应用，应用可以在信号处理函数里执行读写
    异步IO Asynchronous I/O         应用提交 I/O 请求后立即返回，内核完成后通知应用或调用回调

## select
### 数据结构fd_set

    typedef struct fd_set {
        fd_mask fds_bits[FD_SETSIZE/NFDBITS];
    } fd_set;
    fd_set是一个位图 用于存储文件描述符

    注意
    sizeof(fd_set) = 128 字节 * 8 = 1024 bit


### FD_SET

    void FD_SET(int fd, fd_set *set);
    将文件描述符fd添加到fd_set中 set集合中 fd对应的标志位设置为1

    参数
        fd - 文件描述符
        set - 集合

### FD_CLR

    void FD_CLR(int fd, fd_set *set);
    将文件描述符fd从fd_set中删除 set集合中 fd对应的标志位设置为0

    参数
        fd - 文件描述符
        set - 集合

### FD_ZERO

    void FD_ZERO(fd_set *set);
    将fd_set中的所有标志位设置为0

    参数
        set - 集合

### FD_ISSET

    int FD_ISSET(int fd, fd_set *set);
    判断文件描述符fd是否在set集合中 set集合中fd对应的标志位是否为1

    参数
        fd - 文件描述符
        set - 集合

### 数据结构timeval
    #include <sys/select.h>
    struct timeval{
        time_t tv_sec;
        suseconds_t tv_usec;
    }
### select

    int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
    监控多个文件描述符的读写事件

    参数
    nfds - 三个集合文件描述符的最大值+1
        内核需要线性遍历这些集合中的文件描述符，这个值是循环结束的条件
        在Window中这个参数是无效的，指定为-1即可
    readfds - 监控读事件的文件描述符集合
    writefds - 监控写事件的文件描述符集合
    exceptfds - 监控异常事件的文件描述符集合
    timeout - 超时时间 用来解除select()阻塞
        NULL - 永久阻塞等待
        0 - 非阻塞等待
        大于0 - 阻塞等待指定时间
    返回值
        成功 - 大于0 返回监控的文件描述符的数量
        成功 - 0 超时
        失败 - -1 errno被设置为相应的错误值

## poll

### 数据结构pollfd


    #include <poll.h>
    struct pollfd{
        int fd;             /* 委托内核检测的文件描述符 */
        short events;       /* 委托内核检测文件描述符的什么事件 */
        short revents;      /* 内核检测的结果 文件描述符实际发生的事件 -> 传出参数 */
    }

    /*-------------------------------读事件---------------------------------------*/
    #define POLLIN      0x0001    // 普通或优先带数据可读                       可作为events 和 revents
    #define POLLRDNORM  0x0040    // 普通数据可读                               可作为events 和 revents
    #define POLLRDBAND  0x0080    // 优先级带数据可读                           可作为events 和 revents
    #define POLLPRI     0x0002    // 高优先级数据可读（带外数据，如 TCP OOB）   可作为events 和 revents

    /*-------------------------------写事件---------------------------------------*/
    #define POLLOUT     0x0004    // 普通或优先带数据可写                       可作为events 和 revents
    #define POLLWRNORM  POLLOUT   // 普通数据可写                               可作为events 和 revents
    #define POLLWRBAND  0x0100    // 优先级带数据可写                           可作为events 和 revents

    /*-------------------------------异常事件---------------------------------------*/
    #define POLLERR     0x0008    // 发生错误（I/O 错误、连接异常等）                   只可作为revents
    #define POLLHUP     0x0010    // 连接挂起（对端关闭、写入管道无读者）                只可作为revents
    #define POLLNVAL    0x0020    // 无效请求（文件描述符未打开或非法）                  只可作为revents

### poll

    int poll(struct pollfd *fds, nfds_t nfds, int timeout);
    监控多个文件描述符的读写事件

    参数
        fds - 委托内核检测的文件描述符集合
        nfds - 委托内核检测的文件描述符的数量
        timeout - 超时时间 用来解除poll()阻塞
            NULL - 永久阻塞等待
            0 - 非阻塞等待
            大于0 - 阻塞等待指定时间 ms
    返回值
        成功 - 大于0 返回监控的文件描述符的数量
        成功 - 0 超时
        失败 - -1 errno被设置为相应的错误值

## epoll

### 数据结构epoll_event

    struct epoll_event{
        uint32_t events;      /* 事件类型和标志 */
        epoll_data_t data;    /* 用户数据 */
    };
    typedef union epoll_data {
        void        *ptr;
        int          fd;	// 通常情况下使用这个成员, 和epoll_ctl的第三个参数相同即可
        uint32_t     u32;
        uint64_t     u64;
    } epoll_data_t;

### epoll_create

    int epoll_create(int size);
    创建一个epoll实例 创建管理待检测的文件描述符的集合

    参数
        size - 内核中红黑树的初始大小 在Linux内核2.6.8版本以后，这个参数是被忽略的，只需要指定一个大于0的数值就可以了。
    返回值
        成功 - 返回epoll实例的文件描述符
        失败 - -1 errno被设置为相应的错误值

### epoll_ctl

    int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
    向epoll实例中添加、修改、删除待检测的文件描述符

    参数
        epfd - 指定epoll实例的文件描述符 epoll_create() 函数的返回值
        op - 指定操作
            EPOLL_CTL_ADD - 往epoll模型中添加新的节点
            EPOLL_CTL_MOD - 修改epoll模型中已经存在的节点
            EPOLL_CTL_DEL - 删除epoll模型中的指定的节点
        fd - 文件描述符 即要添加/修改/删除的文件描述符
        event - 指定待检测的事件
            EPOLLIN - 读事件 接收数据, 检测读缓冲区，如果有数据该文件描述符就绪
            EPOLLOUT - 写事件 发送数据, 检测写缓冲区，如果可以发送数据该文件描述符就绪
            EPOLLERR - 异常事件
            EPOLLET - 设置为边沿模式 默认水平模式
    返回值
        成功 - 0
        失败 - -1 errno被设置为相应的错误值

### epoll_wait

    int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
    等待事件的发生

    参数
        epfd - 指定epoll实例的文件描述符 epoll_create() 函数的返回值
        events - 传出参数 用于存放内核检测到的事件
        maxevents - 传出参数 指定events数组的大小
        timeout - 超时时间 用来解除epoll_wait()阻塞
            NULL - 永久阻塞等待
            0 - 非阻塞等待
            大于0 - 阻塞等待指定时间 ms
    返回值
        成功 - 大于0 返回检测到的文件描述符的数量
        成功 - 0 超时
        失败 - -1 errno被设置为相应的错误值