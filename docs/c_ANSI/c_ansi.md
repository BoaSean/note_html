
## 概述

### 快速开始

欢迎使用本 API 手册。
ANSI /ISO 



|分类|C89/C90|C95|C99|C11|
|---|---|---|---|---|
|程序结构 / 基础语言支持|<assert.h><br><stddef.h><br><stdarg.h>|<iso646.h>|<stdbool.h><br><stdint.h>|<stdalign.h><br><stdnoreturn.h>|
|工具 / 内存 / 通用函数|<stdlib.h><br><string.h><br><errno.h><br><limits.h>||||
|输入输出|<stdio.h>||||
|数学 / 数值计算|<math.h><br><float.h>||<fenv.h><br><complex.h><br><tgmath.h>||
|系统功能 / 时间 / 本地化|<time.h><br><signal.h><br><setjmp.h><br><locale.h>||<inttypes.h>||
|字符集 / 宽字符|<ctype.h>|<wchar.h><br><wctype.h>||<uchar.h>|
|并发 / 多线程 / 原子||||<threads.h><br><stdatomic.h>|

## <assert.h> - 条件编译宏
## <complex.h> - 复数运算
## <ctype.h> - 字符类型

### isalpha

    int isalpha(int c);

    功能：检查字符是否为字母。

    注意：
        参数必须是可表示为unsigned char的值或EOF
        依赖于当前的本地化设置
        通常只识别ASCII字母

    参数：
        c - 要检查的字符

    返回值：
        如果是字母返回非0值，否则返回0

    示例：
        char c1 = 'A';
        char c2 = '1';
        if (isalpha(c1))  // 返回非0值
            printf("是字母\n");
        if (!isalpha(c2))  // 返回0
            printf("不是字母\n");

### isdigit

    int isdigit(int c);

    功能：检查字符是否为数字。

    注意：
        只检查十进制数字（0-9）
        参数必须是可表示为unsigned char的值或EOF
        不识别其他数字表示（如罗马数字）
    参数：
        c - 要检查的字符
    返回值：
        如果是数字返回非0值，否则返回0
    示例：
        char c1 = '5';
        char c2 = 'a';
        if (isdigit(c1))  // 返回非0值
            printf("是数字\n");
        if (!isdigit(c2))  // 返回0
            printf("不是数字\n");


## <errno.h> - 错误码
## <fenv.h> - 浮点环境
## <float.h> - 浮点极限
## <inttypes.h> - 整数格式
## <iso646.h> - 替代符号
## <limits.h> - 类型限制
## <locale.h> - 本地化
## <math.h> - 数学函数

### sqrt

    double sqrt(double x);
    
    功能：计算平方根。

    注意：
        参数必须是非负数
        负数参数会导致域错误
        返回值总是非负的
    参数：
        x - 要计算平方根的数（必须为非负数）
    返回值：
        x的平方根
    示例：
        double result = sqrt(16.0);  // 返回 4.0
        double result2 = sqrt(2.0);  // 返回 1.4142135623730951

### pow

    double pow(double x, double y);
    功能：计算x的y次方。

    注意：
        负数的非整数次方会导致域错误
        0的0次方结果是未定义的
        可能发生上溢或下溢
    参数：
        x - 底数
        y - 指数
    返回值：
        x的y次方
    示例：
        double result1 = pow(2.0, 3.0);  // 返回 8.0
        double result2 = pow(3.0, 2.0);  // 返回 9.0
        double result3 = pow(2.0, -1.0);  // 返回 0.5

## <setjmp.h> - 非局部跳转
## <signal.h> - 信号处理
## <stdalign.h> - 对齐控制
## <stdarg.h> - 可变参数
## <stdatomic.h> - 原子操作
## <stdbool.h> - 布尔类型
## <stddef.h> - 常用定义
## <stdint.h> - 定宽整数
## <stdio.h> - 输入输出

### printf

    int printf(const char *format, ...);
    功能：格式化输出到标准输出流。

    注意：
        格式字符串中的%数量必须与后续参数数量匹配
        格式字符串不能为NULL
        确保使用正确的格式说明符（%d用于整数，%s用于字符串等）
    参数：
        format - 格式化字符串
        ... - 可变参数列表
    返回值：
        输出的字符数，出错时返回负值
    示例：
        int age = 25;
        char name[] = "John";
        printf("Name: %s, Age: %d\n", name, age);  // 输出：Name: John, Age: 25

### scanf

    int scanf(const char *format, ...);
    功能：从标准输入读取格式化输入。

    注意：
        所有参数必须是指针类型
        字符串输入要注意缓冲区溢出风险
        格式字符串不能为NULL
        输入缓冲区中的空白字符会被跳过
    参数：
        format - 格式化字符串
        ... - 可变参数列表（指针）
    返回值：
        成功读取的项目数，EOF表示错误或文件结束
    示例：
        int age;
        char name[50];
        scanf("%s %d", name, &age);  // 输入：John 25
        // name 现在包含 "John"，age 现在是 25

### fopen

    FILE *fopen(const char *filename, const char *mode);
    功能：打开文件。

    注意：
        文件名和模式字符串都不能为NULL
        确保有适当的文件访问权限
        使用完文件后需要调用fclose关闭
        写入模式会创建新文件或清空已有文件
    参数：
        filename - 文件名
        mode - 打开模式（"r"读取，"w"写入，"a"追加等）
    返回值：
        文件指针，失败时返回NULL
    示例：
        FILE *fp = fopen("test.txt", "r");
        if (fp == NULL) {
            printf("无法打开文件\n");
            return 1;
        }
        // 使用文件...
        fclose(fp);


## <stdlib.h> - 通用工具
## <stdnoreturn.h> - 无返回宏
## <string.h> - 字符串处理

### memcpy

    void *memcpy(void *dest, const void *src, size_t n);
    功能：从源内存区域复制数据到目标内存区域。

    注意：
        源内存区域和目标内存区域不能重叠
        遇到\0不会停止
    参数：
        dest - 目标内存区域的指针
        src - 源内存区域的指针
        n - 要复制的字节数
    返回值：
        返回目标内存区域的指针
    示例：
        #include <stdio.h>
        #include <string.h>

        int main() {
            char src[] = "hello\0world";
            char dest[20] = {0};

            memcpy(dest, src, sizeof(src));  // 拷贝整个 src，包括 \0 后的数据

            printf("dest: %s\n", dest);          // 只输出 "hello"，因为 printf 遇到 '\0' 停止
            printf("dest[6]: %c\n", dest[6]);    // 输出 'w'，说明 \0 后的数据也被复制了

            return 0;
        }


        int main(){
            char a[10] ={0x01,0x02,0x03,0x04,0x00,0x06,0x07,0x08,0x09,0x10};
            char b[10]={0};
            memcpy(b, a, 10);
            for(int i=0;i<10;i++){
                printf("%x",b[i]);              //输出 1 2 3 4 0 6 7 8 9 10
            }
            return 0;
        }

## <tgmath.h> - 泛型数学
## <threads.h> - 线程支持
## <time.h> - 时间日期

### time_t

    typedef long int time_t;

    功能：定义时间类型。用于表示时间戳

    注意：
        时间戳：从1970年1月1日00:00:00 UTC到当前时间的秒数

### ctime

    char *ctime(const time_t *timep);

    功能：将时间戳转换为字符串。

    参数：
        timep - 指向时间戳的指针
    返回值：
        成功返回的字符串首地址 格式为："Wed Mar 12 10:00:00 2025\n"
        失败返回NULL
    示例：
        time_t now = time(NULL);
        char *time_str = ctime(&now);
        printf("当前时间: %s", time_str);

## <uchar.h> - Unicode支持
## <wchar.h> - 宽字符支持
## <wctype.h> - 宽字符类型
