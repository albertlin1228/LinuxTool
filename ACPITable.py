import subprocess

import CommonLib

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

def Call2BytesDecode(Offset, HexDumpArray):
    TempByte = {}
    Temp = 0

    for i in range(2):
        Row,Col = TransferOffsetToArray( Offset + i )
        TempByte[i] = int(HexDumpArray[Row][Col],16) 
        Temp |= ( TempByte[i] << (8 * i) )

    return Temp

def Call3BytesDecode(Offset, HexDumpArray):
    TempByte = {}
    Temp = 0

    for i in range(3):
        Row,Col = TransferOffsetToArray( Offset + i )
        TempByte[i] = int(HexDumpArray[Row][Col],16) 
        Temp |= ( TempByte[i] << (8 * i) )

    return Temp

def Call4BytesDecode(Offset, HexDumpArray):
    TempByte = {}
    Temp = 0

    for i in range(4):
        Row,Col = TransferOffsetToArray( Offset + i )
        TempByte[i] = int(HexDumpArray[Row][Col],16) 
        Temp |= ( TempByte[i] << (8 * i) )

    return Temp

def Call8BytesDecode(Offset, HexDumpArray):
    TempByte = {}
    Temp = 0

    for i in range(8):
        Row,Col = TransferOffsetToArray( Offset + i )
        TempByte[i] = int(HexDumpArray[Row][Col],16) 
        Temp |= ( TempByte[i] << (8 * i) )

    return Temp

def GetSignature(HexDumpArray):
    
    # Byte Offset 0x0, Byte Length 0x4
    Byte0 = int(HexDumpArray[0][0],16)
    Byte1 = int(HexDumpArray[0][1],16)
    Byte2 = int(HexDumpArray[0][2],16)
    Byte3 = int(HexDumpArray[0][3],16)

    Strcpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3)

    print(f"[0x00 04]Signature: {HexDumpArray[0][0]} {HexDumpArray[0][1]} {HexDumpArray[0][2]} {HexDumpArray[0][3]} ({Strcpy})")

def GetLength(HexDumpArray):
    
    OFFSET_LENGTH = 4
    # Byte Offset 0x4, Byte Length 0x4
    LengthVal = Call4BytesDecode(OFFSET_LENGTH, HexDumpArray)

    return LengthVal

def GetRevision(HexDumpArray):
    
    # Byte Offset 0x8, Byte Length 0x1
    print(f"[0x08 01]Revision: {HexDumpArray[0][8]}")

def GetChecksum(HexDumpArray):
    
    # Byte Offset 0x9, Byte Length 0x1
    print(f"[0x09 01]Checksum: {HexDumpArray[0][9]}")    

def GetOemId(HexDumpArray):
    
    # Byte Offset 10, Byte Length 0x6
    Byte0 = int(HexDumpArray[0][10],16)
    Byte1 = int(HexDumpArray[0][11],16)
    Byte2 = int(HexDumpArray[0][12],16)
    Byte3 = int(HexDumpArray[0][13],16)
    Byte4 = int(HexDumpArray[0][14],16)
    Byte5 = int(HexDumpArray[0][15],16)

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3) + chr(Byte4) + chr(Byte5)

    print(f"[0x0A 06]OEMID: {HexDumpArray[0][10]} {HexDumpArray[0][11]} {HexDumpArray[0][12]} {HexDumpArray[0][13]} {HexDumpArray[0][14]} {HexDumpArray[0][15]} ({StrCpy})")        

def GetOemTableId(HexDumpArray):
    
    # Byte Offset 16, Byte Length 0x8
    Byte0 = int(HexDumpArray[1][0],16)
    Byte1 = int(HexDumpArray[1][1],16)
    Byte2 = int(HexDumpArray[1][2],16)
    Byte3 = int(HexDumpArray[1][3],16)
    Byte4 = int(HexDumpArray[1][4],16)
    Byte5 = int(HexDumpArray[1][5],16)
    Byte6 = int(HexDumpArray[1][6],16)
    Byte7 = int(HexDumpArray[1][7],16)    

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3) + chr(Byte4) + chr(Byte5) + chr(Byte6) + chr(Byte7)

    print(f"[0x10 08]OEMID Table ID: {HexDumpArray[1][0]} {HexDumpArray[1][1]} {HexDumpArray[1][2]} {HexDumpArray[1][3]} {HexDumpArray[1][4]} {HexDumpArray[1][5]} {HexDumpArray[1][6]} {HexDumpArray[1][7]} ({StrCpy})")

def GetOemRevision(HexDumpArray):
    
    OFFSET_OEM_REV = 24
    # Byte Offset 24, Byte Length 0x4
    OemRevision = Call4BytesDecode(OFFSET_OEM_REV, HexDumpArray)
    print(f"[0x18 04]OEM Revision: {OemRevision}")

def GetCreaterId(HexDumpArray):
    
    # Byte Offset 28, Byte Length 0x4
    Byte0 = int(HexDumpArray[1][12],16)
    Byte1 = int(HexDumpArray[1][13],16)
    Byte2 = int(HexDumpArray[1][14],16)
    Byte3 = int(HexDumpArray[1][15],16)

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3)

    print(f"[0x1C 04]Creater ID: {HexDumpArray[1][12]} {HexDumpArray[1][13]} {HexDumpArray[1][14]} {HexDumpArray[1][15]} ({StrCpy})")

def GetCreaterRevision(HexDumpArray):
    
    OFFSET_REVISION = 32
    # Byte Offset 32, Byte Length 0x4
    CreaterRevision = Call4BytesDecode(OFFSET_REVISION, HexDumpArray)
    print(f"[0x20 04]Creater Revision: 0x{CreaterRevision:04X}")

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
    Length = GetLength(HexDumpArray)
    print(f"[0x04 04]Length: 0x{Length:08X}")
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
    AddressVal = Call8BytesDecode(AddressOffset, HexDumpArray)
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
    IRQ = Call4BytesDecode(OFFSET_GLOBAL_SYS_INTERRUPT, HexDumpArray)
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
    PciDevId = Call2BytesDecode(OFFSET_PCI_DEV_ID, HexDumpArray)
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
    PciFlags = Call4BytesDecode(OFFSET_PCI_FLAGS, HexDumpArray)
    print(f"[0x47 04]PCI Flags : 0x{PciFlags:08X}") 

    # Pci Segment : Offset 75, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PCI_SEG)
    PciSegNum = int(HexDumpArray[Row][Col],16)
    print(f"[0x4B 01]Pci Segment Number : 0x{PciSegNum:02X}")

    # UART Clock Frequency : Offset 76, Length 4 Byte
    UartClk = Call4BytesDecode(OFFSET_UART_CLK_FREQ, HexDumpArray)
    print(f"[0x4C 04]UART Clock Frequency : 0x{UartClk:08X}")   

def ConfigSpaceStructure(HexDumpArray, StrOffset):

    OFFSET_CON_SPACE_STR = 44
    OFFSET_PCI_SEG = 8
    OFFSET_START_BUS = 10
    OFFSET_END_BUS = 11
    OFFSET_RESERVED = 12
    
    BaseAddr = Call8BytesDecode(OFFSET_CON_SPACE_STR + StrOffset, HexDumpArray)
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
    ReservedVal = Call4BytesDecode(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_RESERVED, HexDumpArray)
    print(f"[0x{(OFFSET_CON_SPACE_STR + StrOffset + OFFSET_RESERVED):02X} 04]Reserved: 0x{ReservedVal:08X}")    

def DumpMCFG(HexDumpArray):

    OFFSET_RESERVED = 36
    OFFSET_CON_SPACE_STR = 44

    # Reserved : Offset 36, Length 8 Byte
    Reserved = Call8BytesDecode(OFFSET_RESERVED, HexDumpArray)
    print(f"[0x24 08]Reserved : 0x{Reserved:016X}")

    # Read table length
    Length = GetLength(HexDumpArray)

    StructureNum = (Length - OFFSET_CON_SPACE_STR + 1) // 16
    print("Structure Number:",StructureNum)

    # Configuration space base address allocation structure : Offset 44, each of length 16 Byte
    for i in range(StructureNum):
        print("==================================")
        ConfigSpaceStructure(HexDumpArray, i*16)

def DecodeFlag(Value):
    TimerInterruptMode = Value & CommonLib.BIT0
    TimerInterruptPolarity = (Value & CommonLib.BIT1) >> 1
    AlwaysOnCapability = (Value & CommonLib.BIT2) >> 2

    match TimerInterruptMode:
        case 0:
            print("0: Interrupt is Level triggered")
        case 1:
            print("1: Interrupt is Edge triggered")

    match TimerInterruptPolarity:
        case 0:
            print("0: Interrupt is Active high")
        case 1:
            print("1: Interrupt is Active low")

    match AlwaysOnCapability:
        case 0:
            print("0: Always On Capability")
        case 1:
            print("1: Always On Capability")

def DecodeGTFlag(Value):
    TimerInterruptMode = Value & CommonLib.BIT0
    TimerInterruptPolarity = (Value & CommonLib.BIT1) >> 1

    match TimerInterruptMode:
        case 0:
            print("0: Interrupt is Level triggered")
        case 1:
            print("1: Interrupt is Edge triggered")

    match TimerInterruptPolarity:
        case 0:
            print("0: Interrupt is Active high")
        case 1:
            print("1: Interrupt is Active low")
          
def DecodeCommonFlag(Value):
    SecureTimer = Value & CommonLib.BIT0
    AlwaysOnCapability = (Value & CommonLib.BIT1) >> 1

    match SecureTimer:
        case 0:
            print("0: Timer is Non-secure")
        case 1:
            print("1: Timer is Secure")

    match AlwaysOnCapability:
        case 0:
            print("0: Always On Capability")
        case 1:
            print("1: Always On Capability")

def DecodeArmWdFlag(Value):
    TimerInterruptMode = Value & CommonLib.BIT0
    TimerInterruptPolarity = (Value & CommonLib.BIT1) >> 1
    SecureTimer = (Value & CommonLib.BIT2) >> 2

    match TimerInterruptMode:
        case 0:
            print("0: Interrupt is Level triggered")
        case 1:
            print("1: Interrupt is Edge triggered")

    match TimerInterruptPolarity:
        case 0:
            print("0: Interrupt is Active high")
        case 1:
            print("1: Interrupt is Active low")
    
    match SecureTimer:
        case 0:
            print("0: Timer is Non-secure")
        case 1:
            print("1: Timer is Secure")

def GTBlockTimerStructure(HexDumpArray, StrOffset):
    OFFSET_FRAME_NUM = 124
    OFFSET_RESERVED = 125
    OFFSET_PHY_ADDR = 128
    OFFSET_EL0_PHY_ADDR = 136
    OFFSET_TIMER_INT = 144
    OFFSET_TIMER_FLAGS = 148
    OFFSET_VIR_TIMER_INT = 152
    OFFSET_VIR_TIMER_FLAGS = 156
    OFFSET_COMMON_TIMER_FLAGS = 160

    print("==================================")
    print("[GT Block Timer Structure]")

    # GT Frame Number : Offset 0, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_FRAME_NUM + StrOffset)
    FrameNum = int(HexDumpArray[Row][Col],16)
    print(f"[0x{(OFFSET_FRAME_NUM + StrOffset):02X} 01]GT Frame Number : 0x{FrameNum:02X}")
    
    # Reserved : Offset 1, Length 3 Byte
    Reserved = Call3BytesDecode(OFFSET_RESERVED + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_RESERVED + StrOffset):02X} 03]Reserved : 0x{Reserved:06X}")

    # GTx Physical Address : Offset 4, Length 8 Byte
    PhyAddr = Call8BytesDecode(OFFSET_PHY_ADDR + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_PHY_ADDR + StrOffset):02X} 08]Physical Address : 0x{PhyAddr:016X}")

    # GTx EL0 Physical Address : Offset 12, Length 8 Byte
    El0PhyAddr = Call8BytesDecode(OFFSET_EL0_PHY_ADDR + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_EL0_PHY_ADDR + StrOffset):02X} 08]EL0 Physical Address : 0x{El0PhyAddr:016X}")

    # GTx Physical Timer GSIV : Offset 20, Length 4 Byte
    El0TimerInt = Call4BytesDecode(OFFSET_TIMER_INT + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_TIMER_INT + StrOffset):02X} 04]Timer Interrupt : 0x{El0TimerInt:08X}")      

    # GTx Physical Timer Flags : Offset 24, Length 4 Byte
    El0TimerFlags = Call4BytesDecode(OFFSET_TIMER_FLAGS + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_TIMER_FLAGS + StrOffset):02X} 04]Timer Flags : 0x{El0TimerFlags:08X}")
    DecodeGTFlag(El0TimerFlags)

    # GTx Virtual Timer GSIV : Offset 28, Length 4 Byte
    VirTimerInt = Call4BytesDecode(OFFSET_VIR_TIMER_INT + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_VIR_TIMER_INT + StrOffset):02X} 04]Virtual Timer Interrupt : 0x{VirTimerInt:08X}")      

    # GTx Physical Timer Flags : Offset 32, Length 4 Byte
    VirTimerFlags = Call4BytesDecode(OFFSET_VIR_TIMER_FLAGS + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_VIR_TIMER_FLAGS + StrOffset):02X} 04]Virtual Timer Flags : 0x{VirTimerFlags:08X}")
    DecodeGTFlag(VirTimerFlags)

    # GTx Common Flags : Offset 36, Length 4 Byte
    CommonTimerFlags = Call4BytesDecode(OFFSET_COMMON_TIMER_FLAGS + StrOffset, HexDumpArray)
    print(f"[0x{(OFFSET_COMMON_TIMER_FLAGS + StrOffset):02X} 04]Common Timer Flags : 0x{CommonTimerFlags:08X}")
    DecodeCommonFlag(CommonTimerFlags)                 

def DumpGTDT(HexDumpArray):

    OFFSET_CON_COUNTER_PHY_ADDR = 36
    OFFSET_RESERVED = 44
    OFFSET_SEL1_INT = 48
    OFFSET_SEL1_TIMER = 52
    OFFSET_NON_SEL1_INT = 56
    OFFSET_NON_SEL1_TIMER = 60   
    OFFSET_VIR_SEL1_INT = 64
    OFFSET_VIR_SEL1_TIMER = 68 
    OFFSET_EL2_INT = 72
    OFFSET_EL2_TIMER = 76
    OFFSET_COUN_READ_PHY_ADDR = 80
    OFFSET_PLT_TIMER_COUNT = 88
    OFFSET_PLT_TIMER_OFFSET = 92
    OFFSET_VIR_EL2_INT = 96
    OFFSET_VIR_EL2_TIMER = 100
    OFFSET_PLT_TIMER_STR_TYPE = 104
    OFFSET_PLT_TIMER_STR_LENGTH = 105
    OFFSET_PLT_TIMER_STR_RESERVED = 107
    OFFSET_PLT_TIMER_STR_PHY_ADDR = 108
    OFFSET_GT_BLOCK_TIMER_COUNT = 116
    OFFSET_GT_BLOCK_TIMER_OFFSET = 120
    OFFSET_ARM_WD_LENGTH = 1
    OFFSET_ARM_WD_RESERVED = 3
    OFFSET_ARM_WD_PHY_ADDR = 4
    OFFSET_ARM_WD_CON_PHY_ADDR = 12
    OFFSET_ARM_WD_TIMER_INT = 20
    OFFSET_ARM_WD_TIMER_FLAGS = 24

    # Counter Block Address : Offset 36, Length 8 Byte
    ConCounterPhyAddr = Call8BytesDecode(OFFSET_CON_COUNTER_PHY_ADDR, HexDumpArray)
    print(f"[0x24 08]Counter Block Address : 0x{ConCounterPhyAddr:016X}")

    # Reserved : Offset 44, Length 4 Byte
    Reserved = Call4BytesDecode(OFFSET_RESERVED, HexDumpArray)
    print(f"[0x2C 04]Reserved : 0x{Reserved:08X}")

    # Secure EL1 Timer GSIV : Offset 48, Length 4 Byte
    Sel1Int = Call4BytesDecode(OFFSET_SEL1_INT, HexDumpArray)
    print(f"[0x30 04]Secure EL1 Timer GSIV : 0x{Sel1Int:08X}")

    # Secure EL1 Timer Flags : Offset 52, Length 4 Byte
    Sel1Timer = Call4BytesDecode(OFFSET_SEL1_TIMER, HexDumpArray)
    print(f"[0x34 04]Secure EL1 Timer Flags : 0x{Sel1Timer:08X}")
    DecodeFlag(Sel1Timer)

    print("==================================")

    # Non-Secure EL1 Timer GSIV : Offset 56, Length 4 Byte
    NonSel1Int = Call4BytesDecode(OFFSET_NON_SEL1_INT, HexDumpArray)
    print(f"[0x38 04]Non-Secure EL1 Timer GSIV : 0x{NonSel1Int:08X}")

    # Non-Secure EL1 Timer Flags : Offset 60, Length 4 Byte
    NonSel1Timer = Call4BytesDecode(OFFSET_NON_SEL1_TIMER, HexDumpArray)
    print(f"[0x3C 04]Non-Secure EL1 Timer Flags : 0x{NonSel1Timer:08X}")
    DecodeFlag(NonSel1Timer)

    print("==================================")

    # Virtual EL1 Timer GSIV : Offset 64, Length 4 Byte
    VirSel1Int = Call4BytesDecode(OFFSET_VIR_SEL1_INT, HexDumpArray)
    print(f"[0x40 04]Virtual EL1 Timer GSIV : 0x{VirSel1Int:08X}")

    # Virtual EL1 Timer Flags : Offset 68, Length 4 Byte
    VirSel1Timer = Call4BytesDecode(OFFSET_VIR_SEL1_TIMER, HexDumpArray)
    print(f"[0x44 04]Virtual EL1 Timer Flags : 0x{VirSel1Timer:08X}")
    DecodeFlag(VirSel1Timer)   

    print("==================================")

    # EL2 Timer GSIV : Offset 72, Length 4 Byte
    El2Int = Call4BytesDecode(OFFSET_EL2_INT, HexDumpArray)
    print(f"[0x48 04]EL2 Timer GSIV : 0x{El2Int:08X}")

    # EL2 Timer Flags : Offset 76, Length 4 Byte
    El2Timer = Call4BytesDecode(OFFSET_EL2_TIMER, HexDumpArray)
    print(f"[0x4C 04]EL2 Timer Flags : 0x{El2Timer:08X}")
    DecodeFlag(El2Timer)   

    print("==================================")

    # Counter Read Base Address : Offset 80, Length 8 Byte
    ConReadPhyAddr = Call8BytesDecode(OFFSET_COUN_READ_PHY_ADDR, HexDumpArray)
    print(f"[0x50 08]Counter Read Base Address : 0x{ConReadPhyAddr:016X}")          

    # Platform Timer Count : Offset 88, Length 4 Byte
    PltTimerCount = Call4BytesDecode(OFFSET_PLT_TIMER_COUNT, HexDumpArray)
    print(f"[0x58 04]Platform Timer Count : 0x{PltTimerCount:08X}")

    # Platform Timer Offset : Offset 92, Length 4 Byte
    PltTimerOffset = Call4BytesDecode(OFFSET_PLT_TIMER_OFFSET, HexDumpArray)
    print(f"[0x5C 04]Platform Timer Offset : 0x{PltTimerOffset:08X}")

    # Virtual EL2 Timer GSIV : Offset 96, Length 4 Byte
    VirEl2TimerInt = Call4BytesDecode(OFFSET_VIR_EL2_INT, HexDumpArray)
    print(f"[0x60 04]Virtual EL2 Timer GSIV : 0x{VirEl2TimerInt:08X}")

    # Virtual EL2 Timer Flags : Offset 100, Length 4 Byte
    VirEl2TimerFlag = Call4BytesDecode(OFFSET_VIR_EL2_TIMER, HexDumpArray)
    print(f"[0x64 04]Virtual EL2 Timer Flags : 0x{VirEl2TimerFlag:08X}")     

    print("==================================")

    # Platform Timer Structure Type : Offset 104, Length 1 Byte
    print("Platform Timer Structure:")
    Row,Col = TransferOffsetToArray(OFFSET_PLT_TIMER_STR_TYPE)
    PltTimerStructureType = int(HexDumpArray[Row][Col],16)

    # Platform Timer Structure Length : Offset 105, Length 2 Byte
    StructureLength = Call2BytesDecode(OFFSET_PLT_TIMER_STR_LENGTH,HexDumpArray)

    # Platform Timer Structure Reserved : Offset 107, Length 1 Byte
    Row,Col = TransferOffsetToArray(OFFSET_PLT_TIMER_STR_RESERVED)
    PltTimerStructureReserved = int(HexDumpArray[Row][Col],16)

    # Platform Timer Structure Physical Addr : Offset 108, Length 8 Byte
    PltTimerStructurePhyAddr = Call8BytesDecode(OFFSET_PLT_TIMER_STR_PHY_ADDR,HexDumpArray)

    if(PltTimerStructureType == 0):
        print("==================================")
        print("GT Block Structure Format:")
        print("[0x68 01]Type : 0 [Generic Timer Block]")
        print(f"[0x69 02]Length : 0x{StructureLength:04X}")
        print(f"[0x6B 01]Reserved : 0x{PltTimerStructureReserved:02X}")
        print(f"[0x6C 08]GT Block Physical address : 0x{PltTimerStructurePhyAddr:016X}")
        
        # GT Block Timer Count : Offset 116, Length 4 Byte
        GTBlockTimerCount = Call4BytesDecode(OFFSET_GT_BLOCK_TIMER_COUNT,HexDumpArray)
        print(f"[0x74 04]GT Block Timer Count : 0x{GTBlockTimerCount:08X}")

        # GT Block Timer Offset : Offset 120, Length 4 Byte
        GTBlockTimerOffset = Call4BytesDecode(OFFSET_GT_BLOCK_TIMER_OFFSET,HexDumpArray)
        print(f"[0x78 04]GT Block Timer Offset : 0x{GTBlockTimerOffset:08X}")

        for i in range(GTBlockTimerCount):
            GTBlockTimerStructure(HexDumpArray, (i*40) )

    # Arm Generic Watchdog Structure Format : Offset (0x68 + StructureLength) , Length 28 Byte
    print("==================================")
    print("Arm Generic Watchdog Structure:")
    ArmWatchdogBaseOffset = OFFSET_PLT_TIMER_STR_TYPE + StructureLength
    Row,Col = TransferOffsetToArray(ArmWatchdogBaseOffset)
    PltTimerStructureType = int(HexDumpArray[Row][Col],16)

    if(PltTimerStructureType == 1):
        # Arm Generic Watchdog Timer Structure Type : Offset 0, Length 1 Byte
        print(f"[0x{ArmWatchdogBaseOffset:02X} 01]Type : 0x{PltTimerStructureType:02X}")

        # Arm Generic Watchdog Timer Structure Length : Offset 1, Length 2 Byte
        StructureLength = Call2BytesDecode(ArmWatchdogBaseOffset + OFFSET_ARM_WD_LENGTH, HexDumpArray)
        print(f"[0x{(ArmWatchdogBaseOffset + OFFSET_ARM_WD_LENGTH):02X} 02]Length : 0x{StructureLength:04X}")

        # Reserved : Offset 3, Length 1 Byte
        Row,Col = TransferOffsetToArray(ArmWatchdogBaseOffset + OFFSET_ARM_WD_RESERVED)
        Reserved = int(HexDumpArray[Row][Col],16)
        print(f"[0x{(ArmWatchdogBaseOffset + OFFSET_ARM_WD_RESERVED):02X} 01]Reserved : 0x{Reserved:02X}")

        # RefreshFrame Physical Address : Offset 4, Length 8 Byte
        ArmWdPhyAddr = Call8BytesDecode(ArmWatchdogBaseOffset + OFFSET_ARM_WD_PHY_ADDR, HexDumpArray)
        print(f"[0x{(ArmWatchdogBaseOffset + OFFSET_ARM_WD_PHY_ADDR):02X} 08]RefreshFrame Physical Address : 0x{ArmWdPhyAddr:016X}")

        # Watchdog Control Frame Physical Address : Offset 12, Length 8 Byte
        ArmWdConPhyAddr = Call8BytesDecode(ArmWatchdogBaseOffset + OFFSET_ARM_WD_CON_PHY_ADDR, HexDumpArray)
        print(f"[0x{(ArmWatchdogBaseOffset + OFFSET_ARM_WD_CON_PHY_ADDR):02X} 08]Control Frame Physical Address : 0x{ArmWdConPhyAddr:016X}")

        # Watchdog Timer GSIV : Offset 20, Length 4 Byte
        ArmWdInt = Call4BytesDecode(ArmWatchdogBaseOffset + OFFSET_ARM_WD_TIMER_INT, HexDumpArray)
        print(f"[0x{(ArmWatchdogBaseOffset + OFFSET_ARM_WD_TIMER_INT):02X} 04]Timer Interrupt : 0x{ArmWdInt:08X}")

        # Watchdog Timer Flags : Offset 24, Length 4 Byte
        ArmWdFlag = Call4BytesDecode(ArmWatchdogBaseOffset + OFFSET_ARM_WD_TIMER_FLAGS, HexDumpArray)
        print(f"[0x{(ArmWatchdogBaseOffset + OFFSET_ARM_WD_TIMER_FLAGS):02X} 04]Timer Flags : 0x{ArmWdFlag:08X}")
        DecodeArmWdFlag(ArmWdFlag)        


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
            DumpGTDT(HexDumpArray)
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
        case _:
            DumpGeneralData(AcpiTableString)