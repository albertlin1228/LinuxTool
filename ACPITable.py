import subprocess

OFFSET_REG_BIT_WIDTH = 0x1
OFFSET_REG_BIT_OFFSET = 0x2
OFFSET_ACCESS_SIZE = 0x3
OFFSET_ADDRESS = 0x4

def TransferOffsetToArray(OffsetVal):
    RowVal = 0
    ColVal = 0

    RowVal = OffsetVal//16
    ColVal = OffsetVal%16

    return RowVal,ColVal

def GetSignature(HexDumpArray):
    
    # Byte Offset 0x0, Byte Length 0x4
    Byte0 = int(HexDumpArray[0][0],16)
    Byte1 = int(HexDumpArray[0][1],16)
    Byte2 = int(HexDumpArray[0][2],16)
    Byte3 = int(HexDumpArray[0][3],16)

    Strcpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3)

    print(f"[0x00 04]Signature: {HexDumpArray[0][0]} {HexDumpArray[0][1]} {HexDumpArray[0][2]} {HexDumpArray[0][3]} ({Strcpy})")

def GetLength(HexDumpArray):
    
    # Byte Offset 0x4, Byte Length 0x4
    Byte0 = int(HexDumpArray[0][4],16)
    Byte1 = int(HexDumpArray[0][5],16)
    Byte2 = int(HexDumpArray[0][6],16)
    Byte3 = int(HexDumpArray[0][7],16)

    LengthVal = (Byte3 << 24) | (Byte2 << 16) | (Byte1 << 8) | Byte0 

    print(f"[0x04 04]Length: 0x{LengthVal:08X}")

    return LengthVal

def GetRevision(HexDumpArray):
    
    # Byte Offset 0x8, Byte Length 0x1
    print(f"[0x08 01]Revision: {HexDumpArray[0][8]}")

def GetChecksum(HexDumpArray):
    
    # Byte Offset 0x9, Byte Length 0x1
    print(f"[0x09 01]Checksum: {HexDumpArray[0][9]}")    

def GetOemId(HexDumpArray):
    
    # Byte Offset 0x10, Byte Length 0x6
    Byte0 = int(HexDumpArray[0][10],16)
    Byte1 = int(HexDumpArray[0][11],16)
    Byte2 = int(HexDumpArray[0][12],16)
    Byte3 = int(HexDumpArray[0][13],16)
    Byte4 = int(HexDumpArray[0][14],16)
    Byte5 = int(HexDumpArray[0][15],16)

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3) + chr(Byte4) + chr(Byte5)

    print(f"[0x10 06]OEMID: {HexDumpArray[0][10]} {HexDumpArray[0][11]} {HexDumpArray[0][12]} {HexDumpArray[0][13]} {HexDumpArray[0][14]} {HexDumpArray[0][15]} ({StrCpy})")        

def GetOemTableId(HexDumpArray):
    
    # Byte Offset 0x16, Byte Length 0x8
    Byte0 = int(HexDumpArray[1][0],16)
    Byte1 = int(HexDumpArray[1][1],16)
    Byte2 = int(HexDumpArray[1][2],16)
    Byte3 = int(HexDumpArray[1][3],16)
    Byte4 = int(HexDumpArray[1][4],16)
    Byte5 = int(HexDumpArray[1][5],16)
    Byte6 = int(HexDumpArray[1][6],16)
    Byte7 = int(HexDumpArray[1][7],16)    

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3) + chr(Byte4) + chr(Byte5) + chr(Byte6) + chr(Byte7)

    print(f"[0x16 08]OEMID Table ID: {HexDumpArray[1][0]} {HexDumpArray[1][1]} {HexDumpArray[1][2]} {HexDumpArray[1][3]} {HexDumpArray[1][4]} {HexDumpArray[1][5]} {HexDumpArray[1][6]} {HexDumpArray[1][7]} ({StrCpy})")

def GetOemRevision(HexDumpArray):
    
    # Byte Offset 0x24, Byte Length 0x4
    Byte0 = int(HexDumpArray[1][8],16)
    Byte1 = int(HexDumpArray[1][9],16)
    Byte2 = int(HexDumpArray[1][10],16)
    Byte3 = int(HexDumpArray[1][11],16)

    OemRevision = (Byte3 << 24) | (Byte2 << 16) | (Byte1 << 8) | Byte0 

    print(f"[0x24 04]OEM Revision: {OemRevision}")

def GetCreaterId(HexDumpArray):
    
    # Byte Offset 0x28, Byte Length 0x4
    Byte0 = int(HexDumpArray[1][12],16)
    Byte1 = int(HexDumpArray[1][13],16)
    Byte2 = int(HexDumpArray[1][14],16)
    Byte3 = int(HexDumpArray[1][15],16)

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3)

    print(f"[0x28 04]Creater ID: {HexDumpArray[1][12]} {HexDumpArray[1][13]} {HexDumpArray[1][14]} {HexDumpArray[1][15]} ({StrCpy})")

def GetCreaterRevision(HexDumpArray):
    
    # Byte Offset 0x32, Byte Length 0x4
    Byte0 = int(HexDumpArray[2][0],16)
    Byte1 = int(HexDumpArray[2][1],16)
    Byte2 = int(HexDumpArray[2][2],16)
    Byte3 = int(HexDumpArray[2][3],16)

    CreaterRevision = (Byte3 << 24) | (Byte2 << 16) | (Byte1 << 8) | Byte0 

    print(f"[0x32 04]Creater Revision: 0x{CreaterRevision:04X}")

def DumpGeneralData(TableName):
    HexDumpArray = [[0]*16 for i in range(16)]

    DumpSpcrCmd = f"sudo hexdump -C /sys/firmware/acpi/tables/{TableName}"
    TableDump = subprocess.Popen(DumpSpcrCmd, stdout=subprocess.PIPE, text=True, shell=True)

    Count = 16

    for RowIndex in range(Count):

        ReadLine = TableDump.stdout.readline()
        #print("len(ReadLine):",len(ReadLine))

        print(ReadLine[0:78])

        for ColIndex in range(10,34,3):
            if( ColIndex >= len(ReadLine)):
                break
            if( ReadLine[ColIndex] == " "):
                break
            StrCpy = '0x' + ReadLine[ColIndex] + ReadLine[ColIndex+1]
            ArrayRow = RowIndex
            ArrayCol = (ColIndex-10)//3
            HexDumpArray[ArrayRow][ArrayCol]= hex(int(StrCpy,16))
            #print(f"HexDumpArray[{ArrayRow}][{ArrayCol}]:{HexDumpArray[ArrayRow][ArrayCol]}")

        for ColIndex in range(35,59,3):
            if( ColIndex >= len(ReadLine)):
                break
            if( ReadLine[ColIndex] == " "):
                break

            StrCpy = '0x' + ReadLine[ColIndex] + ReadLine[ColIndex+1]
            ArrayRow = RowIndex
            ArrayCol = (ColIndex-10)//3
            HexDumpArray[ArrayRow][ArrayCol]= hex(int(StrCpy,16))
            #print(f"HexDumpArray[{ArrayRow}][{ArrayCol}]:{HexDumpArray[ArrayRow][ArrayCol]}")

    """
    # Show content
    for RowIndex in range(ArrayRow+1):    
        for ColIndex in range(ArrayCol+1):
            print(f"{HexDumpArray[RowIndex][ColIndex]}")      
    """
    GetSignature(HexDumpArray)
    GetLength(HexDumpArray)
    GetRevision(HexDumpArray)
    GetChecksum(HexDumpArray)
    GetOemId(HexDumpArray)
    GetOemTableId(HexDumpArray)
    GetOemRevision(HexDumpArray)
    GetCreaterId(HexDumpArray)
    GetCreaterRevision(HexDumpArray)

    return HexDumpArray

def GenericAddressStructure(HexDumpArray, Offset):
    # Generic Address Structure : Length 12 Byte
    # Address Space ID
    print(f"[0x{Offset:02X} 12]")
    StrCpy = f"[0x{Offset:02X} 00]Address Space ID : "
    AddressSpaceID = int(HexDumpArray[2][8],16)
    match AddressSpaceID:
        case 0:
            print(f"{StrCpy}0x00 System Memory space")
        case 1:
            print(f"{StrCpy}0x01 System I/O space")
        case 2:
            print(f"{StrCpy}0x02 PCI Configuration space")
        case 3:
            print(f"{StrCpy}0x03 Embedded Controller")
        case 4:
            print(f"{StrCpy}0x04 SMBus")
        case 5:
            print(f"{StrCpy}0x05 SystemCMOS")
        case 6:
            print(f"{StrCpy}0x06 PciBarTarget")
        case 7:
            print(f"{StrCpy}0x07 IPMI")
        case 8:
            print(f"{StrCpy}0x08 General PurposeIO")
        case 9:
            print(f"{StrCpy}0x09 GenericSerialBus")
        case 10:
            print(f"{StrCpy}0x0A Platform Communications Channel (PCC)")
        case 0x7F:
            print(f"{StrCpy}0x7F Functional Fixed Hardware")
        case num if num in range(0xB,0x7E):
            print(f"{StrCpy}Reserved")
        case num if num in range(0x80,0xBF):
            print(f"{StrCpy}Reserved")
        case num if num in range(0xC0,0xFF):
            print(f"{StrCpy}OEM defined")    

    # Register Bit Width : Offset 1, Length 1 Byte
    RBWOffset = Offset + OFFSET_REG_BIT_WIDTH
    Row,Col = TransferOffsetToArray(RBWOffset)
    RegisterBitWidth = int(HexDumpArray[Row][Col],16)
    print(f"[0x{RBWOffset:02X} 01]Register Bit Width : {RegisterBitWidth:02X}")

    # Register Bit Offset : Offset 2, Length 1 Byte
    RBOOffset = Offset + OFFSET_REG_BIT_OFFSET
    Row,Col = TransferOffsetToArray(RBOOffset)
    RegisterBitOffset = int(HexDumpArray[Row][Col],16)

    print(f"[0x{RBOOffset:02X} 01]Register Bit Offset : {RegisterBitOffset:02X}")

    # Access Size : Offset 3, length 1 Byte
    AccessSizeOffset = Offset + OFFSET_ACCESS_SIZE
    Row,Col = TransferOffsetToArray(AccessSizeOffset)
    AccessSize = int(HexDumpArray[Row][Col],16)
    match AccessSize:
        case 0:
            print(f"[0x{AccessSizeOffset:02X} 01]Access Size : 0 Undefined (legacy reasons)")
        case 1:
            print(f"[0x{AccessSizeOffset:02X} 01]Access Size : 1 Byte access")
        case 2:
            print(f"[0x{AccessSizeOffset:02X} 01]Access Size : 2 Word access")
        case 3:
            print(f"[0x{AccessSizeOffset:02X} 01]Access Size : 3 Dword access")
        case 4:
            print(f"[0x{AccessSizeOffset:02X} 01]Access Size : 4 QWord access")
    
    # Address : Offset 4, length 8 Byte
    AddressOffset = Offset + OFFSET_ADDRESS
    Row,Col = TransferOffsetToArray(AddressOffset)
    AddressByte0 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(AddressOffset+1)
    AddressByte1 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(AddressOffset+2)
    AddressByte2 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(AddressOffset+3)
    AddressByte3 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(AddressOffset+4)
    AddressByte4 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(AddressOffset+5)
    AddressByte5 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(AddressOffset+6)
    AddressByte6 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(AddressOffset+7)
    AddressByte7 = int(HexDumpArray[Row][Col],16)

    AddressVal = (AddressByte7<<56) | (AddressByte6<<48) | (AddressByte5<<40) | (AddressByte4<<32) | (AddressByte3<<24) | (AddressByte2<<16) | (AddressByte1<<8) | AddressByte0
    print(f"[0x{AddressOffset:02X} 08]Address : 0x{AddressVal:016X}")

def DumpSPCR(HexDumpArray):

    OFFSET_INTERRUPT_TYPE = 52
    OFFSET_IRQ = 53
    OFFSET_GLOBAL_SYS_INTERRUPT = 54
    OFFSET_BAUD_RATE = 58
    OFFSET_PARITY = 59
    OFFSET_STOP_BITS = 60
    OFFSET_FLOW_CONTROL = 61
    OFFSET_TER_TYPE = 62
    OFFSET_LANGUAGE = 63
    OFFSET_PCI_DEV_ID = 64
    OFFSET_PCI_VEN_ID = 66
    OFFSET_PCI_BUS = 68
    OFFSET_PCI_DEV = 69
    OFFSET_PCI_FUN = 70
    OFFSET_PCI_FLAGS = 71    
    OFFSET_PCI_SEG = 75 
    OFFSET_UART_CLK_FREQ = 76

    # Interface Type : Offset 36(0x24), Length 1 Byte
    InterfaceType = int(HexDumpArray[2][4],16)
    print(f"[0x24 01]Interface Type:{InterfaceType}")

    # Reserved : Offset 37(0x25), Length 3 Byte
    Reserved = (int(HexDumpArray[2][7],16) << 16) | (int(HexDumpArray[2][6],16) << 8) | int(HexDumpArray[2][5],16)
    print(f"[0x25 03]Reserved:0x{Reserved:08X}")

    print("==================================")

    print("Generic Address Structure")
    SpcrGasOffset = 0x28
    GenericAddressStructure(HexDumpArray,SpcrGasOffset)

    print("==================================")

    # Interrupt Type : Offset 52, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_INTERRUPT_TYPE)
    InterruptType = int(HexDumpArray[Row][Col],16)
    print(f"[0x34 01]Interrupt Type : {InterruptType}")

    # IRQ : Offset 53, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_IRQ)
    IRQ = int(HexDumpArray[Row][Col],16)
    print(f"[0x35 01]PC-AT-compatible IRQ : {IRQ}")

    # Global System Interrupt : Offset 54, Length 4 Byte
    Row,Col = TransferOffsetToArray(OFFSET_GLOBAL_SYS_INTERRUPT)
    IRQByte0 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_GLOBAL_SYS_INTERRUPT+1)
    IRQByte1 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_GLOBAL_SYS_INTERRUPT+2)
    IRQByte2 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_GLOBAL_SYS_INTERRUPT+3)
    IRQByte3 = int(HexDumpArray[Row][Col],16)

    IRQ = (IRQByte3<<24) | (IRQByte2<<16) | (IRQByte1<<8) | IRQByte0

    print(f"[0x36 04]Global System Interrupt : 0x{IRQ:08X}")

    # Baud Rate : Offset 58, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_BAUD_RATE)
    BaudRate = int(HexDumpArray[Row][Col],16)
    match BaudRate:
        case 0:
            print(f"[0x3A 01]Baud Rate : {BaudRate}")
        case 3:
            print(f"[0x3A 01]Baud Rate : {BaudRate} (9600)")
        case 4:
            print(f"[0x3A 01]Baud Rate : {BaudRate} (19200)")
        case 6:
            print(f"[0x3A 01]Baud Rate : {BaudRate} (57600)")
        case 7:
            print(f"[0x3A 01]Baud Rate : {BaudRate} (115200)")
        case _:
            print(f"[0x3A 01]Baud Rate : {BaudRate} (Reserved)")

    # Parity : Offset 59, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PARITY)
    Parity = int(HexDumpArray[Row][Col],16)
    print(f"[0x3B 01]Parity : 0x{Parity:02X}")

    # Stop Bits : Offset 60, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_STOP_BITS)
    StopBits = int(HexDumpArray[Row][Col],16)
    print(f"[0x3C 01]Stop Bits : 0x{StopBits:02X}")

    # Flow Control : Offset 61, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_FLOW_CONTROL)
    FlowControl = int(HexDumpArray[Row][Col],16)
    print(f"[0x3D 01]Flow Control : 0x{FlowControl:02X}")

    # Terminal Type : Offset 62, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_TER_TYPE)
    TerminalType = int(HexDumpArray[Row][Col],16)
    match TerminalType:
        case 0:
            print(f"[0x3E 01]Terminal Type : 0x{TerminalType} (VT100)")
        case 1:
            print(f"[0x3E 01]Terminal Type : 0x{TerminalType} (Extended VT100 (VT100+))")
        case 2:
            print(f"[0x3E 01]Terminal Type : 0x{TerminalType} (VT-UTF8)")
        case 3:
            print(f"[0x3E 01]Terminal Type : 0x{TerminalType} (ANSI)")
        case _:
            print(f"[0x3E 01]Terminal Type : 0x{TerminalType} (Reserved)")
    
    # Language : Offset 63, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_LANGUAGE)
    Language = int(HexDumpArray[Row][Col],16)
    print(f"[0x3E 01]Language : 0x{Language:02X}")

    # PCI device id : Offset 64, Length 2 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_DEV_ID)
    PciDevIdByte0 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_PCI_DEV_ID+1)
    PciDevIdByte1 = int(HexDumpArray[Row][Col],16)

    PciDevId = (PciDevIdByte1<<8) | PciDevIdByte0
    print(f"[0x40 02]PCI device id : 0x{PciDevId:04X}")

     # PCI vendor id : Offset 66, Length 2 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_VEN_ID)
    PciVenIdByte0 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_PCI_DEV_ID+1)
    PciVenIdByte1 = int(HexDumpArray[Row][Col],16)

    PciVenId = (PciVenIdByte1<<8) | PciVenIdByte0
    print(f"[0x42 02]PCI vendor id : 0x{PciVenId:04X}")   

    # Pci Bus Number : Offset 68, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_BUS)
    PciBusNum = int(HexDumpArray[Row][Col],16)
    print(f"[0x44 01]Pci Bus Number : 0x{PciBusNum:02X}")

    # Pci Device Number : Offset 69, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_DEV)
    PciDevNum = int(HexDumpArray[Row][Col],16)
    print(f"[0x45 01]Pci Device Number : 0x{PciDevNum:02X}")

    # Pci Function Number : Offset 70, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_FUN)
    PciFunNum = int(HexDumpArray[Row][Col],16)
    print(f"[0x46 01]Pci Function Number : 0x{PciFunNum:02X}")    

     # PCI Flags : Offset 71, Length 4 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_FLAGS)
    PciFlagsByte0 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_PCI_FLAGS+1)
    PciFlagsByte1 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_PCI_FLAGS+2)
    PciFlagsByte2 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_PCI_FLAGS+3)
    PciFlagsByte3 = int(HexDumpArray[Row][Col],16)

    PciFlags = (PciFlagsByte3<<24) | (PciFlagsByte2<<16) | (PciFlagsByte1<<8) | PciFlagsByte0
    print(f"[0x47 04]PCI Flags : 0x{PciFlags:08X}") 

    # Pci Segment : Offset 75, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_SEG)
    PciSegNum = int(HexDumpArray[Row][Col],16)
    print(f"[0x4B 01]Pci Segment Number : 0x{PciSegNum:02X}")

     # UART Clock Frequency : Offset 76, Length 4 Byte
    Row,Col = TransferOffsetToArray(OFFSET_UART_CLK_FREQ)
    UartClkByte0 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_UART_CLK_FREQ+1)
    UartClkByte1 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_UART_CLK_FREQ+2)
    UartClkByte2 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_UART_CLK_FREQ+3)
    UartClkByte3 = int(HexDumpArray[Row][Col],16)

    UartClk = (UartClkByte3<<24) | (UartClkByte2<<16) | (UartClkByte1<<8) | UartClkByte0
    print(f"[0x4C 04]UART Clock Frequency : 0x{UartClk:08X}")   

def ConfigSpaceStructure(HexDumpArray, StrOffset):
    BaseAddrByte = {}
    Reserved = {}

    OFFSET_CON_SPACE_STR = 44
    OFFSET_PCI_SEG = 8
    OFFSET_START_BUS = 10
    OFFSET_END_BUS = 11
    OFFSET_RESERVED = 12
    
    for i in range(8):
        Row,Col = TransferOffsetToArray(OFFSET_CON_SPACE_STR + StrOffset + i)
        BaseAddrByte[i] = int(HexDumpArray[Row][Col],16) 

    BaseAddr = (BaseAddrByte[7]<<56) | (BaseAddrByte[6]<<48) | (BaseAddrByte[5]<<40) | (BaseAddrByte[4]<<32) | (BaseAddrByte[3]<<24) | (BaseAddrByte[2]<<16) | (BaseAddrByte[1]<<8) | BaseAddrByte[0]
    print(f"[0x{(OFFSET_CON_SPACE_STR + StrOffset):02X} 08]Base Address : 0x{BaseAddr:016X}")

    # Pci Seg : Offset 8, Length 2 Byte
    Row,Col = TransferOffsetToArray(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_PCI_SEG)
    PciSegByte0 = int(HexDumpArray[Row][Col],16)
    Row,Col = TransferOffsetToArray(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_PCI_SEG + 1)
    PciSegByte1 = int(HexDumpArray[Row][Col],16)

    PciSeg = PciSegByte1 << 8 | PciSegByte0
    print(f"[0x{(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_PCI_SEG):02X} 02]Pci Segment Group Number: 0x{PciSeg:04X}")

    # Pci Start Bus : Offset 10, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_START_BUS)
    PciStartBus = int(HexDumpArray[Row][Col],16)    
    print(f"[0x{(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_START_BUS):02X} 01]Pci Start Bus: 0x{PciStartBus:02X}")
    # Pci End Bus : Offset 11, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_END_BUS)
    PciEndBus = int(HexDumpArray[Row][Col],16)     
    print(f"[0x{(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_END_BUS):02X} 01]Pci End Bus: 0x{PciEndBus:02X}")

    # Reserved : Offset 12, Length 4 Byte
    for i in range(4):
        Row,Col = TransferOffsetToArray(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_RESERVED + i)
        Reserved[i] = int(HexDumpArray[Row][Col],16)
    ReservedVal = (Reserved[3]<<24) | (Reserved[2]<<16) | (Reserved[1]<<8) | Reserved[0]
             
    print(f"[0x{(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_RESERVED):02X} 04]Reserved: 0x{ReservedVal:08X}")    

def DumpMCFG(HexDumpArray):
    ReservedByte = {}

    OFFSET_RESERVED = 36
    OFFSET_CON_SPACE_STR = 44

    # Reserved : Offset 36, Length 8 Byte
    for i in range(8):
        Row,Col = TransferOffsetToArray(OFFSET_RESERVED+i)
        ReservedByte[i] = int(HexDumpArray[Row][Col],16) 

    Reserved = (ReservedByte[7]<<56) | (ReservedByte[6]<<48) | (ReservedByte[5]<<40) | (ReservedByte[4]<<32) | (ReservedByte[3]<<24) | (ReservedByte[2]<<16) | (ReservedByte[1]<<8) | ReservedByte[0]
    print(f"[0x24 08]Reserved : 0x{Reserved:016X}")

    # Read table length
    Length = GetLength(HexDumpArray)

    StructureNum = (Length - OFFSET_CON_SPACE_STR + 1) // 16
    print("Structure Number:",StructureNum)

    # Configuration space base address allocation structure : Offset 44, each of length 16 Byte
    for i in range(StructureNum):
        print("==================================")
        ConfigSpaceStructure(HexDumpArray, i*16)
        

def DumpAcpiTable(AcpiTableString):
    match AcpiTableString:
        case "SPCR":
            HexDumpArray = DumpGeneralData("SPCR")
            DumpSPCR(HexDumpArray)
        case "MCFG":
            HexDumpArray = DumpGeneralData("MCFG")
            DumpMCFG(HexDumpArray)
        case "GTDT":
            HexDumpArray = DumpGeneralData("GTDT")
        case "APMT":
            HexDumpArray = DumpGeneralData("APMT")
        case "EINJ":
            HexDumpArray = DumpGeneralData("EINJ")
        case "APIC":
            HexDumpArray = DumpGeneralData("APIC")
        case "PCCT":
            HexDumpArray = DumpGeneralData("PCCT")
        case "SSDT2":
            HexDumpArray = DumpGeneralData("SSDT2")
        case "HMAT":
            HexDumpArray = DumpGeneralData("HMAT")
        case "IORT":
            HexDumpArray = DumpGeneralData("IORT")
        case "SLIT":
            HexDumpArray = DumpGeneralData("SLIT")
        case "SPMI":
            HexDumpArray = DumpGeneralData("SPMI")
        case "SDEI":
            HexDumpArray = DumpGeneralData("SDEI")
        case "DSDT":
            HexDumpArray = DumpGeneralData("DSDT")
        case "SRAT":
            HexDumpArray = DumpGeneralData("SRAT")
        case "DBG2":
            HexDumpArray = DumpGeneralData("DBG2")
        case "HEST":
            HexDumpArray = DumpGeneralData("HEST")
        case "SSDT3":
            HexDumpArray = DumpGeneralData("SSDT3")
        case "FACP":
            HexDumpArray = DumpGeneralData("FACP")
        case "SSDT1":
            HexDumpArray = DumpGeneralData("SSDT1")
        case "RAS2":
            HexDumpArray = DumpGeneralData("RAS2")
        case "AGDI":
            HexDumpArray = DumpGeneralData("AGDI")
        case "PPTT":
            HexDumpArray = DumpGeneralData("PPTT")