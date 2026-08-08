# 错误处理
## 全局变量errno

    extern int errno;

    系统预定义的整型全局变量。

    在库函数和系统调用出错的时errno自动被设置，然后可以根据errno的值找到描述错误的字符串。

    注意
        #include <errno.h>

        man fopen  查看手册内部说明是否支持errno


## strerror

    char *strerror(int errnum);

    strerror函数将错误代码转换为错误信息

    注意
        #include <string.h>
    参数
        errnum - 错误代码
    返回值
        成功 - 找到错误的编号，返回描述错误的字符串的首地址
        失败 - 找不到错误的编号，返回“Unknown error nnn”字符串的首地址
## perror

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

## dlopen

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
## dlclose

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
## dlsym

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

## dlerror

    const char *dlerror(void);
    获取动态库的错误信息

    注意
        #include <dlfcn.h>
    返回值
        成功 - 错误信息
        失败 - NULL

# 进程与线程管理

## 进程管理
### 进程创建

#### fork
    pid_t fork(void) 
    创建一个子进程
	引用：#include <unistd.h>
		
    返回值 :
		父进程中，返回-1，代表新建子进程失败 返回子进程的pid，代表新建子进程成功
		子进程中，返回0.

#### getpid
	pid_t getpid(void)获取当前进程的pid
		引用：#include <unistd.h>
        返回值 : 返回当前进程的pid

### 进程资源回收

#### wait
    pid t wait(int *status)
    阻塞等待子进程结束，然后回收子进程的资源
    参数: 
        status:用于存储子进程的退出状态码
    返回值: 
        成功 终止子进程的pid错误 
        -1 errno做相应的设置

#### waitpid
	pid_t waitpid(pid_t pid, int *status, int options)
    
    阻塞等待子进程结束，然后回收子进程的资源

    参数 : 
        pid: 指定要回收的子进程的pid
            <-1: pid的绝对值指定了进程组的id。等待该组的子进程的终止
            -1:等待任意子进程
            0:等待和父进程同组的子进程
            >0: pid的值指定了要等待的子进程的pid
        status:用于存储子进程的退出状态码
        options:
            0 阻塞等待子进程的结束
            WNOHANG 非阻塞
    返回值: 
        成功 终止子进程的pid。如果 options的值为WNOHANG，要回收的子进程还没有结束，返回0。
        错误 -1 errno做相应的设置

#### 终止检测宏
	WIFEXITED(status)       判断子进程是否是正常终止
	WEXITSTATUS(status)     提取子进程正常退出时返回的退出码

	WIFSIGNALED(status)     判断子进程是否因未被捕获的信号而异常终止
    WTERMSIG(status)        提取导致子进程异常终止的信号编号

### 进程替换

#### execve

    int execve(const char *filename, char *const argv [],char *const envp[]);程序的执行
        参数 :
            filename: 指定可执行文件的名字filename必须是二进制可执行文件或者是#!开头的脚本文件
            argv:这是传递给新的可执行程序的一个字符串数组。通常第一个字符串是可执行文件的名字。字符串数组以NULL作为结束标志。
            envp: 这也是一个字符串数组，传递给新的进程的环境变量列表。环境变量的格式为name=value。字符串数组以NULL作为结束标志。
        返回值 : 
            成功 不返回为什么不返回 ?
            错误 -1 errno做相应的设置

    以下函数都是根据 execve 实现
    int execl(const char *path, const char *arg, .../* (char *) NULL */);
    int execlp(const char *file, const char *arg, ... /* (char *) NULL */);
    int execle(const char *path, const char *arg, .../*,(char *) NULL, char * const envp[] */)；
    int execv(const char *path, char *const argv[]);
    int execvp(const char *file, char *const argv[]);
    int execvpe(const char *file, char *const argv[],char *const envp[]);

        说明
        l:  传参方式list
        v : 传参方式vector
        p : 跟PATH环境变量相关。指定查找可执行程序的路径
        e: 加载程序的时候，传入环境变量。

### 进程退出

#### exit
    void exit(int status)
    使进程正常终止

    引用：#include <stdlib.h>
    参数:
        子进程设置status
        父进程接收status&0377的值，调用wait()来回收
    返回值 : 无


### 进程环境变量

#### environ

    extern char const **environ；			
        全局变量 指向了当前进程的环境变量列表
            使用时 使用 extern char **environ;声明即可

#### envp

    int main(int argc,char *argv[],char *envp[]);
        在main函数中使用envp来访问当前进程的环境变量列表

#### getenv
    char *getenv(const char *name);

    获取环境变量name的值

    参数 :	 name 指定环境变量的名字
    返回值 :
        成功 返回环境变量name的值的首地址
        返回NULL代表没有找到这个环境变量

#### setenv
    int setenv(const char *name, const char *value, int overwrite);
    如果环境变量存在，根据overrite的值对环境变量操作。如果不存在，创建环境变量

    参数 : 
        name 环境变量的名字
        value 环境变量的值
        overwrite 
            0 如果环境变量已经在列表中，不改变环境变量的值
            非0 如果环境变量已经在列表中，使用value的值替换掉原来的值
    返回值 : 
        成功 返回 0
        错误-1 errno被设置为相应的错误值

#### putenv
    int putenv(char *string);

    功能：用于添加一个新的环境变量，或修改一个已有环境变量的值

    参数 
        string: 是一个指向字符串的指针，格式必须为 "name=value"。
            name：要设置或修改的环境变量名称。
            value：要设置的值

    返回值：
        成功：返回 0。
        失败：返回 -1（非零值），并设置 errno 以指示错误原因

    注意：
        把变量设置为环境变量，变量改变则环境变量也会改变

#### unsetenv
    int unsetenv(const char *name);
    从环境变量列表中删除环境变量，如果环境变量不存在，什么都不做
    参数: name 环境变量的名字
    返回值: 
        成功 返回 0
        错误 -1 errno被设置为相应的错误值

#### clearenv
    int clearenv(void);
    清除进程的环境变量列表并将全局变量environ设置为NULL。
    返回值：
        成功 0
        错误 非0

### 进程遗言

#### atexit
    int atexit(void (*function)(void))

    向进程注册遗言函数function，进程调用return或者exit从main函数返回的时候执行

    引用：#include <stdlib.h>
    参数: function:指定遗言函数的入口地址
    返回值 : 成功 0 错误 非0
    注意：
        遗言函数的注册顺序和调用顺序相反
        遗言函数注册一次会被调用一次
        子进程继承父进程的遗言函数
        进程的映像被更换的时候，进程的遗言函数也被覆盖

#### on_exit   
    int on_exit(void (*function)(int , void *), void *arg)
    向进程注册遗言函数function
    引用：#include <stdlib.h>
    参数：
        function:指定遗言函数的入口地址
            int: 进程终止返回的status，不&0377
            void*  接收arg
        arg:传递给function函数的唯一参数
    返回值:成功 0错误 非0

## 线程管理

### 线程创建

#### pthread_create
    int pthread_create(pthread_t *thread, const pthread_attr_t *attr,void *(*start_routine)(void *), void *arg);

    在当前进程中创建一个新的线程

    参数: 
        thread:存放新建线程的tid的空间
        attr:指定新建线程的属性。缺省为NULL.start 
        routine:线程执行函数
        arg:传给函数start_routine的唯一参数
    返回值: 
        成功 0
        失败 返回错误码
    注意：Compile and link with -pthread

#### pthread_self
    pthread_t pthread_self(void)
    
    获取当前线程的tid

    返回值: 这个函数总是成功执行，返回当前线程的id.
    
    注意：Compile and link with -pthread.

### 线程资源回收

#### pthread_detach
    int pthread_detach(pthread_t thread);

    设置指定线程为分离状态。

    参数 : thread 指定线程的id。将该线程设置为分离状态

    返回值 :
        成功 0
        错误 返错误码
    注意：设置为分离状态的线程，在线程终止的时候，自动向系统释放该线程的资源。不需要调用pthread join(3)回收该线程的资源
        不要向已经标记为分离状态的线程再次设置为分离状态，也不要调用pthread join(3)回收该线程的资源。

#### pthread_join
    int pthread_join(pthread_t thread, void **retval);
    
    设置指定线程为join状态

    参数 : 
        thread 指定线程的id。将该线程汇合。
        retval 将汇合线程的退出状态码存储到*retval中。
    返回值 : 
        成功 0
        错误 返回错误码

### 线程退出

#### pthread_exit

    void pthread_exit(void *retval);
    终止当前线程
        
    参数: retval 传递给一进程中的另外一个线程( 调用pthread join(3)的线程)的退出状态码。

#### pthread_cancel
    int pthread_cancel(pthread_t thread);
    
    向指定线程发送取消请求
        参数 : thread 指定线程的id。向该线程发送取消请求。
        返回值 : 
            成功 0错误 
            返回错误码
        注意：被取消的线程终止以后，调用pthread join(3)回收线程的退出状态码为PTHREAD CANCELED.



# 进程间通信与同步

## 通信与同步简介

    内核同步
        中断屏蔽
        原子操作 (不会被中断打断的操作，保证数据一致性)
        自旋锁 (未获取锁的进程处于自旋状态是要消耗cpu资源的 针对多核设计)
        信号量 (获取不到信号量时进程进入休眠，不消耗CPU资源)
        互斥体 (获取不到互斥体时进程进入休眠，不消耗CPU资源，比信号量更轻量)
        RCU (Read-Copy-Update)：一种极其高效的同步机制
    进程/线程
        IPC（进程间通信）
            System V IPC /POSIX IPC
                消息队列
                信号量
                共享内存
            管道  PIPE/FIFO
            Socket
        线程同步-POSIX 标准同步   (futex Fast Userspace Mutex 底层)
            自旋锁（Spinlock）
            互斥锁（Mutex）
            条件变量（Condition Variable）
            POSIX 信号量（Semaphore）
            读写锁（RWLock）
            屏障（Barrier）
        事件机制
            事件通知eventfd
            信号异步通知signal
            文件同步  fcntl
##	System V IPC 

### ftok
    key_t ftok(const char *pathname, int proi_id);

    用随意一个有效文件名和随机生成一个唯一的system v ipc的键值引用

    引用:
        #include <sys/types.h>
        #include <sys/ipc.h>
    参数:
        pathname:指定一个有效的文件名
        proi_id:不能是0.
    返回值: 
        成功 返回键值
        错误 -1 errno被设置
    注意: pathname和proi id的值都相同的时候得到的结果值相同


###	System V IPC 消息队列

#### msgget
    int msgget(key_t key, int msgflg)
        获取 IPC 对象唯一标识id
        引用
            #include <sys/types.h>
            #include <sys/ipc.h>
            #include <sys/msg.h>
        参数
            key	key 值
            msgflg 	访问权限
        返回值 
            成功返回消息队列的 ID，
            失败-1

#### msgsnd

    int msgsnd(int msqid, const void *msgp, size_t msgsz, int msgflg)
        
        发送数据
        
        引用
            #include <sys/types.h>
            #include <sys/ipc.h>
            #include <sys/msg.h>
        参数
            msqid 消息队列 ID
            msgp 指向消息类型的指针
            msgsz 发送的消息的字节数。
            msgflg 
                如果为 0，直到发送完成函数才返回，即阻塞发送
                IPC_NOWAIT：消息没有发送完成， 函数也会返回，即非阻塞发送
        返回值 
            成功返回 0
            失败返回-1

#### msgrcv       
    ssize_t msgrcv(int msqid, void *msgp, size_t msgsz, long msgtyp, int msgflg)
        接收消息
        参数
            msqid IPC 对象对应的 id
            msgp 消息指针，消息包含类型和字段
            msgsz 消息里的字段大小
            msgtyp 消息里的类型
            msgflg 位掩码，不止一个
        返回值 
            成功返回接收到的字段大小
            错误返回-1

#### msgctl
    int msgctl(int msqid, int cmd, struct msqid_ds *buf)\
        控制操作，删除消息队列对象等
        引用
            #include <sys/types.h>
            #include <sys/ipc.h>
            #include <sys/msg.h>
        参数
            msqid 消息队列的 ID
            cmd 
                IPC_STAT：读取消息队列的属性，然后把它保存在 buf 指向的缓冲区。
                IPC_SET：设置消息队列的属性，这个值取自 buf 参数
                IPC_RMID：删除消息队列
            buf 	消息队列的缓冲区
        返回值 
            成功返回 0
            失败返回-1

###	System V IPC 信号量

#### semget

    int semget(key_t key, int nsems, int semflg)
    创建一个新信号量或取得一个已有信号量

        引用
            #include <sys/types.h>
            #include <sys/ipc.h>
            #include <sys/sem.h>
        参数
            key 信号量的键值
            nsems 信号量的数量
            semflg 标识
        返回值 
            成功返回信号量的 ID
            失败返回 -1

#### semop

    int semop(int semid, struct sembuf *sops, size_t nsops)
    执行信号量 PV
        引用
            #include <sys/types.h>
            #include <sys/ipc.h>
            #include <sys/sem.h>
        参数
            semid 信号量 ID
            *sops 信号量结构体数组
                    struct sembuf{
                        unsigned short sem_num; //要操作的信号量的编号
                        short sem_op;		//P/V 操作，1 为 V 操作，释放资源。-1 为 P操作，分配资源。0 为等待，直到信号量的值变成 0
                        short sem_flg; //0 表示阻塞，IPC_NOWAIT 表示非阻塞
                    }
            nsops信号量数量

#### semctl

    int semctl(int semid, int semnum, int cmd, union semun arg)
    信号量控制
        引用
            #include <sys/types.h>
            #include <sys/ipc.h>
            #include <sys/sem.h>
        参数
            semid 信号量id
            semnum 信号量编号
                    union semun {
                        int val;
                        struct semid_ds *buf;
                        unsigned short *array;
                        struct seminfo *__buf;
                    }
            cmd 
                IPC_STAT(获取信号量的属性) 
                IPC_SET(设置信号量的属性)
                IPC_RMID (删除信号量)
                SETVAL(设置信号量的值)
            arg 

###	System V IPC 共享内存

####	shmget

    int shmget(key_t key, size t size, int shmflg);
    分配一个system_v 的共享内存段
        引用：
            #include <sys/ipc.h>
            #include <sys/shm.h>
        参数: 
            key ftok(3)的返回值
            size 指定了共享内存段的大小
            shmflg:
                IPC CREAT
                IPC EXCL
                mode
        返回值:
            成功 返回共享内存段的id
            失败-1 errno被设置为相应的错误码
####	shmat

    void *shmat(int shmid, const void *shmaddr, int shmflg);
    将共享内存段附加到进程的地址空间
        引用：
            #include <sys/types.h>
            #include <sys/shm.h>
        参数:
            shmid: 指定了共享内存段的id.将这个共享内存段附加到进程的地址空间
            shmaddr:为NULL表示 系统选择进程的具体地址空间
            shmflg:通常为 0，表示共享内存可读可写，或者为 SHM_RDONLY，表示共享内存可读可写
        返回值:
            成功 返回附加到进程的具体地址
            错误 (void *) -1 errno被设置为相应的错误码
#### shmdt

    int shmdt(const void *shmaddr)
    删除地址映射
        引用
            #include <sys/types.h>
            #include <sys/shm.h>
        参数： 共享内存映射后的地址
        返回值 ：成功返回 0，失败返回 -1

#### shmctl

    int shmctl(int shmid, int cmd, struct shmid_ds *buf)
    销毁共享内存
        引用
            #include <sys/ipc.h>
            #include <sys/shm.h>
        参数 
            shmid 要删除的共享内存的标识符
            cmd 
                IPC_STAT (获取对象属性) 
                IPC_SET (设置对象属性) 
                IPC_RMID(删除对象)
            buf 
                指定 IPC_STAT (获取对象属性) IPC_SET (设置对象属性) 时用来保存或者设置的属性

## 	POSIX IPC 
### 	POSIX IPC 消息队列

####  mq_open
    消息队列 (Message Queue)   

### POSIX IPC 信号量

#### sem_post

    信号量 (Semaphore)    
        有名信号量 
        无名信号量

### POSIX IPC 共享内存

####  shm_open

    共享内存 (Shared Memory)   

## 管道 PIPE/FIFO

### pipe 无名管道PIPE

    int pipe(int pipefd[2])
    创建一个单工的无名管道
    引用：#include <unistd.h>
    参数: pipefd 指定一个有两个整型元素的数组名字。
        pipefd[0] 指向管道读端 
        pipefd[1] 指向管道写端
    返回值 : 
        成功 返回0
        错误 返回-1 errno被设置为相应的错误值

### mkfifo 有名管道FIFO

    int mkfifo(const char *pathname, mode t mode);
    创建一个有名管道文件
    参数 : 
        pathname 指定要创建的文件的名字(管道类型的文件)。
        mode: 指定管道文件的权限
    返回值:
        成功 返回0
        错误 返回-1 errno被设置为相应的错误值。

## POSIX 标准同步
### POSIX 自旋锁(Spinlock)
### POSIX 互斥锁(Mutex)

#### pthread_mutex_t
    pthread_mutex_t 互斥锁类型

#### PTHREAD_MUTEX_INITIALIZER
    pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER；
    静态初始化mutex锁

#### pthread_mutex_init
    int pthread_mutex_init(pthread_mutex_t *mutex,const pthread_mutexattr_t *mutexattr)
    使用mutex锁的属性初始化mutex锁
        参数: 
            mutex 指定要初始化的锁的地址
            mutexattr 指定线程锁的属性。NULL使用缺省的属性初始化mutex锁
        返回值 : 总是返回 0
#### pthread_mutex_destroy
    int pthread_mutex_destroy(pthread_mutex_t *mutex)
    销毁mutex锁，释放mutex锁hold的资源
        参数: mutex 指定要销毁的锁的地址
        返回值 :成功 返回 0 错误 非的错误码
#### pthread_mutex_lock
    int pthread_mutex_lock(pthread_mutex_t *mutex) 
    锁定mutex锁，如果锁被其他线程占用，阻塞等待，直到占用该锁的线程释放锁。否则，立即上锁返回
        参数 : mutex 指定要操作的锁
        返回值 : 成功 返回 0 错误 非的错误码
#### pthread_mutex_trylock
    int pthread_mutex_trylock(pthread_mutex_t *mutex)
    尝试加锁。如果锁被其他线程占用，立即返回错误;否则，立即加锁并返回
        参数: mutex 指定要操作的锁
        返回值 : 成功 返回 0 错误 非的错误码
#### pthread_mutex_unlock
    int pthread_mutex_unlock(pthread_mutex_t *mutex)
    释放锁
        参数: mutex 指定要操作的锁
        返回值 : 成功 返回 0 错误 非0的错误码


### POSIX 条件变量(Condition Variable)

#### pthread_cond_t
    pthread_cond_t 条件变量类型
    
        条件变量是一个同步设备，条件不满足的情况下，暂停执行和释放处理器，直到条件被满足为止。
        条件变量的基本操作。
            发送条件变量( 条件变为真的时候)
            等待条件满足( 条件不满足的时候 )

#### PTHREAD_COND_INITIALIZER
    pthread_cond_t cond = PTHREAD_COND_INITIALIZER
    静态初始化一个条件变量



#### pthread_cond_init
    int pthread_cond_init(pthread_cond_t *cond, pthread_condattr_t *cond_attr)
    使用条件变量的属性初始化一个条件变量
        参数 : 	
            cond 指定要初始化的条件变量
            cond_attr 指定条件变量的属性	NULL 取条件变量的默认属性
        返回值 : 成功 返回 0 错误 非0的错误码
#### pthread_cond_destroy
    int pthread_cond_destroy(pthread_cond_t *cond)
    销毁条件变量，释放条件变量hold的资源
        参数: cond 指定要销毁的条件变量的地址
        返回值 : 成功 返回 0 错误 非0的错误码
#### pthread_cond_signal
    int pthread_cond_signal(pthread_cond_t *cond)
    如果线程在等待条件变量为真，从其中选出一个执行。如果没有线程等待条件变量为真，什么都不做。
        参数: cond 指定要操作的条件变量的地址
        返回值 : 成功 返回 0 错误 非的错误码
#### pthread_cond_broadcast
    int pthread_cond_broadcast(pthread_cond_t *cond)
    通知多有的等待条件变量为真的线程执行。如果没有线程等待条件变量为真，什么都不做
        参数: cond 指定要操作的条件变量的地址
        返回值 : 成功 返回 0 错误 非的错误码
#### pthread_cond_wait
    int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex)
    原子的解锁并等待条件变量变为真。当条件变量为真的时候，自动重新获取mutex锁
        参数: 
            cond 指定要操作的条件变量的地址
            mutex 指定使用的mutex锁
        返回值 : 成功 返回 0 错误 非0的错误码
#### pthread_cond_timedwait
    int pthread_cond_timedwait(pthread_cond_t *cond, pthread_mutex_t *mutex,const struct timespec *abstime)
    在指定的时间内没有等到，立即返回错误 abstime指定了等待的时间
        参数: 
            cond 指定要操作的条件变量的地址
            mutex 指定使用的mutex锁
            abstime 指定等待的时间
        返回值 : 成功 返回 0 错误 非0的错误码


### POSIX 信号量(Semaphore)

#### sem_t
    sem_t 信号量类型

#### sem_init
    int sem_init(sem_t *sem, int pshared, unsigned int value)
    初始一个匿名的信号量
        参数 : 
            sem 指定要初始化的匿名信号量的地址
            pshared 
                0 代表多线程 
                非0 多进程
            value 指定信号量的初始值
        返回值 : 成功 返回 0 错误 1 errno被设置相应的错误码
#### sem_destroy
    int sem_destroy(sem_t *sem)
    销毁指定的信号量
        参数 : sem 指定要销毁的信号量的地址
        返回值 : 成功 返回 0 错误 -1 errno被设置相应的错误码
        注意 : 使用sem destroy(3)只能销毁使用sem init(3)初始化的信号量
#### sem_post
    int sem_post(sem_t *sem)
    解锁指定的信号量，信号量的值加1。如果有线程或进程调用sem_wait(3)阻塞在该信号量，则被唤醒，继续锁定信号量。
        参数: sem 指定要操作的信号量的地址
        返回值 : 成功 返回 0 错误 -1 errno被设置相应的错误码
#### sem_wait
    int sem_wait(sem_t *sem)
    信号量的值减1操作。如果当前信号量的值为0，阻塞等待直到其他进程或线程使该信号量的值大于0为止。
        参数: sem 指定要操作的信号量的地址
        返回值 : 成功 返回 0 错误 -1 errno被设置相应的错误码。
#### sem_trywait
    int sem_trywait(sem_t *sem)
    尝试减一操作，如果当前信号量的值为0，立即返回，返回错误
        参数: sem 指定要操作的信号量的地址
        返回值 : 成功 返回 0 错误 -1 errno被设置相应的错误码
#### sem_timedwait
    int sem_timedwait(sem_t *sem, const struct timespec *abs_timeout)
    指定了等待的时长。如果超时，返回错误
        参数 :
            sem 指定要操作的信号量的地址
            abs_timeout 指定等待的时长
        返回值 : 成功 返回 0 错误 1 errno被设置相应的错误码。


### POSIX 读写锁(RWLock)
### POSIX 屏障(Barrier)

## 事件机制
### 事件通知eventfd
### 信号异步通知signal

    信号是提供异步事件处理机制的软件中断
    
    信号有一个非常明确的生命周期
        首先，信号被生成，并被发送至系统内核
        其次，系统内核存储信号，直到可以处理它
        - 最后，一旦有空闲，内核即按以下三种方式之一处理信号
            忽略信号:什么也不做。SIGKILL和SIGSTOP信号不能忽略
            捕获信号: 内核暂停收到信号的进程正在执行的代码，跳转到事先注册的信号处理函数，执行该函数并返回，跳回到捕获信号的地方继续执行。SIGKILL和SIGSTOP信号不能捕获
            默认操作: 不同信号有不同的默认操作，通常是终止收到信号的进程，但也有一些信号的默认操作是视而不见，即忽略
            
    信号的产生
        信号的产生有三种方式：
            1由硬件产生，如从键盘输入 Ctrl+C 可以终止当前进程
            2异常，进程异常时会发送信号
            3由其他进程发送，如可在 shell 进程下，使用命令 kill -信号标号 PID，向指定进程发送信号。

#### kill 信号产生
    int kill(pid t pid, int sig);
    向进程发送指定信号
    引用：
        #include <sys/types.h>
        #include <signal.h>
    参数 : 
        pid:指定目标进程的pid
        sig: 指定信号的编号
    返回值: 
        成功 返回0
        失败-1 将错误的编号设置到error中
    扩充: 给进程自己发送信号。kill(getpid(),sig)。这也是raise(3)的实现

#### raise
    int raise(int sig)
    向自身发送信号等同于kill(getpid(),sig)
#### alarm

    unsigned_int alarm(unsigned_int seconds);
    设定的时间超过后产生 SIGALARM 信号，默认动作是终止进程
    引用：#include <unistd.h>
    参数: seconds:指定的秒数
    返回值 :返回上次设置的闹钟的未决时间值(还有多长时间要执行)。如果上次闹钟已经执行，返回0.
    注意:alarm(0) 取消原来设置的闹钟

#### pause 信号的接收
    int pause(void)
    使当前进程进入睡眠状态，直到有信号到达
        引用：#include <unistd.h>
        返回值 :进程被信号中断后一直返回-1

#### signal 信号处理

    sighandler_t signal(int signum, sighandler t handler)
    向进程注册信号处理函数

    #include <signal.h>

    参数:
        signum: 指定信号的编号
        handle: 信号处理函数的入口地址
            typedef void (*sighandler t)(int)
            SIG_IGN忽略该信号
            SIG_DFL默认处理方式
            
    返回值: 
        成功返回原来的信号处理函数的地址
        失败 SIG ERR 将错误的编号设置到error中失败
    注意: SIGKILL和SIGSTOP两个信号不能被捕获和忽略

####  sigset_t 进程的掩码集和未决集

    blocking 掩码集   0不屏蔽该信号  1屏蔽该信号
    pending  未决集   0信号没有发生  1信号发生还未处理


    typedef struct{
        unsigned long int _val[(1024 / (8 * sizeof (unsigned long int)))];
    }_sigset_t;
    typedef_sigset _t sigset_t;	//信号集类型
    unsigned long int val[32]；


    int sigemptyset(sigset_t *set);
        将信号集set初始化为空，也就是不包含任何信号
        参数: set 指定要初始化的信号集的地址
        返回值: 
            成功 0 
            错误 -1 errno被设置为相应的错误号
    int sigfillset(sigset_t *set);
        将信号集set初始化为满，也就是包含所有信号
        参数: set 指定要初始化的信号集的地址
        返回值 : 
            成功 0 
            错误 -1 errno被设置为相应的错误号
    int sigaddset(sigset_t *set, int signum);
        将信号signum添加到信号集set中
        参数: 
            set 指定已经初始化过的具体的信号集
            signum 指定具体的信号
        返回值 : 
            成功 0
            错误 -1 errno被设置为相应的错误号
    int sigdelset(sigset_t *set, int signum)
        将信号signum从信号集set中移除
        参数: 
            set 指定已经初始化过的具体的信号集
            signum 指定具体的信号
        返回值 :
                成功 0
                错误 -1 errno被设置为相应的错误号
    int sigismember(const sigset t *set, int siqnum)
        测试信号signum是否是信号集set中的一员
        参数:
            set 指定已经初始化过的具体的信号集
            signum 指定具体的信号
        返回值: 错误 -1 errno被设置为相应的错误号
            成功	1	信号signum是set信号集中的一员
                0	信号signum不是set信号集中的一员
#### sigprocmask
    int sigprocmask(int how, const sigset_t *set, sigset t *oldset);
    设置进程的信号掩码集
    引用：#include <signal.h>
    参数 :
        how 可以取以下三个值的其中之一:
            SIG_BLOCK 将set信号集合原来的信号集做并集操作的结果设置为进程的信号掩码集
            SIG_UNBLOCK 将set中的信号从原来的信号集中移除，结果设置为进程的信号掩码集
            SIG_SETMASK 将set信号集设置为进程的信号掩码集
        set 指定具体的信号集
        oldset 用于保存原来的信号集。如果设置为NULL，表示不保存原来的信号集
    返回值 :
        成功 0
        错误 -1 errno被设置为相应的错误码

#### sigpending
    int sigpending(sigset t *set)
    获取进程的未决信号集
        引用：#include <signal.h>
        参数:set将进程的未决信号集填充到set指定的地址空间里
        返回值 :
            成功0
            错误 -1 errno被设置为相应的错误码
        注意:获取进程未决信号集后，可以使用 sigismember(3)来判断信号是不是未决信号集中的一员，如果是，代表信号处于未决状态，否则，信号不是未决状态



### 文件同步  fcntl

# 内存管理

## mmap
    void *mmap(void *addr, size t length, int prot,int flags,int fd, off t offset)
    将设备或文件映射到进程的虚拟地址空间
        参数:
            addr:指定了映射区域的起始地址。如果addr指定为NULL有内核选择映射区域的起始地址
            length:指定了映射区域的长度
            prot:
                PROT_EXEC Pages may be executed
                PROT_READ Pages may be read.
                PROT_WRITE Pages may be written.
                PROT_NONE Pages may not be accessed
            flags:二选一
                MAP SHARED:对映射区域的更新同步到底层文件中,也能被映射到同一文件的其它进程所见.
                MAP_PRIVATE:私有的写时拷贝的映射区域它对映射区域数据的更新,不被同步到文件中,也不被映射同一文件的其它进程所见.
                按位或到flags中
                MAP ANONYMOUS:匿名映射,不支持任何文件的映射.如果这个标记被指定.fd和offset被忽略 fd -1. offset 0
            fd:指定了要映射的文件的描述符
            offset:指定了映射区域的起始位置.必须是页的整数倍
        返回值:
            错误 MAP_FAILED errno被设置
            成功 返映射区域的起始地址
## munmap
    int munmap(void *addr, size t length)
    解除文件的映射
        参数:
            addr:指定了映射区域的起始地址
            length:指定了映射区域的长度
        返回值:
            成功  0
            错误 -1 errno被设置
        注意:关闭文件不影响已经建立映射的文件


# 文件管理

## 文件描述符

### open
    int open(const char *pathname, int flags,...)
    打开一个文件,有可能创建一个文件
        引用：
            #include <sys/types.h>
            #include <sys/stat.h>
            #include <fcntl.h>
        参数:
            pathname:指定了要打开的文件的路径
            flags 从以下选项中选择一个
                O_RDONLY 以只读方式打开文件
                O_WRONLY 以只写的方式打开文件
                O_RDWR 以可读可写的方式打开文件
                文件的创建标记和身份标记可以被按位或到flags中
                    O_CREAT:文件不存在,创建文件.通过mode指定文件的权限
                    文件的最终权限有可能被进程的umask修改.mode & ~umask
                    O_EXCL:如果文件存在,这个标记和O_CREAT一起被指定的时候,这个调用返回失败
                    O_TRUNC:如果文件存在,打开的时候有写的方式,文件的内容将被清空为0.
                    O_APPEND:以追加的方式打开文件,文件的读写位置被定位在文件的末尾.
            ...可变参数 参数的个数和类型取决于flags
        返回值:
            成功 返回一个非负的文件描述符
            错误 -1 errno被设置为相应的值
### close
    int close(int fd)
    关闭一个文件描述符,当前进程拥有的这个文件的所有记录锁都被移除;如果这个指向底层描述符的最后一个文件描述符,跟这个描述符相关的资源也被释放
        引用：#include <unistd.h>
        参数:fd:指定了要关闭的文件描述符
        返回值:
            成功0
            错误 -1 errno被设置为相应的错误码
### read
    ssize t read(int fd, void *buf, size t count)
    从文件描述符中读取数据
        引用:#include <unistd.h>
        参数:
            fd:指定了具体的文件
            buf:从文件中读取到的数据存放在这里
            count:指定最多读取的字节数
        返回值:
            错误 1 errno被设置
            成功 返回读取到的字节数 0代表到达了文件的末尾
    ssize t write(int fd, const void *buf, size t count)向指定的文件写入数据
        引用:#include <unistd.h>
        参数:
            fd:指定了具体的文件
            buf:指定了写入数据存放的地址
            count:指定了写入文件的最大字节数
        返回值:
            错误 -1 errno被设置
            成功 返回实际写入文件的字节数
### lseek
    off_t lseek(int fd, off_t offset, int whence)
    重新定位文件的读写位置
        引用：
            #include <sys/types.h>
            #include <unistd.h>
        参数: 
            fd 指定了文件
            offset 指定了一个字节数
            whence:
                SEEK_SET:位置被设置在文件的第offset个字节处
                SEEK_CUR:位置被设置在当前位置+offset字节处
                SEEK_END:位置被设置在文件的大小+offset字节处
        返回值:
            错误 -1 errno被设置
            成功 返回位置距离文件开头的字节数
### dup
    int dup(int oldfd)  
    
    找一个最小的未使用的文件描述符  也指向 oldfd
        
        引用:#include <unistd.h>
        参数:oldfd:源描述符
        返回值:
            成功 最小的未使用的文件描述符,作为新的文件描述符
            错误 -1 errno被设置
### dup2
    int dup2(int oldfd, int newfd)
    
    用newfd 指向 oldfd
  
        参数:
            oldfd:源描述符
            newfd:目标描述符
        返回值:
            成功 返回newfd
            失败 -1 errno被设置

### struct flock

	struct flock {
		...
		short	l_type;		/*Type of lock: F_RDLCK,F_WRLCK, F_UNLCK */锁的类型
		short	l_whence; 	/* How to interpret  l_start:SEEK_SET, SEEK_CUR, SEEK_END */
		off_t	l_start;	               /* Starting offset for lock */
		off_t	l_len;		/* Number of bytes to lock */
		pid_t	l_pid;		/* PID of process blocking our lock(set by F_ETLK and F_FD_ETLK) */
		...
	}；
### fcntl
	int fcntl(int fd, int cmd, ... )对文件加锁
		引用：
			#include <unistd.h>
			#include <fcntl.h>
		参数:
			fd:指明被操作的文件描述符
			cmd:指定了命令,对这个文件描述符操作的命令
			F_SETLK:设置锁,如果有互斥锁被其它进程占有,立即返回,返回错误 errno被设置
			F_SETLKW:设置锁,如果有互斥锁被其它进程占有,等待其它进程解锁
			F_GETLK:测试加锁如果可以加锁,l_type被设置为F_UNLCK 如果有互斥锁，将持有互斥锁的进程的pid填写到l_pid字段
			...可变参数
		返回值:
			成功 0
			错误 -1将错误码设置到errno变量中

## 文件系统

### 文件系统基础操作 

####  chdir
    chdir           更改当前工作目录。效果类似在 Shell 中执行 cd 命令，影响当前进程。
#### getcwd
    getcwd          获取当前工作目录的绝对路径字符串，效果类似 Shell 的 pwd 命令。

### 文件元数据 
####  struct stat
    struct stat{       //元数据结构体
        dev_t 		st_dev; 	/* ID of device containing file*/
        ino_t 		st_ino;		/* inode number */		唯一Inode号
        mode_t 	st_mode;	    /* protection */		类型与权限字段
        nlink_t 	              st_nlink;	/* number of hard links */	硬链接数
        uid_t		st_uid;		/* user ID of owner */		用户ID
        gid_t		st_gid;		/* group ID of owner */		用户组ID
        dev_t		st_rdev; 	/* device ID (if special file) */
        off_t 		st_size;	/* total size, in bytes */
        blksize_t 	st_blksize;	/* blocksize for filesystem I/O */
        blkcnt_t 	st_blocks;	/*number of 512B blocks allocated */
        struct timespec st_atim; 	/* time of last access */	访问时间: 文件内容被最后一次读操作的时间，例如像: cat、 more等操作 但是state 还有ls命令不影响
        struct timespec st_mtim;	/* time of last modification */ 修改时间: 文件内容被最后一次修改的时间，例如vim对文件进行编辑保存
        struct timespec st_ctim;	              /*time of last status change*/  状态时间: 文件的状态最后一次被改变的时间，例如当使用chmod.chown等改变文件属性的操作
        
        #define st_atime st_atim.tv_sec	/*Backward compatibility */
        #define st_mtime st_mtim.tv_sec
        #define st_ctime st_ctim.tv_sec
    };
#### stat
    int stat(const char *pathname,struct stat *buf)获取文件的元数据
        引用：
            #include <sys/types.h>
            #include <sys/stat.h>
            #include <unistd.h>
        参数:
            pathname:指定文件的路径
            buf:用来存储文件元数据的空间地址
        返回值:
            成功0
            错误 -1 errno被设置

#### 文件类型宏定义
    S_IFMT 		0170000 	bit mask for the file type bit fields
    S_IFSOCK 	0140000 	socket
    S_IFLNK		0120000		symbolic link
    S_IFREG	    0100000		regular file
    S_IFBLK		0060000 	block device
    S_IFDIR		0040000		directory
    S_IFCHR	    0020000 	character device
    S_IFIF		O0010000 	FIFO

    S_ISREG(st mode) is it  regular file?
    S_ISDIR(st mode) directory?
    S_ISCHR(st mode) character device?
    S_ISBLK(st mode) block device?
    S_ISFIFO(st mode) FIFO (named pipe)?
    S_ISLNK(st mode) symbolic link? (Not in POSIX.1-1996.)
    S_ISSOCK(st mode) socket? (Not in POSIX.1-1996.)

#### 文件权限宏定义
    S_IRWXU 	00700		mask for file owner permissions
    S_IRUSR 	00400		owner has read permission
    S_IWUSR 	00200		owner has write permission
    S_IXUSR	00100		owner has execute permission
    S_IRWXG	00070		mask for group permissions
    S_IRGRP	00040		group has read permission
    S_IWGRP	00020		group has write permission
    S_IXGRP	00010		group has execute permission
    S_IRWXO 	00007		mask for permissions for others (not in group)
    S_IROTH  	00004		others have read permission
    S_IWOTH 	00002		others have write permission
    S_IXOTH 	00001		others have execute permission

#### access 检查权限
    access          检查权限（非文件夹专属）。测试当前进程（按实际 UID/GID）对某个文件/目录是否拥有读/写/执行权限。
#### chmod
    chmod           修改权限（非文件夹专属）。改变文件或目录的访问权限位（如 rwxr-xr-x）。

### 软链接和硬链接

#### link
    link            创建硬链接。为现有的 inode（文件实体）再增加一个目录项（文件名），硬链接数 nlink 加 1。

#### unlink
    unlink          删除目录项（文件名），并将 inode 的硬链接计数减 1。当计数变为 0 时，磁盘上的文件数据块才会被真正释放。
#### symlink
    symlink         创建符号链接（软链接）。这是一个特殊的文件，里面存放着指向另一个文件路径的字符串（类似于 Windows 的快捷方式）。

### 文件系统增删改查

#### opendir
    DIR *opendir(const char *name)打开文件夹
        引用:
            #include <sys/types.h>
            nclude <dirent.h>
        参数：name:指定了要打开的文件夹的名字
        返回值:
            错误 NULL errno被设置
            成功 指向文件夹流的地址
#### closedir
    int closedir(DIR *dirp)关闭一个文件夹
        引用：
            #include <sys/types.h>
            #include <dirent.h>
        参数:dirp:指定要关闭的文件夹流
        返回值:
            成功 0
            错误 -1 errno被设置
#### struct dirent
    struct dirent {
        ino_t		d_ino; 		/* inode number */
        off_t		d_off; 		/* not an offset; see NOTES */
        unsigned short 	d_reclen; 	/* length of this record */
        unsigned char 	d_type; 	/* type of file; not supported by all filesystem types */
        char		d_name[256];	/* filename */
    };
#### readdir
    struct dirent *readdir(DIR *dirp)读取文件夹里的一个条目
        引用：
            #include <dirent.h>
        参数:
            dirp:指定了文件夹流,从这个文件夹流中获取数据
        返回值:
            成功 返回一个地址
            失败 函数调用失败NULL errno被设置
                到达文件的末尾NULL errno不被设置
#### mkdir
    mkdir           创建一个空目录。

#### rmdir 
    rmdir           删除一个空目录（目录下不能有任何文件或子目录）。
#### rename 
    rename          重命名或移动文件/目录。本质上是在目录树中修改目录项的路径，可跨越不同目录。
#### remove 
    remove          通用删除。根据参数类型自动选择操作：如果是文件则调用 unlink，如果是空目录则调用 rmdir。


## 其他文件相关

### getpwuid
    struct passwd {  //用户信息结构体
        char 	*pw_name;	/* username */		用户名，方便记忆
        char 	*pw_passwd;	/* user password */	密码
        uid_t	pw_uid;	/* user ID */		用户UID，系统通过UID来识别不同的用户和分配用户权限 0：超级用户 1~499系统用户(伪用户) 500~65535普通用户
        gid_t	pw_gid;		/* group ID */		组GID	每个用户创建时被同时默认创建相同名的组叫做初始组 ，后来加入的组称为附加组
        char	*pw_gecos;	/* user information */  用户说明，可不写
        char	*pw_dir;	/* home directory */    用户家目录路径
        char	*pw_shell;	/* shell program */	登录后第一个程序
    };
    struct passwd *getpwuid(uid t uid)	获取/etc/passwd文件中的一项
        引用：
            #include <sys/types.h>
            #include <pwd.h>
        参数 : uid 指定用户的uid，找到匹配uid的用户的信息
        返回值:
            成功 返回一个具体的地址，指向struct passwd结构体的地址;如果返回NULL errno没有被设置，代表没有找到匹配的条目。
            失败 NULL 将errno的值设置为相应的错误码

        命令 
            /etc/passwd  保存用户信息   与passwd结构体对应 不同的地方：x表示有密码
            /etc/shadow 保存真正的密码
### getgrgid
    struct group {
        char	*gr_name;		/* group name */	组名
        char	*gr_passwd;		/* group_password*/ 	用户组加密后的口令，一般为空
        gid_t 	gr_gid;			/* group ID */		组标识号 系统内部用来标识组
        char 	**gr_mem;		/* group members */	组内用户列表
    };
    struct group *getgrgid(gid_t gid)获取/etc/group文件中的一项
        引用：
            #include <sys/types.h>
            #include <grp.h>
        参数 : gid 指定用户组的gid，找到匹配gid的用户组信息
        返回值: 
            成功 返回一个具体的地址，指向struct group结构体的地址;如果返回NULL	errno没有没设置，代表没有找到相匹配的项目。
            失败 NULL 将errno的值设置为相应的错误码

        命令    /ect/group 保存用户组信息

### basename 

### dirname 
	dirname         它们不涉及任何系统调用，不访问磁盘，只是对字符串进行“切分”。在实际开发中，它们属于 “路径字符串处理” 工具



# 网络编程
## 数据结构ip地址

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


## socket

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

## bind

    int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    将套接字绑定到指定的地址

    参数
        sockfd - 套接字描述符
        addr - 具体的地址
        addrlen - 地址的长度
    返回值
        成功 - 0
        失败 - -1 errno被设置为相应的错误值

## listen

    int listen(int sockfd, int backlog);
    监听套接字

    参数
        sockfd - 套接字描述符
        backlog - 指定未决连接的最大数 客户端已经成功连接服务器，但是服务器还没有接收的连接称为未决连接
    返回值
        成功 - 0
        失败 - -1 errno被设置为相应的错误值

## accept

    int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
    未决队列中接收一个连接 自动创建一个套接字用于通讯并返回该套接字

    参数
        sockfd - 套接字描述符
        addr - 客户端的地址
        addrlen - 地址的长度
    返回值
        成功 - 返回新的套接字描述符
        失败 - -1 errno被设置为相应的错误值

## connect

    int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    使用套接字向服务器发起连接

    参数
        sockfd - 套接字描述符
        addr - 服务器的地址
        addrlen - 地址的长度
    返回值
        成功 - 0
        失败 - -1 errno被设置为相应的错误值

## recvfrom

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

## sendto

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
## 五种IO模型

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