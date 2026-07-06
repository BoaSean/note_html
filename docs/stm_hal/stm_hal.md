
## SDMMC

### SDMMC概述

    SD_TypeDef                                                                                                                                  //SDMMC 总线结构体
    SDMMC_InitTypeDef                                                                                                                           //SDMMC 总线初始化结构体
    HAL_SD_CardInfoTypeDef                                                                                                                      //SDMMC 外接 SD 卡信息结构体
    SD_HandleTypeDef                                                                                                                            //SDMMC 总线句柄结构体
    HAL_StatusTypeDef HAL_SD_Init(SD_HandleTypeDef *hsd);                                                                                       //初始化 SD 卡
    HAL_StatusTypeDef HAL_SD_DeInit(SD_HandleTypeDef *hsd);                                                                                     //用于复位 SD 总线初始化
    HAL_StatusTypeDef HAL_SD_ReadBlocks(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd, uint32_t NumberOfBlocks,uint32_t Timeout);    //用于 SD 卡数据读取
    HAL_StatusTypeDef HAL_SD_ReadBlocks_DMA(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd,uint32_t NumberOfBlocks);                  //用于 SD 卡数据读取，DMA 方式
    HAL_StatusTypeDef HAL_SD_WriteBlocks(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd, uint32_t NumberOfBlocks,uint32_t Timeout);   //向 SD 卡写入数据
    HAL_StatusTypeDef HAL_SD_WriteBlocks_DMA(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd,uint32_t NumberOfBlocks);                 //向 SD 卡写入数据，DMA 方式
    HAL_StatusTypeDef HAL_SD_Erase(SD_HandleTypeDef *hsd, uint32_t BlockStartAdd, uint32_t BlockEndAdd);                                        //用于 SD 卡擦除

### SD_TypeDef

    SD_TypeDef	//SDMMC 总线结构体

    stm32h743xx.h

### SDMMC_InitTypeDef

    SDMMC_InitTypeDef //SDMMC 总线初始化结构体   

    stm32h7xx_ll_sdmmc.h

        typedef struct
        {
            uint32_t ClockEdge;            //用于设置 SDMMC 的数据或者命令变化的时钟沿
                        #define SDMMC_CLOCK_EDGE_RISING ((uint32_t)0x00000000U)
                        #define SDMMC_CLOCK_EDGE_FALLING SDMMC_CLKCR_NEGEDGE
        
            uint32_t ClockPowerSave;       //用于设置空闲状态，是否输出时钟
                        #define SDMMC_CLOCK_POWER_SAVE_DISABLE ((uint32_t)0x00000000U)
                        #define SDMMC_CLOCK_POWER_SAVE_ENABLE SDMMC_CLKCR_PWRSAV
        
            uint32_t BusWide;              //用于设置 SDMMC 总线位宽
                        #define SDMMC_BUS_WIDE_1B ((uint32_t)0x00000000U)
                        #define SDMMC_BUS_WIDE_4B SDMMC_CLKCR_WIDBUS_0
                        #define SDMMC_BUS_WIDE_8B SDMMC_CLKCR_WIDBUS_1
        
            uint32_t HardwareFlowControl;  //用于设置时候使能硬件流控制
                        #define SDMMC_HARDWARE_FLOW_CONTROL_DISABLE ((uint32_t)0x00000000U) 
                        #define SDMMC_HARDWARE_FLOW_CONTROL_ENABLE SDMMC_CLKCR_HWFC_EN
        
            uint32_t ClockDiv;             //用于设置 SDMMC 时钟分频，参数范围 0 到 1023
        
        #if (USE_SD_TRANSCEIVER != 0U)
            uint32_t TranceiverPresent;    //用于设置是否带 1.8V 收发器
            #define SDMMC_TRANSCEIVER_UNKNOWN ((uint32_t)0x00000000U)
                #define SDMMC_TRANSCEIVER_NOT_PRESENT ((uint32_t)0x00000001U)
                #define SDMMC_TRANSCEIVER_PRESENT ((uint32_t)0x00000002U)
        #endif /* USE_SD_TRANSCEIVER */
    } SDMMC_InitTypeDef;

### HAL_SD_CardInfoTypeDef

    HAL_SD_CardInfoTypeDef //SDMMC 外接 SD 卡信息结构体  

        stm32h7xx_hal_sd.h


        HAL_SD_CardInfoTypeDef    //SDMMC 外接 SD 卡信息结构体  stm32h7xx_hal_sd.h
            typedef struct
            {
                uint32_t CardType;                     //卡类型
                        /*!< SD Standard Capacity <2Go */
                        #define CARD_SDSC ((uint32_t)0x00000000U) 
                        /*!< SD High Capacity <32Go, SD Extended Capacity <2To */
                        #define CARD_SDHC_SDXC ((uint32_t)0x00000001U) 
                        #define CARD_SECURED ((uint32_t)0x00000003U)
            
                uint32_t CardVersion;                  //卡版本
                        #define CARD_V1_X ((uint32_t)0x00000000U) 
                        #define CARD_V2_X ((uint32_t)0x00000001U)
            
                uint32_t Class;                        //卡类型
            
                uint32_t RelCardAdd;                   //卡相对地址
            
                uint32_t BlockNbr;                     //整个卡的块数
            
                uint32_t BlockSize;                    //每个块的字节数
            
                uint32_t LogBlockNbr;                  //整个卡的逻辑块数
            
                uint32_t LogBlockSize;                 //逻辑块大小
                        #define SPI_FIRSTBIT_MSB (0x00000000UL)
                        #define SPI_FIRSTBIT_LSB SPI_CFG2_LSBFRST
            
                uint32_t CardSpeed;                    //用于设置是否使能 SPI 总线的 TI 模式
                        /*!< Normal Speed Card <12.5Mo/s , Spec Version 1.01 */
                        #define CARD_NORMAL_SPEED ((uint32_t)0x00000000U) 
                        /*!< High Speed Card <25Mo/s , Spec version 2.00 */ 
                        #define CARD_HIGH_SPEED ((uint32_t)0x00000100U) 
                        /*!< UHS-I SD Card <50Mo/s for SDR50, DDR5 Cards
                            and <104Mo/s for SDR104, Spec version 3.01 */
                        #define CARD_ULTRA_HIGH_SPEED ((uint32_t)0x00000200U) 
                
            } HAL_SD_CardInfoTypeDef;

### SD_HandleTypeDef

    SD_HandleTypeDef	//SDMMC 总线句柄结构体      
        stm32h7xx_hal_sd.h

        #if defined (USE_HAL_SD_REGISTER_CALLBACKS) && (USE_HAL_SD_REGISTER_CALLBACKS == 1U)
        typedef struct __SD_HandleTypeDef
        #else
        typedef struct
        #endif /* USE_HAL_SD_REGISTER_CALLBACKS */
        {
            SD_TypeDef                   *Instance;        /*!< SD registers base address           */
        
            SD_InitTypeDef               Init;             /*!< SD required parameters              */
        
            HAL_LockTypeDef              Lock;             /*!< SD locking object                   */
        
            uint8_t                      *pTxBuffPtr;      /*!< Pointer to SD Tx transfer Buffer    */
        
            uint32_t                     TxXferSize;       /*!< SD Tx Transfer size                 */
        
            uint8_t                      *pRxBuffPtr;      /*!< Pointer to SD Rx transfer Buffer    */
        
            uint32_t                     RxXferSize;       /*!< SD Rx Transfer size                 */
        
            __IO uint32_t                Context;          /*!< SD transfer context                 */
        
            __IO HAL_SD_StateTypeDef     State;            /*!< SD card State                       */
        
            __IO uint32_t                ErrorCode;        /*!< SD Card Error codes                 */
        
            HAL_SD_CardInfoTypeDef       SdCard;           /*!< SD Card information                 */
        
            uint32_t                     CSD[4];           /*!< SD card specific data table         */
        
            uint32_t                     CID[4];           /*!< SD card identification number table */
        
        #if defined (USE_HAL_SD_REGISTER_CALLBACKS) && (USE_HAL_SD_REGISTER_CALLBACKS == 1U)
            void (* TxCpltCallback)(struct __SD_HandleTypeDef *hsd);
            void (* RxCpltCallback)(struct __SD_HandleTypeDef *hsd);
            void (* ErrorCallback)(struct __SD_HandleTypeDef *hsd);
            void (* AbortCpltCallback)(struct __SD_HandleTypeDef *hsd);
            void (* Read_DMADblBuf0CpltCallback)(struct __SD_HandleTypeDef *hsd);
            void (* Read_DMADblBuf1CpltCallback)(struct __SD_HandleTypeDef *hsd);
            void (* Write_DMADblBuf0CpltCallback)(struct __SD_HandleTypeDef *hsd);
            void (* Write_DMADblBuf1CpltCallback)(struct __SD_HandleTypeDef *hsd);
        #if (USE_SD_TRANSCEIVER != 0U)
            void (* DriveTransceiver_1_8V_Callback)(FlagStatus status);
        #endif /* USE_SD_TRANSCEIVER */
        
            void (* MspInitCallback)(struct __SD_HandleTypeDef *hsd);
            void (* MspDeInitCallback)(struct __SD_HandleTypeDef *hsd);
        #endif /* USE_HAL_SD_REGISTER_CALLBACKS */
        } SD_HandleTypeDef;
                
        条件编译 USE_HAL_SD_REGISTER_CALLBACKS 用来设置使用自定义回调还是使用默认回调
        此定义一 般放在 stm32h7xx_hal_conf.h 文件里面设置： #define USE_HAL_SD_REGISTER_CALLBACKS 1 
        通过函数 HAL_SD_RegisterCallback 注册回调，取消注册使用函数 HAL_SD_UnRegisterCallback。

### HAL_SD_ReadBlocks

    HAL_StatusTypeDef HAL_SD_ReadBlocks(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd, uint32_t NumberOfBlocks,uint32_t Timeout);	//用于 SD 卡数据读取
        函数参数：
            第 1 个参数是 SD_HandleTypeDef 类型结构体指针变量。
            第 2 个参数是接收数据的缓冲地址。
            第 3 个参数是要读取的扇区地址，即从第几个扇区开始读取（512 字节为一个扇区）。
            第 4 个参数是读取的扇区数。
            第 5 个参数是传输过程的溢出时间，单位 ms。
        返回值
            HAL_TIMEOUT 表示超时HAL_ERROR 表示参数错误HAL_OK 表示发送成功，HAL_BUSY 表示忙，正在使用中。

### HAL_SD_WriteBlocks

    HAL_StatusTypeDef HAL_SD_WriteBlocks(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd, uint32_t NumberOfBlocks,uint32_t Timeout);	//向 SD 卡写入数据
        函数参数：
            第 1 个参数是 SD_HandleTypeDef 类型结构体指针变量。
            第 2 个参数是要写入到 SD 卡的数据缓冲地址。
            第 3 个参数是要写入的扇区地址，即从第几个扇区开始写入（512 字节为一个扇区）。
            第 4 个参数是读取的扇区数。
            第 5 个参数是传输过程的溢出时间，单位 ms。
        返回值
            HAL_TIMEOUT 表示超时HAL_ERROR 表示参数错误HAL_OK 表示发送成功，HAL_BUSY 表示忙，正在使用中。

### HAL_SD_Erase

    HAL_StatusTypeDef HAL_SD_Erase(SD_HandleTypeDef *hsd, uint32_t BlockStartAdd, uint32_t BlockEndAdd);						//用于 SD 卡擦除
        函数参数：
            第 1 个参数是 SD_HandleTypeDef 类型结构体指针变量。
            第 2 个参数是擦除的起始扇区地址，地址单位是第几个扇区（512 字节为一个扇区）。
            第 3 个参数是擦除的结束扇区地址，地址单位是第几个扇区（512 字节为一个扇区）。
        返回值
            HAL_TIMEOUT 表示超时HAL_ERROR 表示参数错误HAL_OK 表示发送成功，HAL_BUSY 表示忙，正在使用中。

### HAL_SD_ReadBlocks_DMA

    HAL_StatusTypeDef HAL_SD_ReadBlocks_DMA(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd,uint32_t NumberOfBlocks);			//用于 SD 卡数据读取，DMA 方式
        函数参数：
            第 1 个参数是 SD_HandleTypeDef 类型结构体指针变量。
            第 2 个参数是接收数据的缓冲地址。
            第 3 个参数是要读取的扇区地址，即从第几个扇区开始读取（512 字节为一个扇区）。
            第 4 个参数是读取的扇区数。
        返回值	
            HAL_TIMEOUT 表示超时
            HAL_ERROR 表示参数错误
            HAL_OK 表示发送成功
            HAL_BUSY 表示忙，正在使用中

### HAL_SD_WriteBlocks_DMA

    HAL_StatusTypeDef HAL_SD_WriteBlocks_DMA(SD_HandleTypeDef *hsd, uint8_t *pData, uint32_t BlockAdd,uint32_t NumberOfBlocks);			//向 SD 卡写入数据，DMA 方式
        函数参数：
            第 1 个参数是 SD_HandleTypeDef 类型结构体指针变量。
            第 2 个参数是要写入到 SD 卡的数据缓冲地址。
            第 3 个参数是要写入的扇区地址，即从第几个扇区开始写入（512 字节为一个扇区）。
            第 4 个参数是读取的扇区数。
        返回值	
            HAL_TIMEOUT 表示超时
            HAL_ERROR 表示参数错误
            HAL_OK 表示发送成功
            HAL_BUSY 表示忙，正在使用中

## ETH

### ETH概述


```C

    /* Exported functions --------------------------------------------------------*/

    /** @addtogroup ETH_Exported_Functions
    * @{
    */

    /** @addtogroup ETH_Exported_Functions_Group1*/
    /* Initialization and de initialization functions  **********************************/
    HAL_StatusTypeDef HAL_ETH_Init(ETH_HandleTypeDef *heth);                                                                             //初始化以太网外设
    HAL_StatusTypeDef HAL_ETH_DeInit(ETH_HandleTypeDef *heth);                                                                            //初始化以太网外设
    void              HAL_ETH_MspInit(ETH_HandleTypeDef *heth);
    void              HAL_ETH_MspDeInit(ETH_HandleTypeDef *heth);

    /** @addtogroup ETH_Exported_Functions_Group2/
    /* IO operation functions *******************************************************/
    HAL_StatusTypeDef HAL_ETH_Start(ETH_HandleTypeDef *heth);                                                                           //启动 MAC + DMA  轮询方式
    HAL_StatusTypeDef HAL_ETH_Start_IT(ETH_HandleTypeDef *heth);                                                                        //启动 MAC + DMA  中断方式
    HAL_StatusTypeDef HAL_ETH_Stop(ETH_HandleTypeDef *heth);                            
    HAL_StatusTypeDef HAL_ETH_Stop_IT(ETH_HandleTypeDef *heth);

    HAL_StatusTypeDef HAL_ETH_ReadData(ETH_HandleTypeDef *heth, void **pAppBuff);                                                       //从 DMA RX 描述符中取出一帧
    HAL_StatusTypeDef HAL_ETH_RegisterRxAllocateCallback(ETH_HandleTypeDef *heth,pETH_rxAllocateCallbackTypeDef rxAllocateCallback);    //注册 RX buffer分配函数    DMA需要 buffer 时，HAL 会回调你  你返回一块内存（通常是 lwIP pbuf）
    HAL_StatusTypeDef HAL_ETH_UnRegisterRxAllocateCallback(ETH_HandleTypeDef *heth);
    HAL_StatusTypeDef HAL_ETH_RegisterRxLinkCallback(ETH_HandleTypeDef *heth, pETH_rxLinkCallbackTypeDef rxLinkCallback);               //DMA 收到一帧后回调        把多个 DMA buffer 链接成一帧  通常在这里把数据交给 lwIP
    HAL_StatusTypeDef HAL_ETH_UnRegisterRxLinkCallback(ETH_HandleTypeDef *heth);
    HAL_StatusTypeDef HAL_ETH_GetRxDataErrorCode(ETH_HandleTypeDef *heth, uint32_t *pErrorCode);
    HAL_StatusTypeDef HAL_ETH_RegisterTxFreeCallback(ETH_HandleTypeDef *heth, pETH_txFreeCallbackTypeDef txFreeCallback);
    HAL_StatusTypeDef HAL_ETH_UnRegisterTxFreeCallback(ETH_HandleTypeDef *heth);
    HAL_StatusTypeDef HAL_ETH_ReleaseTxPacket(ETH_HandleTypeDef *heth);                                                                 //手动释放一个 TX 描述符

    #ifdef HAL_ETH_USE_PTP
    HAL_StatusTypeDef HAL_ETH_PTP_SetConfig(ETH_HandleTypeDef *heth, ETH_PTP_ConfigTypeDef *ptpconfig);
    HAL_StatusTypeDef HAL_ETH_PTP_GetConfig(ETH_HandleTypeDef *heth, ETH_PTP_ConfigTypeDef *ptpconfig);
    HAL_StatusTypeDef HAL_ETH_PTP_SetTime(ETH_HandleTypeDef *heth, ETH_TimeTypeDef *time);
    HAL_StatusTypeDef HAL_ETH_PTP_GetTime(ETH_HandleTypeDef *heth, ETH_TimeTypeDef *time);
    HAL_StatusTypeDef HAL_ETH_PTP_AddTimeOffset(ETH_HandleTypeDef *heth, ETH_PtpUpdateTypeDef ptpoffsettype,
                                                ETH_TimeTypeDef *timeoffset);
    HAL_StatusTypeDef HAL_ETH_PTP_InsertTxTimestamp(ETH_HandleTypeDef *heth);
    HAL_StatusTypeDef HAL_ETH_PTP_GetTxTimestamp(ETH_HandleTypeDef *heth, ETH_TimeStampTypeDef *timestamp);
    HAL_StatusTypeDef HAL_ETH_PTP_GetRxTimestamp(ETH_HandleTypeDef *heth, ETH_TimeStampTypeDef *timestamp);
    HAL_StatusTypeDef HAL_ETH_RegisterTxPtpCallback(ETH_HandleTypeDef *heth, pETH_txPtpCallbackTypeDef txPtpCallback);
    HAL_StatusTypeDef HAL_ETH_UnRegisterTxPtpCallback(ETH_HandleTypeDef *heth);
    #endif /* HAL_ETH_USE_PTP */

    HAL_StatusTypeDef HAL_ETH_Transmit(ETH_HandleTypeDef *heth, ETH_TxPacketConfig *pTxConfig, uint32_t Timeout);                       //阻塞方式发送一帧
    HAL_StatusTypeDef HAL_ETH_Transmit_IT(ETH_HandleTypeDef *heth, ETH_TxPacketConfig *pTxConfig);                                      //非阻塞 / 中断方式

    HAL_StatusTypeDef HAL_ETH_WritePHYRegister(ETH_HandleTypeDef *heth, uint32_t PHYAddr, uint32_t PHYReg, uint32_t RegValue);          //通过 MDIO 访问 PHY 寄存器
    HAL_StatusTypeDef HAL_ETH_ReadPHYRegister(ETH_HandleTypeDef *heth, uint32_t PHYAddr, uint32_t PHYReg,uint32_t *pRegValue);

    void              HAL_ETH_IRQHandler(ETH_HandleTypeDef *heth);
    void              HAL_ETH_TxCpltCallback(ETH_HandleTypeDef *heth);                                                                  //irq  收包完成
    void              HAL_ETH_RxCpltCallback(ETH_HandleTypeDef *heth);                                                                  //irq  发包完成
    void              HAL_ETH_ErrorCallback(ETH_HandleTypeDef *heth);                                                                   //irq  error
    void              HAL_ETH_PMTCallback(ETH_HandleTypeDef *heth);
    void              HAL_ETH_EEECallback(ETH_HandleTypeDef *heth);
    void              HAL_ETH_WakeUpCallback(ETH_HandleTypeDef *heth);
    void              HAL_ETH_RxAllocateCallback(uint8_t **buff);                                                                       //  以太网 DMA 即将接收数据之前”，由用户分配一个接收缓冲区（buffer），并把地址交给 ETH DMA 使用
    void              HAL_ETH_RxLinkCallback(void **pStart, void **pEnd, uint8_t *buff, uint16_t Length);                               //irq  接收完链接接收包   
    void              HAL_ETH_TxFreeCallback(uint32_t *buff);                                                                           //      释放发送buffer                                
    void              HAL_ETH_TxPtpCallback(uint32_t *buff, ETH_TimeStampTypeDef *timestamp);



    /** @addtogroup ETH_Exported_Functions_Group3*/                                                                                     //性能调优
    /* Peripheral Control functions  **********************************************/
    /* MAC & DMA Configuration APIs  **********************************************/
    HAL_StatusTypeDef HAL_ETH_GetMACConfig(ETH_HandleTypeDef *heth, ETH_MACConfigTypeDef *macconf);
    HAL_StatusTypeDef HAL_ETH_GetDMAConfig(ETH_HandleTypeDef *heth, ETH_DMAConfigTypeDef *dmaconf);
    HAL_StatusTypeDef HAL_ETH_SetMACConfig(ETH_HandleTypeDef *heth, ETH_MACConfigTypeDef *macconf);
    HAL_StatusTypeDef HAL_ETH_SetDMAConfig(ETH_HandleTypeDef *heth, ETH_DMAConfigTypeDef *dmaconf);
    void              HAL_ETH_SetMDIOClockRange(ETH_HandleTypeDef *heth);

    /* MAC VLAN Processing APIs    ************************************************/
    void              HAL_ETH_SetRxVLANIdentifier(ETH_HandleTypeDef *heth, uint32_t ComparisonBits, uint32_t VLANIdentifier);

    /* MAC L2 Packet Filtering APIs  **********************************************/
    HAL_StatusTypeDef HAL_ETH_GetMACFilterConfig(ETH_HandleTypeDef *heth, ETH_MACFilterConfigTypeDef *pFilterConfig);
    HAL_StatusTypeDef HAL_ETH_SetMACFilterConfig(ETH_HandleTypeDef *heth, ETH_MACFilterConfigTypeDef *pFilterConfig);
    HAL_StatusTypeDef HAL_ETH_SetHashTable(ETH_HandleTypeDef *heth, uint32_t *pHashTable);
    HAL_StatusTypeDef HAL_ETH_SetSourceMACAddrMatch(ETH_HandleTypeDef *heth, uint32_t AddrNbr, uint8_t *pMACAddr);

    /* MAC Power Down APIs    *****************************************************/
    void              HAL_ETH_EnterPowerDownMode(ETH_HandleTypeDef *heth, ETH_PowerDownConfigTypeDef *pPowerDownConfig);
    void              HAL_ETH_ExitPowerDownMode(ETH_HandleTypeDef *heth);
    HAL_StatusTypeDef HAL_ETH_SetWakeUpFilter(ETH_HandleTypeDef *heth, uint32_t *pFilter, uint32_t Count);


    /** @addtogroup ETH_Exported_Functions_Group4*/
    /* Peripheral State functions  **************************************************/
    HAL_ETH_StateTypeDef HAL_ETH_GetState(ETH_HandleTypeDef *heth);                                                                     //MAC / DMA 配置
    uint32_t             HAL_ETH_GetError(ETH_HandleTypeDef *heth);                                                                     //总错误码
    uint32_t             HAL_ETH_GetDMAError(ETH_HandleTypeDef *heth);                                                                  //DMA 错误（RX 溢出、总线错误）
    uint32_t             HAL_ETH_GetMACError(ETH_HandleTypeDef *heth);
    uint32_t             HAL_ETH_GetMACWakeUpSource(ETH_HandleTypeDef *heth);                                                           //MAC 层错误（CRC、帧格式）

```