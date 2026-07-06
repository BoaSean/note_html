
# cdev 字符设备
## 文件操作
### 数据结构file_operations

```C
struct file_operations {
    struct module *owner;
    loff_t (*llseek) (struct file *, loff_t, int);				            //修改一个文件的当前的读写位置，并将新位置返回
    ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);		//read
    ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);//write
    ssize_t (*read_iter) (struct kiocb *, struct iov_iter *);
    ssize_t (*write_iter) (struct kiocb *, struct iov_iter *);
    int (*iterate) (struct file *, struct dir_context *);
    unsigned int (*poll) (struct file *, struct poll_table_struct *);		//用于查询设备是否可以进行非阻塞读写
    long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);	//ioctl
    long (*compat_ioctl) (struct file *, unsigned int, unsigned long);
    int (*mmap) (struct file *, struct vm_area_struct *);			        //将设备内存映射到进程的虚拟地址空间中
    int (*open) (struct inode *, struct file *);				            //open
    int (*flush) (struct file *, fl_owner_t id);
    int (*release) (struct inode *, struct file *);				            //close
    int (*fsync) (struct file *, loff_t, loff_t, int datasync);
    int (*fasync) (int, struct file *, int);
    int (*lock) (struct file *, int, struct file_lock *);
    ssize_t (*sendpage) (struct file *, struct page *, int, size_t, loff_t *, int);
    unsigned long (*get_unmapped_area)(struct file *, unsigned long, unsigned long, unsigned long, unsigned long);
    int (*check_flags)(int);
    int (*flock) (struct file *, int, struct file_lock *);
    ssize_t (*splice_write)(struct pipe_inode_info *, struct file *, loff_t *, size_t, unsigned int);
    ssize_t (*splice_read)(struct file *, loff_t *, struct pipe_inode_info *, size_t, unsigned int);
    int (*setlease)(struct file *, long, struct file_lock **, void **);
    long (*fallocate)(struct file *file, int mode, loff_t offset,loff_t len);
    void (*show_fdinfo)(struct seq_file *m, struct file *f);
    int (*copy_file_range)(struct file *, loff_t , struct file *,loff_t, size_t, unsigned int);
    int (*clone_file_range)(struct file *, loff_t, struct file *,loff_t, u64);
    int (*dedupe_file_range)(struct file *, u64, u64, u64 *);
};

```

### (*open)

### (*release)

### (*read)

### (*write)

### (*unlocked_ioctl) 

    long (*unlocked_ioctl) (struct file *file, unsigned int cmd, unsigned long arg);
    功能：ioctl

    注意：
        read write 读取大数据的时候效率高。 ioctl 读取大数据的时候效率不高
    参数：
        file - 文件结构体
        cmd - 命令 对应的应用层的请求码request
        arg - 参数 应用层发来的数据（一般会使用地址）

### ioctl命令辅助宏

    //合成命令的宏定义
    _IO(type,nr) 
    _IOR(type,nr,size) 
    _IOW(type,nr,size) 
    _IOWR(type,nr,size) 
    //分解命令的宏定义
    _IOC_DIR(nr) 
    _IOC_TYPE(nr) 
    _IOC_NR(nr) 
    _IOC_SIZE(nr) 
                        
    功能：ioctl命令辅助宏

    参数：
        cmd 被划分为四个分区，区分命令、数据、数据的传输方向
        nr - 0-7 命令的编号，范围是 0-255. 第一个分区和第二个分区主要作用是用来区分命令的。
        type - 8-15 命令的幻数。 第一个分区和第二个分区主要作用是用来区分命令的。
        size - 16-23 数据的大小
        dir - 24-31 数据传输方向

## 上通下达

### copy_from_user

    unsigned long copy_from_user(void *to, const void __user *from, unsigned long n);
    功能：从用户空间复制数据到内核空间

    参数：
        to - 目标地址 内核中的目标空间的地址
        from - 源地址 用户空间数据的地址
        n - 拷贝的字节数
    返回值：
        0 - 拷贝成功
        负数 - 返回没有拷贝的字节数


### copy_to_user

    unsigned long copy_to_user(void __user *to, const void *from, unsigned long n);
    功能：从内核空间复制数据到用户空间

    参数：
        to - 目标地址 用户空间的目标空间的地址
        from - 源地址 内核空间的源数据的地址
        n - 拷贝的字节数
    返回值：
        0 - 拷贝成功
        负数 - 返回没有拷贝的字节数

### ioremap

    void* ioremap(phys_addr_t paddr, unsigned long size);
    功能：将硬件寄存器地址映射到内核空间

    注意：
        如果成功，就可以通过操作映射后的地址的这个内存，就相当操作硬件的寄存器
    参数：
        paddr - 物理地址
        size - 映射的大小
    返回值：
        成功返回映射后的地址
        失败返回NULL

### iounmap

    void iounmap(const volatile void __iomem *addr);
    功能：取消映射

    参数：
        addr - 映射后的地址


## 驱动模块传参

### module_param

    module_param(name, type, perm);
    功能：传递普通的参数

    参数：
        name - 要传递进去参数的名称
        type - 要传递进去参数的类型
        perm - 要传递进去参数的读写权限
            #define S_IRUSR 00400 - 文件所有者可读
            #define S_IWUSR 00200 - 文件所有者可写
            #define S_IXUSR 00100 - 文件所有者可执行
            #define S_IRGRP 00040 - 文件所在组可读
            #define S_IWGRP 00020 - 文件所在组可写
            #define S_IXGRP 00010 - 文件所在组可执行
            #define S_IROTH 00004 - 与文件所有者不同组的用户可读
            #define S_IWOTH 00002 - 与文件所有者不同组的用户可写
            #define S_IXOTH 00001 - 与文件所有者不同组的用户可执行

### module_param_array

    module_param_array(name, type, *count, perm);
    功能：传递数组

    参数：
        name - 要传递进去参数的名称
        type - 要传递进去参数的类型
        count - 要传递进去参数的个数
        perm - 要传递进去参数的读写权限


## 设备号申请

### 数据结构dev_t

```C
    typedef __u32 __kernel_dev_t;
    typedef __kernel_dev_t dev_t;           //dev_t  32位
```

### dev_t辅助宏

```C
    #define 	MINORBITS	20 						                    //次设备号的位数，一共是 20 位
    #define 	MINORMASK 	((1U << MINORBITS) - 1) 			        //次设备号的掩码
    #define 	MAJOR(dev) 	((unsigned int) ((dev) >> MINORBITS)) 		//在 dev_t 里面获取我们的主设备号
    #define 	MINOR(dev) 	((unsigned int) ((dev) & MINORMASK)) 		//在 dev_t 里面获取我们的次设备号
    #define 	MKDEV(ma,mi) 	(((ma) << MINORBITS) | (mi)) 			//将我们的主设备号ma和次设备号mi组成一个 dev_t 类型
```

### register_chrdev_region

    int register_chrdev_region(dev_t *dev, unsigned count,const char *name);
    功能：静态注册设备号

    参数：
        dev - 申请的设备号的起始值。类型是 dev_t 类型
        count - 要申请的次设备号的个数。
        name - 设备名称
    返回值：
        成功返回0 失败返回-1

### alloc_chrdev_region

    int alloc_chrdev_region(dev_t *dev, unsigned baseminor, unsigned count, const char *name);
    功能：动态注册设备号

    注意：
        使用动态分配会优先使用 255 到 234
        申请一段连续的多个设备号
        设备号的主设备号一样，但是次设备号不同，次设备号以 baseminor 为起始地址地址开始递增。一般 baseminor 为 0,也就是说次设备号从 0 开始。
    参数：
        dev - 保存申请到的设备号
        baseminor - 起始次设备号
        count - 要申请的次设备号的个数。
        name - 设备名称
    返回值：
        成功返回0 失败返回-1

### unregister_chrdev_region

    void unregister_chrdev_region(dev_t from, unsigned count);
    功能：释放设备号

    参数：
        from - 要注销的设备号的起始值
        count - 表示从 from 开始，要释放的设备号个数

## 设备节点

### 数据结构class

    struct class

### class_create

    struct class *class_create(struct module *owner, const char *name);
        #define class_create(owner, name) \              
            ({ \
            static struct lock_class_key __key; \
            __class_create(owner, name, &__key); \
            }) 
    功能：创建一个类

    注意：
        内核中创建一个设备类，这个类会在/sys/class下显示，创建一个设备类可以更好地对设备进行管理
    参数：
        owner - 模块的拥有者
        name - 类名
    返回值：
        成功返回类指针
        失败返回NULL

### class_destroy

    void class_destroy(struct class *cls);
    功能：销毁一个类

    参数：
        cls - 类指针


### 数据结构device

    struct device {
        struct kobject      kobj;            //内核设备模型的顶层抽象类。
        struct device       *parent;        //设备的父节点设备是哪个？

        struct device_private   *p;         //私有数据指针。

        const char      *init_name;         /* initial name of the device */  //设备的名称。
        const struct device_type *type;     //设备的类型

        struct bus_type *bus;               /* type of bus device is on */ //设备所在的总线的类型。
        struct device_driver *driver;       /* which driver has allocated this //与驱动模块匹配的对象。 device */
        void   *platform_data;              /* Platform specific data, device //平台核心数据，不要碰。core doesn't touch it */
    ...
        struct list_head    msi_list;       //设备模型管理使用链表。
        struct class       *class;          //设备所从属的设备类。
    ...
        dev_t           devt;               /* dev_t, creates the sysfs "dev" *///设备号

    };

### device_create

    struct device *device_create(struct class *class, struct device *parent, dev_t devt, void *drvdata, const char *fmt, ...);
    功能：建立设备号与设备节点名称之间的关系。提交uevent事件

    参数：
        class - 设备类 设备要创建哪个类下面
        parent - 设备父节点 一般为 NULL，也就是没有父设备
        devt - 设备号
        drvdata - 驱动数据 设备可能会使用的一些数据，一般为 NULL
        fmt - 设备名称 如果设置 fmt=xxx 的话，就会生成/dev/xxx 这个设备
    返回值：
        成功返回设备指针
        失败返回NULL

### device_destroy

    void device_destroy(struct class *class, dev_t devt);
    功能：销毁一个设备

    参数：
        class - 设备类
        devt - 设备号

## map映射

### register_chrdev

    int register_chrdev(unsigned int major, const char *name, const struct file_operations *fops);
    功能：字符设备映射

    注意：
        在内核中为某个设备号，申请主设备号，关联与此设备进行操作
    参数：
        major - 主设备号
        0 - 系统自动分配一个设备号
        大于0 - 静态指定使用某个主设备号（0-4096）
        name - 设备名称
        fops - 文件操作结构体
    返回值：
        成功返回0 失败返回-1

### unregister_chrdev
    void unregister_chrdev(unsigned int major, const char *name);
    功能：注销映射

    参数：
        major - 主设备号
        name - 设备名称

## cdev

### 数据结构cdev

    struct cdev {
        struct kobject kobj;                //用来支持设备模型，每个内核对象（设备对象，驱动对象）都是kobj
        struct module *owner;               //指向模块的指针，一般使用THIS_MODULE指针即可。
        const struct file_operations *ops;  //字符设备向上提供的回调函数的接口。
        struct list_head list;              //内核的对象的管理链理。
        dev_t dev;                          //字符设备的设备号。
        unsigned int count;                 //设备的个数。
    } __randomize_layout;

### cdev_alloc

    struct cdev *cdev_alloc(void);
    功能：分配cdev结构体 在内核中动态申请一块内存（kmalloc）

    返回值：
        成功返回cdev结构体指针
        失败返回NULL

### kfree

    void kfree(const void *ptr);
    功能：释放内存

    参数：
        ptr - 要释放的内存指针

### cdev_init

    void cdev_init(struct cdev *cdev, const struct file_operations *fops);
    功能：初始化cdev结构体

    参数：
        cdev - 设备结构体
        fops - 文件操作结构体

### cdev_add

    int cdev_add(struct cdev *cdev, dev_t dev, unsigned count);
    功能：添加cdev结构体

    参数：
        cdev - 设备结构体
        dev - 设备号
        count - 设备个数

### cdev_del

    void cdev_del(struct cdev *cdev);
    功能：删除cdev结构体

    参数：
        cdev - 设备结构体

## misc

### 数据结构miscdevice

    struct miscdevice {
        int minor;                                              //次设备号 需要用户设置
                // #define PSMOUSE_MINOR 1
                // #define MS_BUSMOUSE_MINOR 2  
                // #define ATIXL_BUSMOUSE_MINOR 3 /* unused */
                // #define AMIGAMOUSE_MINOR 4 /*FIXME OBSOLETE */
                // #define ATARIMOUSE_MINOR 5 /* unused */
                // #define SUN_MOUSE_MINOR 6 /* unused */
                // ...... 
                // #define MISC_DYNAMIC_MINOR 255
        const char *name;                                       //设备节点的名字.当设备注册成功后，会在/dev 目录下自动生成一个名为 name 的设备文件
        const struct file_operations *fops;                     //文件操作集
        struct list_head list;
        struct device *parent;
        struct device *this_device;
        const struct attribute_group **groups;
        const char *nodename;
        umode_t mode;
    };

### misc_register

    int misc_register(struct miscdevice *misc);
    
    向系统中注册一个 misc设备

### misc_deregister

    void misc_deregister(struct miscdevice *misc);
    
    注销misc设备

# IO 模型
## 5种IO模型
### 5种IO模型概述
    阻塞IO Blocking I/O
    非阻塞IO Non-blocking I/O
    IO多路复用 I/O Multiplexing
    信号驱动IO Signal-driven I/O
    异步IO Asynchronous I/O

## wait_queue 等待队列

### 数据结构wait_queue_head_t

    struct __wait_queue_head {
        spinlock_t lock;                //自旋锁
        struct list_head task_list;     //链表头
    };
    typedef struct __wait_queue_head wait_queue_head_t;

### init_waitqueue_head

    void init_waitqueue_head(wait_queue_head_t *q);
    功能：动态初始化等待队列头结构

    参数：
        q - 等待队列头

### DECLARE_WAIT_QUEUE_HEAD

    DECLARE_WAIT_QUEUE_HEAD(name);
    功能：一次性完成等待队列头的定义和初始化

    参数：
        name - 等待队列头名称

### wait_event

    void wait_event(wait_queue_head_t *wq_head, condition);
        #define wait_event(wq, condition)
        do{
            if (condition)
            break;
                __wait_event(wq, condition);
        } while (0)
                        
    功能：等待condition满足，否则阻塞

    参数：
        wq_head - 等待队列头
        condition - 条件

### wait_event_timeout

    long wait_event_timeout(wait_queue_head_t *wq_head, condition, long timeout);
    功能：等待condition满足，或者超时

    参数：
        wq_head - 等待队列头
        condition - 条件
        timeout - 超时时间

### wait_event_interruptible

    long wait_event_interruptible(wait_queue_head_t *wq_head, condition);
    功能：等待condition满足，可中断

### wait_event_interruptible_timeout

    long wait_event_interruptible(wait_queue_head_t *wq_head, condition);
    功能：等待condition满足，可中断

### 数据结构wait_queue_t

    struct __wait_queue {
        unsigned int flags;
        void *private;
        wait_queue_func_t func;
        struct list_head task_list;
    };
    typedef struct __wait_queue wait_queue_t;

    功能：wait_queue_t 表示等待队列项

### DECLARE_WAITQUEUE

    DECLARE_WAITQUEUE(name, tsk);
    功能：定义并初始化一个等待队列项

    参数：
        name - 等待队列项名称
        tsk - 进程描述符

### add_wait_queue
    void add_wait_queue(wait_queue_head_t *head, wait_queue_t *wait);
    功能：将进程添加到等待队列中

    参数：
        head - 等待队列头
        wait - 等待队列项

### remove_wait_queue
    void remove_wait_queue(wait_queue_head_t *head, wait_queue_t *wait);
    功能：将进程从等待队列中移除

    参数：
        head - 等待队列头
        wait - 等待队列项

### wake_up
    void wake_up(wait_queue_head_t *head);
    功能：唤醒等待队列中的进程

### wake_up_interruptible

    void wake_up_interruptible(wait_queue_head_t *head);
    功能：唤醒可中断的休眠进程

    注意：
        唤醒 TASK_INTERRUPTIBLE 状态的进程，不会影响 TASK_UNINTERRUPTIBLE 进程


## poll 轮询

### poll_wait

    void poll_wait(struct file *filp, wait_queue_head_t *wait_queue, poll_table *wait);
    功能：将进程添加到等待队列中

    注意：
        poll_wait 结合 poll/select/epoll 机制等待事件
        poll_wait 本身 不会阻塞进程，只是 告诉内核进程在等待某个事件
        它的 作用是注册等待队列，当设备状态变化时，内核会唤醒等待进程
    参数：
        filp - 文件描述符
        wait_queue - 等待队列头
        wait - 等待队列


## fasync 异步队列

### 数据结构fasync_struct

    struct fasync_struct

### fasync_helper

    int fasync_helper(int fd, struct file *filp, int on, struct fasync_struct **fapp);
    把当前异步标记的fd及所在进程信息放入到异步队列中

### kill_fasync

    void kill_fasync(struct fasync_struct **fapp, int sig, int band);
    遍历异步队列并向相应的进程发出信号以唤醒

 
# sync 同步机制
## sync 同步机制概述
### sync 同步机制概述1

    中断屏蔽
    自旋锁 (未获取锁的进程处于自旋状态是要消耗cpu资源的 针对多核设计)
    信号量 (获取不到信号量时进程进入休眠，不消耗CPU资源)
    互斥体 (获取不到互斥体时进程进入休眠，不消耗CPU资源，比信号量更轻量)
    原子操作 (不会被中断打断的操作，保证数据一致性)

## 中断屏蔽

### local_irq_disable

    local_irq_disable();关中断宏

### local_irq_enable

    local_irq_enable();开中断宏

## 自旋锁 


### 数据结构 spinlock_t

    spinlock_t lock;
    功能：定义一个自旋锁对象

### spin_lock_init

    spin_lock_init(&lock);
    功能：初始化自旋锁的宏。

    参数：
        lock - 自旋锁对象的指针

### spin_lock

    void spin_lock(spinlock_t *lock);
    功能：获取自旋锁（上锁）。

    参数：
        lock - 自旋锁对象的指针

### spin_unlock

    void spin_unlock(spinlock_t *lock);
    功能：释放自旋锁（解锁）。

    参数：
        lock - 自旋锁对象的指针

## 信号量 

### 数据结构struct semaphore

    struct semaphore sem;
    功能：定义一个信号量对象。

    注意：
        使用前必须先初始化
        通常定义为全局变量或结构体成员
        可以用于进程间同步
    示例：
        // 全局定义
        static struct semaphore my_sem;

        // 结构体成员
        struct my_device {
            struct semaphore sem;
            // 其他成员
        };

### sema_init

    void sema_init(struct semaphore *sem, int val);
    功能：初始化信号量。

    注意：
        val为1时信号量具有互斥效果
        val大于1时可以用于资源计数
        必须在使用信号量之前调用
    参数：
        sem - 信号量对象的指针
        val - 信号量的初始值
    示例：
        struct semaphore my_sem;
        // 初始化为互斥信号量
        sema_init(&my_sem, 1);

### down

    void down(struct semaphore *sem);
    功能：获取信号量（阻塞版本）。

    注意：
        如果信号量不可用，调用进程会进入休眠
        可以在获取信号量时休眠
        不能在中断上下文中使用
        必须与up配对使用
    参数：
        sem - 信号量对象的指针
    示例：
        // 获取信号量（会阻塞）
        down(&my_sem);
        // 临界区代码
        up(&my_sem);

### down_trylock

    int down_trylock(struct semaphore *sem);
    功能：尝试获取信号量（非阻塞版本）。

    注意：
        如果信号量不可用，立即返回而不休眠
        可以在不允许休眠的上下文中使用
        成功获取时必须调用up释放
    参数：
        sem - 信号量对象的指针
    返回值：
        0 - 成功获取信号量
        非0 - 获取失败
    示例：
        // 尝试获取信号量（不会阻塞）
        if (down_trylock(&my_sem) == 0) {
            // 成功获取信号量
            // 临界区代码
            up(&my_sem);
        } else {
            // 获取失败，执行其他操作
            printk("无法获取信号量\n");
        }

### up

    void up(struct semaphore *sem);
    功能：释放信号量。

    注意：
        必须与down或down_trylock配对使用
        会唤醒等待该信号量的进程
        可以在中断上下文中使用
    参数：
        sem - 信号量对象的指针
    示例：
        // 释放信号量
        up(&my_sem);

## 互斥体
### 数据结构struct mutex

    struct mutex mtx;
    功能：定义一个互斥体对象。

    注意：
        使用前必须先初始化
        通常定义为全局变量或结构体成员
        互斥体比信号量更轻量级，适用于简单的互斥场景
        同一时刻只能被一个任务持有
    示例：
        // 全局定义
        static struct mutex my_mutex;

        // 结构体成员
        struct my_device {
            struct mutex mtx;
            // 其他成员
        };

### mutex_init

    void mutex_init(struct mutex *mtx);
    功能：初始化互斥体。

    注意：
        必须在使用互斥体之前调用
        初始化后互斥体处于未锁定状态
        不能重复初始化已经初始化的互斥体
    参数：
        mtx - 互斥体对象的指针
    示例：
        struct mutex my_mutex;
        // 初始化互斥体
        mutex_init(&my_mutex);

### mutex_lock

    void mutex_lock(struct mutex *mtx);
    功能：获取互斥体（阻塞版本）。

    注意：
        如果互斥体已被占用，调用进程会进入休眠
        不能在中断上下文中使用
        不能在原子上下文中使用
        必须与mutex_unlock配对使用
        同一个进程不能重复获取同一个互斥体
    参数：
        mtx - 互斥体对象的指针
    示例：
        // 获取互斥体（会阻塞）
        mutex_lock(&my_mutex);
        // 临界区代码
        mutex_unlock(&my_mutex);

### mutex_trylock

    int mutex_trylock(struct mutex *mtx);
    功能：尝试获取互斥体（非阻塞版本）。

    注意：
        如果互斥体已被占用，立即返回而不休眠
        可以在不允许休眠的上下文中使用
        成功获取时必须调用mutex_unlock释放
    参数：
        mtx - 互斥体对象的指针
    返回值：
        1 - 成功获取互斥体
        0 - 获取失败
    示例：
        // 尝试获取互斥体（不会阻塞）
        if (mutex_trylock(&my_mutex)) {
            // 成功获取互斥体
            // 临界区代码
            mutex_unlock(&my_mutex);
        } else {
            // 获取失败，执行其他操作
            printk("无法获取互斥体\n");
        }

### mutex_unlock

    void mutex_unlock(struct mutex *mtx);
    功能：释放互斥体。

    注意：
        必须与mutex_lock或mutex_trylock配对使用
        只能由持有互斥体的进程释放
        会唤醒等待该互斥体的进程
        不能重复释放未被锁定的互斥体
    参数：
        mtx - 互斥体对象的指针
    示例：
        // 释放互斥体
        mutex_unlock(&my_mutex);

## 原子操作
### 数据结构atomic_t

    atomic_t atm;
    功能：定义一个原子变量。

    注意：
        使用前必须初始化
        可以通过atomic_set或ATOMIC_INIT初始化
        原子操作保证在多处理器系统上的同步
    示例：
        // 先定义，再初始化
        atomic_t atm;
        atomic_set(&atm, 1);

        // 定义并初始化
        atomic_t atm = ATOMIC_INIT(1);

### ATOMIC_INIT

    atomic_t atm = ATOMIC_INIT(1);
    功能：定义并初始化原子变量的宏。

    注意：
        只能在变量定义时使用
        不能用于已经定义的变量
        参数必须是编译时常量
    参数：
        i - 原子变量的初始值

### atomic_read

    int atomic_read(const atomic_t *v);
    功能：原子读取变量的值。

    注意：
        保证读取操作的原子性
        不会被其他CPU的并发操作干扰
    参数：
        v - 原子变量的指针
    返回值：
        返回原子变量的当前值
    示例：
        int val = atomic_read(&atm);

### atomic_set

    void atomic_set(atomic_t *v, int i);
    功能：原子设置变量的值。

    注意：
        保证设置操作的原子性
        可以用于初始化或重置原子变量
    参数：
        v - 原子变量的指针
        i - 要设置的值
    示例：
        atomic_set(&atm, 100);

### atomic_inc

    void atomic_inc(atomic_t *v);
    功能：原子递增操作。

    注意：
        将原子变量的值加1
        操作是原子的，不会被中断
        常用于引用计数
    参数：
        v - 原子变量的指针
    示例：
        atomic_inc(&atm);  // atm = atm + 1

### atomic_dec

    void atomic_dec(atomic_t *v);
    功能：原子递减操作。

    注意：
        将原子变量的值减1
        操作是原子的，不会被中断
        常用于引用计数
    参数：
        v - 原子变量的指针
    示例：
        atomic_dec(&atm);  // atm = atm - 1

### atomic_dec_and_test

    int atomic_dec_and_test(atomic_t *v);
    功能：原子递减并测试是否为零。

    注意：
        将原子变量的值减1并测试结果
        整个操作是原子的
        常用于引用计数的释放检查
    参数：
        v - 原子变量的指针
    返回值：
        1 - 递减后的值为0
        0 - 递减后的值不为0
    示例：
        if (atomic_dec_and_test(&atm)) {
            // 引用计数变为0，执行清理操作
            cleanup_resource();
        }

### atomic_add

    void atomic_add(int i, atomic_t *v);
    功能：原子加法操作。

    注意：
        将原子变量的值加上指定的数
        操作是原子的，不会被中断
    参数：
        i - 要加的值
        v - 原子变量的指针
    示例：
        atomic_add(10, &atm);  // atm = atm + 10

### atomic_sub

    void atomic_sub(int i, atomic_t *v);
    功能：原子减法操作。

    注意：
        将原子变量的值减去指定的数
        操作是原子的，不会被中断
    参数：
        i - 要减的值
        v - 原子变量的指针
    示例：
        atomic_sub(10, &atm);  // atm = atm - 10

# platform
## platform设备和驱动
### 数据结构struct platform_device

    struct platform_device {                //-描述设备的结构体
        const char *name;						    //device名字，可以用来和driver匹配
        int id;								        //ID是device名字相同时的另一区分标志
        bool id_auto;
        struct device dev;						    //内置的 device 结构体
        u32 num_resources;						    //资源结构体数量
        struct resource *resource;					//资源结构体数组指针  //--描述设备使用资源的结构体

        const struct platform_device_id *id_entry;	//用来进行与设备驱动匹配用的 id_table
        char *driver_override;                      /* Driver name to force a match */
        
        struct mfd_cell *mfd_cell;                  /* MFD cell pointer */
        
        struct pdev_archdata archdata;				/* arch specific additions *///私有数据
    };

    struct resource {      //--描述设备使用资源的结构体
        resource_size_t start;						//资源的起始信息
        resource_size_t end;						//资源的终止信息
        const char *name;						    //资源名字
        unsigned long flags;						//资源类型
        struct resource *parent, *sibling, *child;			
    };

### platform_device_register

    int platform_device_register(struct platform_device *pdev);
    功能：加载platform_device对象到平台总线上

### platform_device_unregister

    void platform_device_unregister(struct platform_device *pdev);
    功能：把platform_device从总线上卸载

### 数据结构struct platform_driver

    struct platform_driver {        //-描述驱动的结构体
        int (*probe)(struct platform_device *);				//当 driver 和 device 匹配成功的时候，就会执行 probe 函数
        int (*remove)(struct platform_device *);			//当 driver 和 device 任意一个 remove 的时候，就会执行这个函数
        void (*shutdown)(struct platform_device *);			//当设备收到 shutdown 命令的时候，就会执行这个函数
        int (*suspend)(struct platform_device *, pm_message_t state);	//当设备收到 suspend 命令的时候，就会执行这个函数
        int (*resume)(struct platform_device *);			//当设备收到 resume 命令的时候，就会执行这个函数
        struct device_driver driver;					    //--内置的device_driver 结构体
        const struct platform_device_id *id_table;			//id_table匹配表
        bool prevent_deferred_probe;                        //是否延时探测
    };

    struct device_driver {
        const char *name;                                   //驱动名称
        struct bus_type *bus;
        
        struct module *owner;
        const char *mod_name; 
        
        bool suppress_bind_attrs; 
        
        const struct of_device_id *of_match_table;			//---采用设备树的时候驱动使用的匹配表
        const struct acpi_device_id *acpi_match_table;
        
        int (*probe) (struct device *dev);
        int (*remove) (struct device *dev);
        void (*shutdown) (struct device *dev);
        int (*suspend) (struct device *dev, pm_message_t state);
        int (*resume) (struct device *dev);
        const struct attribute_group **groups;
        
        const struct dev_pm_ops *pm;
        
        struct driver_private *p;                           //私有数据，主要用于传参。
    };

    struct of_device_id {
        char name[32];
        char type[32];
        char compatible[128];					//compatible 成员，通过设备节点的 compatible 和 of_match_table中每个项目的 compatible 成员变量进行匹配
        const void *data;
    };

    struct platform_device_id {
        char name[PLATFORM_NAME_SIZE];
        kernel_ulong_t driver_data;
    };

#### platform_driver_register

    int platform_driver_register(struct platform_driver *drv);
    功能：注册驱动到platform总线上，并自动匹配platform_device或设备树

#### platform_driver_unregister

    void platform_driver_unregister(struct platform_driver *drv);
    功能：从platform上卸载驱动


### platform驱动资源获取


### probe形参

    int (*probe)(struct platform_device *pdev);
    功能：通过回调的probe函数的形参获取设备资源

### platform_get_resource

    struct resource *platform_get_resource(struct platform_device *dev, unsigned int type, unsigned int num);
    功能：获取设备资源

    参数：
        dev - 设备结构体
        type - 资源类型。即设备资源的类型：即那个flags标记类型是内存资源，还是中断资源，还是什么别的资源等。
        num - 资源编号。即同类资源所处位置的索引值（注意是同类资源的索引）
    返回值：
        成功返回获取到的资源，失败返回NULL

# DeviceTree
## DeviceTree驱动资源获取

### 数据结构struct device_node
    struct device_node {
        const char *name;//节点名称：
        phandle phandle; //节点引用值，类似于引用记数
        const char *full_name;//全称
        struct fwnode_handle fwnode;

        struct    property *properties;//属性结构体
        struct    property *deadprops;    /* removed properties *///已经被删除了此属性
        struct    device_node *parent;//父节点：
        struct    device_node *child; //子节点：
        struct    device_node *sibling;//兄弟节点
    #if defined(CONFIG_OF_KOBJ)
        struct    kobject kobj;
    #endif
        unsigned long _flags;
        void    *data;
    #if defined(CONFIG_SPARC)
        unsigned int unique_id;
        struct of_irq_controller *irq_trans;
    #endif
    };

    struct property{		//属性结构体
        char *name; 		/* 属性名字 */
        int length; 		/* 属性长度 */
        void *value; 		/* 属性值 */
        struct property *next;	/* 下一个属性 */
        unsigned long _flags;
        unsigned int unique_id;
        struct bin_attribute attr;
    };

### of_find_node_by_path

    struct device_node *of_find_node_by_path(const char *path);
    功能：根据路径获取设备树节点

    参数：
        path - 设备树节点路径
    返回值：
        成功返回设备树节点，失败返回NULL

### of_get_parent

    struct device_node *of_get_parent(const struct device_node *node);
    功能：获取设备树节点的父节点

    参数：
        node - 设备树节点
    返回值：
        成功返回设备树节点，失败返回NULL

### of_get_next_child

    struct device_node *of_get_next_child(const struct device_node *node, struct device_node *prev);
    功能：获取设备树节点的子节点

    参数：
        node - 设备树节点
        prev - 前一个子节点
    返回值：
        成功返回设备树节点，失败返回NULL

### of_find_property

    struct property *of_find_property(const struct device_node *np, const char *name, int *lenp);
    功能：获取设备树节点的属性

    参数：
        np - 设备树节点
        name - 属性名称
        lenp - 属性长度
    返回值：
        成功返回设备树节点属性，失败返回NULL

### of_iomap

    void __iomem *of_iomap(struct device_node *node, int index);
    功能：将设备树节点中的内存区域映射到内核空间 以前我们会通过 ioremap 函数来完成物理地址到虚拟地址的映射

    参数：
        node - 设备树节点
        index - reg 属性中要完成内存映射的段，如果 reg 属性只有一段的话 index 就设置 0
    返回值：
        成功返回映射的内存区域，失败返回NULL

### of_property_read_u8

    int of_property_read_u8(const struct device_node *np, const char *propname, u8 *val);
    功能：读取u8类型的属性

    参数：
        np - 设备树节点
        propname - 属性名称
        val - 属性值
    返回值：
        成功返回0，失败返回-EINVAL

### of_property_read_u16_array

    int of_property_read_u16_array(const struct device_node *np, const char *propname, u16 *val, size_t sz);
    功能：读取u16类型的属性

    参数：
        np - 设备树节点
        propname - 属性名称
        val - 属性值
        sz - 属性值数量
    返回值：
        成功返回0，失败返回-EINVAL

### of_property_read_u32_array

    int of_property_read_u32_array(const struct device_node *np, const char *propname, u32 *val, size_t sz);
    功能：读取u32类型的属性

    参数：
        np - 设备树节点
        propname - 属性名称
        val - 属性值
        sz - 属性值数量
    返回值：
        成功返回0，失败返回-EINVAL

### of_property_read_u64_array

    int of_property_read_u64_array(const struct device_node *np, const char *propname, u64 *val, size_t sz);
    功能：读取u64类型的属性

    参数：
        np - 设备树节点
        propname - 属性名称
        val - 属性值
        sz - 属性值数量
    返回值：
        成功返回0，失败返回-EINVAL

### of_property_read_string

    int of_property_read_string(const struct device_node *np, const char *propname, const char **str);
    功能：读取字符串类型的属性

    参数：
        np - 设备树节点
        propname - 属性名称
        str - 属性值
    返回值：
        成功返回0，失败返回-EINVAL

# pinctrl子系统

# GPIO 子系统

## DeviceTree驱动获取gpio

### of_get_named_gpio

    int of_get_named_gpio(struct device_node *np, const char *list_name, int index, enum of_gpio_flags *flags);
    功能：获取设备树节点中的GPIO

    参数：
        np - 设备树节点
        list_name - 列表名称
        index - 索引
        flags - 标志
    返回值：
        成功返回GPIO编号，失败返回-EINVAL

## legacy_gpio_api

### gpio_request

    int gpio_request(unsigned gpio, const char *label);
    功能：请求GPIO。申请当前进程使用GPIO号，防止进程竞态出现。

    参数：
        gpio - GPIO编号
        label - 标签
    返回值：
        成功返回0，失败返回-EINVAL

### gpio_direction_input

    int gpio_direction_input(unsigned gpio);
    功能：设置GPIO为输入

    参数：
        gpio - GPIO编号
    返回值：
        成功返回0，失败返回-EINVAL

### gpio_direction_output

    int gpio_direction_output(unsigned gpio, int value);
    功能：设置GPIO为输出

    参数：
        gpio - GPIO编号
        value - 值
    返回值：
        成功返回0，失败返回-EINVAL

### gpio_get_value

    int gpio_get_value(unsigned gpio);
    功能：获取GPIO值

    参数：
        gpio - GPIO编号
    返回值：
        成功返回GPIO值，失败返回-EINVAL

### gpio_set_value

    void gpio_set_value(unsigned gpio, int value);
    功能：设置GPIO值

    参数：
        gpio - GPIO编号
        value - 值
    返回值：
        成功返回0，失败返回-EINVAL

### gpio_free

    void gpio_free(unsigned gpio);
    功能：释放GPIO

    参数：
        gpio - GPIO编号
    返回值：
        成功返回0，失败返回-EINVAL

## descriptor-based_gpio_api

# 中断子系统
## 中断api

### irq_of_parse_and_map

    int irq_of_parse_and_map(struct device_node *node, int index);
    功能：解析设备树节点中的中断信息，并映射为中断号

    参数：
        node - 设备树节点
        index - 中断索引
    返回值：
        成功返回中断号，失败返回-EINVAL

### of_irq_get

    int of_irq_get(struct device_node *dev, int index);
    功能：获取设备树节点中的中断信息

    参数：
        dev - 设备树节点
        index - 中断索引
    返回值：
        成功返回中断号，失败返回-EINVAL

### gpio_to_irq

    int gpio_to_irq(unsigned gpio);
    功能：将GPIO编号转换为中断号

    参数：
        gpio - GPIO编号
    返回值：
        成功返回中断号，失败返回-EINVAL

### request_irq

    int request_irq(unsigned int irq, irq_handler_t handler, unsigned long flags, const char *name, void *dev);
    功能：请求中断

    参数：
        irq - 中断号
        handler - 中断处理函数
        flags - 标志
            #include <linux/interrupt.h>
            IRQF_SHARED - 多个设备共享一个中断线，共享的所有中断都必须指定此标志。如果使用共享中断的话，`request_irq` 函数的 `dev` 参数就是唯一区分它们的标志。
            IRQF_ONESHOT - 单次中断，中断执行一次就结束。
            IRQF_TRIGGER_NONE - 无触发。
            IRQF_TRIGGER_RISING - 上升沿触发。
            IRQF_TRIGGER_FALLING - 下降沿触发。
            IRQF_TRIGGER_HIGH - 高电平触发。
            IRQF_TRIGGER_LOW - 低电平触发。
        name - 名称
        dev - 设备
    返回值：
        成功返回0，失败返回-EINVAL

### free_irq

    void free_irq(unsigned int irq, void *dev_id);
    功能：释放中断

    参数：
        irq - 中断号
        dev_id - 设备
    返回值：
        成功返回0，失败返回-EINVAL

### enable_irq

    void enable_irq(unsigned int irq);
    功能：使能中断

    参数：
        irq - 中断号
    返回值：
        成功返回0，失败返回-EINVAL

### disable_irq

    void disable_irq(unsigned int irq);
    功能：禁止中断

    参数：
        irq - 中断号
    返回值：
        成功返回0，失败返回-EINVAL

### request_threaded_irq

    int request_threaded_irq(unsigned int irq, irq_handler_t handler, irq_handler_t thread_fn, unsigned long irqflags, const char *name, void *dev);
    功能：请求中断

    参数：
        irq - 中断号
        handler - 中断处理函数 irqreturn_t handler(int irq, void *dev_id);
        thread_fn - 线程处理函数 irqreturn_t thread_fn(int irq, void *dev_id);
        irqflags - 标志
        name - 名称
        dev - 设备
    返回值：
        成功返回0，失败返回-EINVAL

## 内核定时器
### 数据结构jiffies

    unsigned long jiffies;
    功能：系统节拍数 记录自系统启动以来产生的节拍的总数

### jiffies转换api

    unsigned long jiffies_to_msecs(const unsigned long j);将节拍数转换为毫秒
    unsigned long jiffies_to_usecs(const unsigned long j);将节拍数转换为微秒
    unsigned long msecs_to_jiffies(const unsigned int msecs);将毫秒转换为节拍数
    unsigned long usecs_to_jiffies(const unsigned int usecs);将微秒转换为节拍数
### jiffies时间前后判断api

    int time_after(unsigned long a, unsigned long b);判断a是否在b之后
    int time_before(unsigned long a, unsigned long b);判断a是否在b之前
    int time_after_eq(unsigned long a, unsigned long b);判断a是否在b之后或相等
    int time_before_eq(unsigned long a, unsigned long b);判断a是否在b之前或相等
### sleep睡眠api

    unsigned long msleep(unsigned int msecs);睡眠毫秒
    unsigned long usleep(unsigned int usecs);睡眠微秒
    unsigned long nsleep(unsigned int nsecs);睡眠纳秒

### 数据结构timer_list
    struct timer_list {               //内核定时器的结构体对象
        struct hlist_node       entry;                              //内核链表节点
        unsigned long           expires;                            //定时器超时时间。
        void                    (*function)(struct timer_list *);   //内核定时器处理函数
        u32                     flags;                              //一般填写为0;

    #ifdef CONFIG_LOCKDEP
        struct lockdep_map    lockdep_map;
    #endif
    };

### init_timer
    void init_timer(struct timer_list *timer);
    功能：初始化定时器

    参数：
        timer - 定时器
    返回值：
        成功返回0，失败返回-EINVAL
### DEFINE_TIMER
    DEFINE_TIMER(_name, _function, _expires, _data);
    功能：旧版 该宏会静态创建一个名叫 timer_name 内核定时器，并初始化

    参数：
        _name - 名称
        _function - 处理函数
        _expires - 超时时间
        _data - 传递给function的数据
### timer_setup
    void timer_setup(struct timer_list *timer, void (*function)(struct timer_list *), unsigned int flags);
    功能：设置定时器

    参数：
        timer - 定时器
        function - 处理函数
        flags - 标志
### add_timer

    void add_timer(struct timer_list *timer);
    功能：向内核注册并启动定时器

    注意：
        注册以后，定时器就会开始运行 定时器只能启动一次，多次调用会发生崩溃溃
    参数：
        timer - 定时器

### mod_timer

    int mod_timer(struct timer_list *timer, unsigned long expires);
    功能：修改定时器超时时间

    参数：
        timer - 定时器
        expires - 超时时间
    返回值：
        成功返回0，失败返回-EINVAL

### del_timer

    int del_timer(struct timer_list *timer);
    功能：删除定时器

### del_timer_sync

    int del_timer_sync(struct timer_list *timer);
    功能：同步删除定时器

    注意：
        确保定时器在返回之前被完全删除 等待使用完定时器再删除
    参数：
        timer - 定时器
    返回值：
        成功返回0，失败返回-EINVAL

### del_timer_async

    void del_timer_async(struct timer_list *timer);
    功能：异步删除定时器

    注意：
        从定时器队列中移除定时器，不会等待回调函数执行完毕
    参数：
        timer - 定时器
    返回值：
        成功返回0，失败返回-EINVAL

## 中断下文tasklet

### 数据结构tasklet_struct

    struct tasklet_struct                                       //tasklet结构体
    {
            struct tasklet_struct *next;                    //下一个节点的指针
            unsigned long state;                            //tasklet的状态标记
            atomic_t count;                                 //tasklet的引用记数
            bool use_callback;                              //是否使用回调callback;
            union {
                void (*func)(unsigned long data);           //回调func参数data
                void (*callback)(struct tasklet_struct *t); //回调callback参数为tasklet对象指针。
            };
            unsigned long data;                             //向func回调传递的参数
    };

### tasklet_init

    void tasklet_init(struct tasklet_struct *t, void (*func)(unsigned long), unsigned long data);
    功能：旧版本 初始化tasklet

    参数：
        t - tasklet
        func - 处理函数
        data - 传递给func的数据

### tasklet_setup

    void tasklet_setup(struct tasklet_struct *t, void (*func)(unsigned long));
    功能：设置tasklet

    参数：
        t - tasklet
        func - 处理函数

### tasklet_schedule

    void tasklet_schedule(struct tasklet_struct *t);
    功能：执行调用

### tasklet_kill

    void tasklet_kill(struct tasklet_struct *t);
    功能：tasklet对象从tasklet链表中删除


## 中断下文workqueue

### 数据结构work_struct

    #include <linux/workqueue.h>
    struct work_struct {                                                //工作
        /*    atomic_long_t data; */
            unsigned long data;

            struct list_head entry;
            work_func_t func;                                        //回调的队列的处理函数
            //typedef void (*work_func_t)(struct work_struct *work);    //回调函数类型
    #ifdef CONFIG_LOCKDEP
            struct lockdep_map lockdep_map;
    #endif
    };

### INIT_WORK

    INIT_WORK(_work, _func);
    功能：初始化工作（struct work_struct）：定义一个工作结构，并指定其执行的函数

### schedule_work

    bool schedule_work(struct work_struct *work);
    功能：将工作提交到工作队列，以便稍后执行

### cancel_work_sync

    void cancel_work_sync(struct work_struct *work);
    功能：延时卸载——如果卸载模块时，万一有工作队列中任务还没有执行结束，使用此方法，可以等待任务执行结束后再卸载。

### destroy_workqueue

    void destroy_workqueue(struct workqueue_struct *wq);
    功能：消毁当前工作队列——一般会先取消工作，再销毁队列，如果手动申请了指定的工作队列。


## 中断下文threaded_irq


# input子系统

## input子系统api

### 数据结构input_dev

    struct input_dev {
        const char *name;                                                               //设备名称
        const char *phys;                                                               //设备在系统中的物理路径
        const char *uniq;                                                               //设备唯一识别符
        struct input_id id;                                                             //设备ID，包含总线类型(PCI 、 USB)、厂商ID,设备ID与 input handler 匹配的时会用到

        unsigned long evbit[BITS_TO_LONGS(EV_CNT)];                                         //设备支持的事件类型
        unsigned long keybit[BITS_TO_LONGS(KEY_CNT)];                                       //设备支持的具体的按键、按钮事件
        unsigned long relbit[BITS_TO_LONGS(REL_CNT)];                                       //设备支持的具体的相对坐标事件
        unsigned long absbit[BITS_TO_LONGS(ABS_CNT)];                                       //设备支持的具体的绝对坐标事件
        unsigned long mscbit[BITS_TO_LONGS(MSC_CNT)];                                       //设备支持的具体的混杂事件
        unsigned long ledbit[BITS_TO_LONGS(LED_CNT)];                                       //设备支持的具体的LED指示灯事件
        unsigned long sndbit[BITS_TO_LONGS(SND_CNT)];                                       //设备支持的具体的音效事件
        unsigned long ffbit[BITS_TO_LONGS(FF_CNT)];                                         //设备支持的具体的力反馈事件
        unsigned long swbit[BITS_TO_LONGS(SW_CNT)];                                         //设备支持的具体的开关事件

        unsigned int keycodemax;                                                            //键盘码表的大小
        unsigned int keycodesize;                                                           //键盘码表中的元素个数
        void *keycode;                                                                      //设备的键盘码表
        
        int (*setkeycode)(struct input_dev *dev,unsigned int scancode, unsigned int keycode);       //下面两个是可选方法，用于配置和获取键盘码表
        int (*getkeycode)(struct input_dev *dev,unsigned int scancode, unsigned int *keycode);

        struct ff_device *ff;                                                               //如果设备支持力反馈，则该成员将指向力反馈设备描述结构
        unsigned int repeat_key;                                                            //保存上一个键值，用于实现软件自动重复按键（用户按住某个键不放）
        struct timer_list timer;                                                            //用于软件自动重复按键的定时器

        int sync;                                                                           //在上次同步事件(EV_SYNC)发生后没有新事件产生，则被设置为 1 

        int abs[ABS_CNT];                                                                   //用于上报的绝对坐标当前值
        int rep[REP_MAX + 1];                                                               //记录自动重复按键参数的当前值

        unsigned long key[BITS_TO_LONGS(KEY_CNT)];                                          //反映设备按键、 按钮的当前状态
        unsigned long led[BITS_TO_LONGS(LED_CNT)];                                          //反映设备LED指示灯的当前状态
        unsigned long snd[BITS_TO_LONGS(SND_CNT)];                                          //反映设备音效的当前状态
        unsigned long sw[BITS_TO_LONGS(SW_CNT)];                                            //反映设备开关的当前状态

        int absmax[ABS_CNT];                                                                //绝对坐标的最大值
        int absmin[ABS_CNT];                                                                //绝对坐标的最小值
        int absfuzz[ABS_CNT];                                                               //绝对坐标的噪音值，变化小于该值的一半可忽略该事件
        int absflat[ABS_CNT];                                                               //摇杆中心位置大小
        int absres[ABS_CNT];

        int (*open)(struct input_dev *dev);                                                 //提供以下4个设备驱动层的操作接口，根据具体的设备需求实现它们
        void (*close)(struct input_dev *dev);
        int (*flush)(struct input_dev *dev, struct file *file);
        int (*event)(struct input_dev *dev, unsigned int type, unsigned int code, int value);   //用于处理送到设备驱动层来的事件，很多事件在事件处理层被处理，但有的事件仍需送到设备驱动中．如LED指示灯事件和音效事件
        
        struct input_handle *grab;                                                              //指向独占该设备的输入句柄（ input handle ），通常设备驱动上报的事件会被分发到与设备
                                                                                                //关联的所有事件处理程序（ input handler ）中处理，但如果通过ioctl 的EVIOCGRAB命令
                                                                                                //设置了独占句柄，则上报事件只能被所设置的输入句柄对应的事件处理程序处理
        
        spinlock_t event_lock;                                                                  //调用 event （） 时需要使用该自旋锁来实现互斥
        struct mutex mutex;                                                                     //用于串行化的访问 open()、 close()和flush()等设备方法

        //记录输入事件处理程序(input handlers)调用设备open()方法的次数．保证设备open()方法是在
        //第一次调用 input_open_device()中被调用，设备close()方法在最后一次调用 input_close_device()中被调用
        unsigned int users;
        bool going_away;

        struct device dev;                                                                      //内嵌device结构

        struct list_head    h_list;                                                             //与该设备相关的输入句柄列表(struct input handle)
        struct list_head    node;                                                               //挂接到input_dev_list链表上
    };

### input_dev

    struct input_dev *input_allocate_device(void);
    功能：申请 input_dev 结构体

### input_free_device

    void input_free_device(struct input_dev *dev);
    功能：注销 input_dev 结构体

### set_bit

    void set_bit(int nr, volatile unsigned long *addr);
    功能：设置 bit 位

    参数：
        nr - 位数
        addr - 地址
    示例：

        set_bit(EV_KEY, xxx_input_dev->evbit);              //设置什么事件类型
        set_bit(KEY_L,xxx_input_dev->keybit);               //设置那个按键的事件？   

### input_register_device

    int input_register_device(struct input_dev *dev);
    功能：注册 input_dev 结构体

### input_unregister_device

    void input_unregister_device(struct input_dev *dev);
    功能：注销 input_dev 结构体

### input_event

    void input_event(struct input_dev *dev, unsigned int type, unsigned int code, int value);
    功能：上报事件

    参数：
        dev - input_dev 结构体 表示哪个输入设备生成了这个事件
        type - 事件的类型
            EV_KEY 按键事件（如键盘按键、鼠标按钮等）
            EV_REL 相对轴事件（如鼠标移动）
            EV_ABS 绝对轴事件（如触摸屏位置）
            EV_SYN 同步事件，用于标志一组事件的结束
        code - 事件编码 具体描述事件的子类别。对于EV_KEY code 表示具体的按键；对于轴事件EV_REL 和 EV_ABS，code 表示具体的轴（如 REL_X 表示 X 轴移动）
        value - 事件值 表示事件的具体值。对于按键事件，这里通常是 1按下或 0释放；对于轴事件，这里表示移动的距离或位置的具体值。

### input_sync

    void input_sync(struct input_dev *dev);
    功能：同步事件 通知输入子系统已经完成一组事件数据的上报

    参数：
        dev - input_dev 结构体

### 数据结构input_event

    struct input_event{             //app中获取事件的结构体
        struct timeval time//事件发生的时间戳;
        __u16 type;//事件类型
        __u16 code;//事件编码 
        __s32 value;//事件值
    };


# i2c子系统
## i2c设备挂载

### 数据结构i2c_driver
    struct i2c_driver {
        ...
        /* Standard driver model interfaces */
        int (*probe)(struct i2c_client *client, const struct i2c_device_id *id);
        int (*remove)(struct i2c_client *client);
        ...    
        struct device_driver driver;//驱动的父类：父类中有匹配方式 of_match_table;
        ...

    };
    //i2c驱动的父类
    struct device_driver {
        const char        *name; //驱动的名字，用来生成节点
    ...
        const struct of_device_id    *of_match_table;//设备树匹配方式
    ...
        struct driver_private *p;//私有属性指针
    };
### i2c_add_driver

    #define i2c_add_driver(driver) \
        i2c_register_driver(THIS_MODULE, driver)
                    
    功能：i2c_driver对象的注册宏

### i2c_del_driver

    void i2c_del_driver(struct i2c_driver *driver);
    功能：i2c_driver对象的注销宏

### module_i2c_driver

    module_i2c_driver(__i2c_driver)
    功能：一键注册注销宏

## 使用i2c_client传输


### 数据结构i2c_client

    struct i2c_client {
        unsigned short flags;           /* 设备的标志位 */

        unsigned short addr;            /* 设备的 I2C 地址 */


        char name[I2C_NAME_SIZE];       /* 设备的名称 */

        struct i2c_adapter *adapter;    /* 指向 I2C 适配器的指针，表示该设备连接到哪个适配器上 */

        struct device dev;              /* 通用设备结构，用于描述设备的基本信息 */
    ...
    };

### i2c_master_send

    int i2c_master_send(const struct i2c_client *client, const char *buf, int count);
    功能：i2c_client对象的写入宏

    参数：
        client - i2c_client对象
        buf - 数据
        count - 数据长度
    返回值：
        成功返回发送的字节数，失败返回负数

### i2c_master_recv

    int i2c_master_recv(const struct i2c_client *client, char *buf, int count);
    功能：i2c_client对象的读取宏

    参数：
        client - i2c_client对象
        buf - 数据
        count - 数据长度
    返回值：
        成功返回读取的字节数，失败返回负数

## 使用i2c_adapter传输


### 数据结构i2c_adapter
    struct i2c_adapter 
    {
        struct module *owner;// 驱动程序模块的所有者
        unsignedintclass;// 适配器类别
        conststruct i2c_algorithm *algo;// 用于与硬件通信的算法
        void *algo_data;                     // 算法相关数据
        ...
        struct device dev;// 设备结构
        int nr;                              // 适配器号
        char name[48];                       // 适配器名称
        ...
    };
### 数据结构i2c_msg
    struct i2c_msg {
        __u16 addr; /* slave address    从机地址        */
        __u16 flags;//数据中的读写标记为0为写，1为读
                #define I2C_M_RD        0x0001  /* read data, from slave to master */
                                    /* I2C_M_RD is guaranteed to be 0x0001! */
                #define I2C_M_TEN       0x0010  /* this is a ten bit chip address */
                #define I2C_M_DMA_SAFE      0x0200  /* the buffer of this message is DMA safe */
                                    /* makes only sense in kernelspace */
                                    /* userspace buffers are copied anyway */
                #define I2C_M_RECV_LEN      0x0400  /* length will be first received byte */
                #define I2C_M_NO_RD_ACK     0x0800  /* if I2C_FUNC_PROTOCOL_MANGLING */
                #define I2C_M_IGNORE_NAK    0x1000  /* if I2C_FUNC_PROTOCOL_MANGLING */
                #define I2C_M_REV_DIR_ADDR  0x2000  /* if I2C_FUNC_PROTOCOL_MANGLING */
                #define I2C_M_NOSTART       0x4000  /* if I2C_FUNC_NOSTART */
                #define I2C_M_STOP      0x8000  /* if I2C_FUNC_PROTOCOL_MANGLING */
        __u16 len;      /* msg length          消息长度     */
        __u8 *buf;      /* pointer to msg data  消息的首地址        */
    };
### i2c_transfer

    int i2c_transfer(struct i2c_adapter *adap, struct i2c_msg *msgs, int num);
    功能：i2c_msg对象的传输宏

    参数：
        adap - i2c_adapter对象
        msgs - i2c_msg对象
        num - 消息数量
    返回值：
        成功返回 num个数，失败返回非num数或错误码

# spi子系统

## spi设备挂载

### 数据结构spi_driver
    struct spi_driver {
        const struct spi_device_id *id_table;
        int                     (*probe)(struct spi_device *spi);
        int                     (*remove)(struct spi_device *spi);
        void                    (*shutdown)(struct spi_device *spi);
        struct device_driver    driver;
    };
    //spi驱动的父类
    struct device_driver {
        const char        *name; //驱动的名字，用来生成节点
    ...
        const struct of_device_id    *of_match_table;//设备树匹配方式
    ...
        struct driver_private *p;//私有属性指针
    };

### spi_register_driver 

    int spi_register_driver(struct spi_driver *sdrv);
    #define spi_register_driver(driver) \
        __spi_register_driver(THIS_MODULE, driver)
    功能：注册spi_driver

### spi_unregister_driver

    void spi_unregister_driver(struct spi_driver *sdrv);
    功能：注销spi_driver

### module_spi_driver

    module_spi_driver(__spi_driver)
    #define module_spi_driver(__spi_driver) \
        module_driver(__spi_driver, spi_register_driver, spi_unregister_driver)
                    
    功能：一键注册注销宏
## spi数据传输


### 数据结构spi_device

    struct spi_device {
        struct device        dev;                 // SPI 设备的通用设备结构体，用于设备模型的集成
        struct spi_controller *controller;        // 该 SPI 设备所属的控制器
        struct spi_controller *master;            // 兼容层，指向控制器，与 controller 成员相同
        u32                 max_speed_hz;         // 该 SPI 设备的最大时钟频率（Hz）
        u32                 mode;                 // SPI 模式，包含时钟相位和极性等信息
            #define  SPI_CPHA        0x01                    /* clock phase */
            #define  SPI_CPOL        0x02                    /* clock polarity */
            #define  SPI_MODE_0      (0|0)                   /* (original MicroWire) */
            #define  SPI_MODE_1      (0|SPI_CPHA)
            #define  SPI_MODE_2      (SPI_CPOL|0)
            #define  SPI_MODE_3      (SPI_CPOL|SPI_CPHA)
            #define  SPI_CS_HIGH     0x04                    /* chipselect active high? */
            #define  SPI_LSB_FIRST   0x08                    /* per-word bits-on-wire */
            #define  SPI_3WIRE       0x10                    /* SI/SO signals shared */
            #define  SPI_LOOP        0x20                    /* loopback mode */
            #define  SPI_NO_CS       0x40                    /* 1 dev/bus, no chipselect */
            #define  SPI_READY       0x80                    /* slave pulls low to pause */
            #define  SPI_TX_DUAL     0x100                   /* transmit with 2 wires */
            #define  SPI_TX_QUAD     0x200                   /* transmit with 4 wires */
            #define  SPI_RX_DUAL     0x400                   /* receive with 2 wires */
            #define  SPI_RX_QUAD     0x800                   /* receive with 4 wires */
        int                 irq;                  // 该设备使用的中断号
        char                modalias[SPI_NAME_SIZE]; // 设备的模块别名
        int                 cs_gpio;              // 片选 GPIO 引脚（遗留字段）
        struct gpio_desc    *cs_gpiod;            // 片选 GPIO 描述符
        ...//其它属性

    };

### spi_setup

    int spi_setup(struct spi_device *spi);
    功能：设置spi_device

### spi_write

    int spi_write(struct spi_device *spi, const char *buf, int len);
    功能：写入spi_device

### spi_read

    int spi_read(struct spi_device *spi, char *buf, int len);
    功能：读取spi_device

### 数据结构spi_transfer

    struct spi_transfer {

        const void      *tx_buf;
        void            *rx_buf;
        unsigned        len;

        dma_addr_t      tx_dma;
        dma_addr_t      rx_dma;
        struct sg_table tx_sg;
        struct sg_table rx_sg;

        unsigned        cs_change:1;
        unsigned        tx_nbits:3;
        unsigned        rx_nbits:3;
    #define     SPI_NBITS_SINGLE        0x01 /* 1bit transfer */
    #define     SPI_NBITS_DUAL          0x02 /* 2bits transfer */
    #define     SPI_NBITS_QUAD          0x04 /* 4bits transfer */
        u8              bits_per_word;
        u16             delay_usecs;
        u32             speed_hz;

        struct list_head transfer_list;
    };

### 数据结构spi_message

    struct spi_message {
        struct list_head        transfers;

        struct spi_device       *spi;

        unsigned                is_dma_mapped:1;

        void                    (*complete)(void *context);
        void                    *context;
        unsigned                frame_length;
        unsigned                actual_length;
        int                     status;

        struct list_head        queue;
        void                    *state;
    };

### spi_message_init

    void spi_message_init(struct spi_message *mesg);
    功能：初始化spi_message

### spi_message_add_tail

    void spi_message_add_tail(struct spi_transfer *tfr, struct spi_message *mesg);
    功能：spi_transfer结构体添加到spi_message队列的末尾

### spi_sync

    int spi_sync(struct spi_device *spi, struct spi_message *mesg);
    功能：同步传输spi_message 阻塞当前线程进行数据传输

### spi_async

    int spi_async(struct spi_device *spi, struct spi_message *mesg);
    功能：异步传输spi_message


# null