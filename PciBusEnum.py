import os
import subprocess
#import mmap
#import struct
"""
from periphery import MMIO

  | Reserved (MBZ) | Segment | Reserved (MBZ) |     Bus     | Device | Function | Register |
  63             48  47    32  31           28 27         20 19    15 14      12 11         0
            PCI Register: Bits 0..11
            PCI Function  Bits 12..14
            PCI Device  Bits 15..19
            PCI Bus Bits 20..27
            Reserved  Bits 28..31.  Must be 0.
            PCI Segment Bits 32..47
            Reserved  Bits 48..63.  Must be 0.  

def PciEnum():
    for Segment in range(8):
        print("====Segment", Segment, "====")
        for Bus in range(256):
            for Dev in range(32):
                for Fun in range(8):
                    #Address = Segment + (0x1 << 31) + (Bus << 20) + (Dev << 15) + (Fun << 12)
                    Address = 0x80000000 + (Bus << 20) + (Dev << 15) + (Fun << 12)
                    print("Address = ",Address)
                    VidDid = MMIO(Address,0x4)
                    print("VidDid = ", VidDid)
"""
# Global variable
GlobalExistDevice = 0
GlobalVendorId = 0
GlobalDeviceId = 0

# Bit definition
BIT0 = 1
BIT1 = 1 << 1
BIT2 = 1 << 2
BIT3 = 1 << 3
BIT4 = 1 << 4
BIT5 = 1 << 5
BIT6 = 1 << 6
BIT7 = 1 << 7
BIT8 = 1 << 8
BIT9 = 1 << 9
BIT10 = 1 << 10
BIT11 = 1 << 11
BIT12 = 1 << 12
BIT13 = 1 << 13
BIT14 = 1 << 14
BIT15 = 1 << 15
BIT16 = 1 << 16
BIT17 = 1 << 17
BIT18 = 1 << 18
BIT19 = 1 << 19
BIT20 = 1 << 20
BIT21 = 1 << 21
BIT22 = 1 << 22
BIT23 = 1 << 23
BIT24 = 1 << 24
BIT25 = 1 << 25
BIT26 = 1 << 26
BIT27 = 1 << 27
BIT28 = 1 << 28
BIT29 = 1 << 29
BIT30 = 1 << 30
BIT31 = 1 << 31


# Pci configuration space offset
OFFSET_COMMAND = 0x4                # Command offset
OFFSET_UE_STATUS = 0x4              # UE status offset
OFFSET_STATUS = 0x6                 # Status offset
OFFSET_HEADER_TYPE = 0xE            # Header type offset
OFFSET_32_BAR0_TYPE = 0x10          # 32 bit BAR0 offset
OFFSET_PCIE_CAP = 0x2               # Pcie capabilities offset
OFFSET_DEVICE_CAP = 0x4             # Device capability offset
OFFSET_DEVICE_CONTROL = 0x8         # Device control offset
OFFSET_DEVICE_STATUS = 0xA          # Device status offset
OFFSET_LINK_CAPABILITY = 0xC        # Link capability offset
OFFSET_LINK_CONTROL = 0x10          # Link control offset
OFFSET_LINK_STATUS = 0x12           # Link status offset
OFFSET_PRI_BUS_NUMBER = 0x18        # Primary Bus offset
OFFSET_SEC_BUS_NUMBER = 0x19        # Second Bus offset
OFFSET_SUB_BUS_NUMBER = 0x1A        # Subordinate Bus offset
OFFSET_PCIE_EXT_CAP_HEADER = 0x100  # Pcie Extend Cap Header Offset

# Pci Regiset Description
PCI_STATUS_CAP = 0x10
HEADER_LAYOUT_CODE = 0x7f
HEADER_TYPE_CARDBUS_BRIDGE = 0x2
PCI_CARD_BUS_BRIDGE_CAP_PTR = 0x14
PCI_CAP_PTR = 0x34

class Device(object):

    __base = "/sys/bus/pci/devices/"

    def __init__(self, pciid:str):
        global GlobalExistDevice
        global GlobalVendorId
        global GlobalDeviceId

        self.__base = os.path.join(self.__base, str(pciid))
        self.__vendor = f"{self.__base}/vendor"
        self.__device = f"{self.__base}/device"

        if not os.access(self.__base, os.F_OK):
            #raise ValueError("Device not found:%s" % (self.__base))
            GlobalExistDevice = 0
        else:
            #print("Access ", self.__base ," ok")
            GlobalExistDevice = 1

            # Print VendorId
            with open(self.__vendor,'r') as file:
                GlobalVendorId = file.read()
            
            # Print DeviceId
            with open(self.__device,'r') as file:
                GlobalDeviceId = file.read()

def PciEnumOperation():
    PfaNumberArray = []
    HexVendor = {}
    HexDevice = {}

    PfaNumberIndex = 0

    for Segment in range(8):
        for Bus in range(256):
            for Dev in range(32):
                for Fun in range(8):
                    # PfaNumber = 0007:00:01.0
                    PfaNumber = f"{str(Segment).zfill(4)}:{str(Bus).zfill(2)}:{str(Dev).zfill(2)}.{str(Fun)}"
                    Device(PfaNumber)

                    if GlobalExistDevice == 1:
                        PfaNumberArray.append(PfaNumber)
                        
                        # Save Vid and Did from string file of the /sys/bus/pci/devices/ to hex digit
                        DigitVendor = int(GlobalVendorId,16)
                        DigitDevice = int(GlobalDeviceId,16)
                        
                        HexVendor[PfaNumberIndex] = str(hex(DigitVendor))
                        HexDevice[PfaNumberIndex] = str(hex(DigitDevice))

                        print(f"Index {str(PfaNumberIndex).zfill(2)} : {PfaNumber} VendorId: {DigitVendor:04X} DeviceId: {DigitDevice:04X}" )

                        PfaNumberIndex += 1

    return PfaNumberIndex,HexVendor,HexDevice                

def TransferOffsetToArray(OffsetVal):
    RowVal = 0
    ColVal = 0

    RowVal = OffsetVal//16
    ColVal = OffsetVal%16

    return RowVal,ColVal

def ReadByDword(HexDumpArray,Row,Col):

    DwordVal = int(HexDumpArray[Row][Col+3],16)<<24 | int(HexDumpArray[Row][Col+2],16)<<16 | int(HexDumpArray[Row][Col+1],16)<<8 | int(HexDumpArray[Row][Col],16)

    return DwordVal

def ReadByWord(HexDumpArray,Row,Col):

    WordVal = int(HexDumpArray[Row][Col+1],16)<<8 | int(HexDumpArray[Row][Col],16)

    return WordVal
    
def ListPciRegContent(HexVendor,HexDevice):
    HexDumpArray = [[0]*16 for i in range(16)]

    LsPciCmd = f"sudo lspci -d {str(HexVendor)}:{str(HexDevice)} -xxx"
    #print("LsPciCmd:",LsPciCmd)
    #RegisterDump = subprocess.run(LsPciCmd, capture_output=True, text=True, shell=True)
    #print(RegisterDump.stdout)
    
    RegisterDump = subprocess.Popen(LsPciCmd, stdout=subprocess.PIPE, text=True, shell=True)
    for RowIndex in range(17):
        LineStr = RegisterDump.stdout.readline()
        if not LineStr:
            break
        if RowIndex == 0:
            print(LineStr[0:100])
        if RowIndex >= 1:
            #print ("LineStr:",LineStr.rstrip())
            #print(LineStr[4:51]) #print 256 hex dump value
            print(LineStr[0:51]) #print offset register dump
            for ColIndex in range(4,52,3):
                #print(LineStr[ColIndex],LineStr[ColIndex+1])
                StrCpy = '0x' + LineStr[ColIndex] + LineStr[ColIndex+1]
                ArrayRow = RowIndex-1
                ArrayCol = (ColIndex-4)//3
                HexDumpArray[ArrayRow][ArrayCol]= hex(int(StrCpy,16))
                #print("HexDumpArray:", HexDumpArray[ArrayRow][ArrayCol])

    return HexDumpArray

def ListPcieRegContent(HexVendor,HexDevice):
    HexDumpArray = [[0]*16 for i in range(256)]

    LsPciCmd = f"sudo lspci -d {str(HexVendor)}:{str(HexDevice)} -xxxx"
    
    RegisterDump = subprocess.Popen(LsPciCmd, stdout=subprocess.PIPE, text=True, shell=True)
    for RowIndex in range(257):
        LineStr = RegisterDump.stdout.readline()
        if(RowIndex >= 17):
            print(LineStr[0:52]) #print offset register dump
            for ColIndex in range(5,52,3):
                #print(LineStr[ColIndex],LineStr[ColIndex+1])
                StrCpy = '0x' + LineStr[ColIndex] + LineStr[ColIndex+1]
                ArrayRow = RowIndex-17
                ArrayCol = (ColIndex-5)//3
                HexDumpArray[ArrayRow][ArrayCol]= hex(int(StrCpy,16))
                #print(f"HexDumpArray[{ArrayRow}][{ArrayCol}]: {HexDumpArray[ArrayRow][ArrayCol]}")

    return HexDumpArray

def CheckBusRelation(HexDumpArray):
    Row0,Col0 = TransferOffsetToArray(OFFSET_PRI_BUS_NUMBER)
    Row1,Col1 = TransferOffsetToArray(OFFSET_SEC_BUS_NUMBER)
    Row2,Col2 = TransferOffsetToArray(OFFSET_SUB_BUS_NUMBER)
    
    print("Primary Bus:",int(HexDumpArray[Row0][Col0],16),"Second Bus:",int(HexDumpArray[Row1][Col1],16),"Subordinate Bus:",int(HexDumpArray[Row2][Col2],16))

def CheckCmdReg(HexDumpArray):
    print("==================================")
    print("Commad Register:")
    Row,Col = TransferOffsetToArray(OFFSET_COMMAND)

    Byte0 = int(HexDumpArray[Row][Col],16)
    Byte1 = int(HexDumpArray[Row][Col+1],16)

    print("IoSpace+" if(Byte0 & BIT0) else "IoSpace-","MemorySpace+" if(Byte0 & BIT1) else "MemorySpace-","BusMaster+" if(Byte0 & BIT2) else "BusMaster-","ParityErrorResponse+" if(Byte0 & BIT6) else "ParityErrorResponse-","SERR+" if(Byte1 & BIT0) else "SERR-")
    print("==================================")

def CheckTypeHeader(HexDumpArray):

    Row,Col = TransferOffsetToArray(OFFSET_HEADER_TYPE)

    Value = HexDumpArray[Row][Col]
    #print("Row:",Row,"Col:",Col,"Value:",Value)
    
    #
    # Check Type0/Type1, Multifunction
    #
    HeaderLayout = int(Value,16) & 0x7F
    MultiFun = (int(Value,16) & 0x80) >> 7

    return HeaderLayout,MultiFun

def CheckBarRegister(HexDumpArray):
    Bar32ValueArray = {}
    Bar64ValueArray = {}

    #SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str(OFFSET_32_BAR0_TYPE)}.l"
    #RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)
    #Bar0Value = int(RegisterDump.stdout,16)
    Row,Col = TransferOffsetToArray(OFFSET_32_BAR0_TYPE)

    Bar0Value = ReadByDword(HexDumpArray,Row,Col)

    if( ( (Bar0Value & BIT3) >> 3) == 1 ):
        Prefetchable = 1
    else:
        Prefetchable = 0

    if (Bar0Value & BIT0) == True:
        print("IO space indicator")
    else:
        if ((Bar0Value & (BIT1 | BIT2)) >> 1) == BIT1:
            print("64 bits Memory space indicator","Prefetchable" if(Prefetchable == 1) else "Non Prefetchable")

            for BarIndex in range(6): 
                #SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str( hex(int(OFFSET_32_BAR0_TYPE,16) + 4*BarIndex))}.l"
                #print("SetPciCmd:",SetPciCmd)
                #RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)
                #BarValue = int(RegisterDump.stdout,16)
                Row,Col = TransferOffsetToArray(OFFSET_32_BAR0_TYPE + 4*BarIndex)
                BarValue = ReadByDword(HexDumpArray,Row,Col)

                Bar64ValueArray[BarIndex] = BarValue

            Bar0Value = Bar64ValueArray[1] << 32 | Bar64ValueArray[0]
            print(f"BAR 0 : 0x{Bar0Value:016X}")
            Bar1Value = Bar64ValueArray[3] << 32 | Bar64ValueArray[2]
            print(f"BAR 1 : 0x{Bar1Value:016X}")
            Bar2Value = Bar64ValueArray[5] << 32 | Bar64ValueArray[4]
            print(f"BAR 2 : 0x{Bar2Value:016X}")

        elif ((Bar0Value & (BIT1 | BIT2)) >> 1) == 0:
            print("32 bits Memory space indicator","Prefetchable" if(Prefetchable == 1) else "Non Prefetchable")
            print(f"BAR 0 : 0x{Bar0Value:08X}")
            Bar32ValueArray[0] = Bar0Value
            for BarIndex in range(1,6): 
                #SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str( hex(int(OFFSET_32_BAR0_TYPE,16) + 4*BarIndex))}.l"
                #print("SetPciCmd:",SetPciCmd)
                #RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)
                #BarValue = int(RegisterDump.stdout,16)
                Row,Col = TransferOffsetToArray(OFFSET_32_BAR0_TYPE + 4*BarIndex)
                BarValue = ReadByDword(HexDumpArray,Row,Col)

                Bar32ValueArray[BarIndex] = BarValue
                print(f"BAR {BarIndex} : 0x{Bar32ValueArray[BarIndex]:08X}")
                
def PcieBaseFindCapId(HexDumpArray,CapId):
    
    Row,Col = TransferOffsetToArray(OFFSET_STATUS)

    # Check PCI status capability
    if(int(HexDumpArray[Row][Col],16) & PCI_STATUS_CAP == 0):
        return 0
    else:
        #
        # Check the header layout to determine the Offset of Capabilities Pointer Register
        #
        Row,Col = TransferOffsetToArray(OFFSET_HEADER_TYPE)
        if(int(HexDumpArray[Row][Col],16) & HEADER_LAYOUT_CODE == HEADER_TYPE_CARDBUS_BRIDGE):
            # If CardBus bridge, start at Offset 0x14
            CapHeaderOffset = PCI_CARD_BUS_BRIDGE_CAP_PTR
        else:
            # Otherwise, start at Offset 0x34
            CapHeaderOffset = PCI_CAP_PTR
        #
        # Get Capability Header, A pointer value of 00h is used to indicate the last capability in the list.
        #
        CapHeaderId = 0
        Row,Col = TransferOffsetToArray(CapHeaderOffset)

        # The bottom two bits are Reserved and must be set to 00b
        CapHeaderOffset = int(HexDumpArray[Row][Col],16) & ~(BIT1|BIT2)

        while (CapHeaderOffset != 0 and CapHeaderId != 0xFF):
            
            Row,Col = TransferOffsetToArray(CapHeaderOffset)
            CapHeaderId = int(HexDumpArray[Row][Col],16) & 0xff
            if (CapHeaderId == CapId):
                return CapHeaderOffset
            else:
                Col += 1
                CapHeaderOffset = int(HexDumpArray[Row][Col],16)
    return 0

def PcieExtBaseFindCapId(HexDumpArray,CapId):
    PcieExtOffset = OFFSET_PCIE_EXT_CAP_HEADER
    
    Row,Col = TransferOffsetToArray(PcieExtOffset - PcieExtOffset)
    CapVal = ReadByDword(HexDumpArray,Row,Col)
    
    while( (CapVal != 0xffffffff) and PcieExtOffset !=0 ):

        Row,Col = TransferOffsetToArray(PcieExtOffset - OFFSET_PCIE_EXT_CAP_HEADER)
        CapVal = ReadByWord(HexDumpArray,Row,Col)

        if( (CapVal & 0xffff) == CapId ):
            ArrayIndex = PcieExtOffset - OFFSET_PCIE_EXT_CAP_HEADER
            Row,Col = TransferOffsetToArray(ArrayIndex)
            CapVal = ReadByDword(HexDumpArray,Row,Col)
            return PcieExtOffset
        
        # Bit[20:31]:Next Cap Offset
        # Bit[16:19]:Cap Version
        # Bit[0:18]:PCIe Extended Cap Id
        PcieExtOffset -= OFFSET_PCIE_EXT_CAP_HEADER
        Row,Col = TransferOffsetToArray(PcieExtOffset)
        Col += 2
        PcieExtOffset = ( ReadByWord(HexDumpArray,Row,Col) & 0xFFF0 ) >> 4

    return 0

def GetPcieCapRegister(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Pcie Capibilities:")
    PcieCapOffset = CapHeaderOffset + OFFSET_PCIE_CAP
    Row,Col = TransferOffsetToArray(PcieCapOffset)
    PcieCapValue = ReadByWord(HexDumpArray,Row,Col)

    DeviceTypeReg = ( PcieCapValue & (BIT4 | BIT5 | BIT6 | BIT7 ) ) >> 4

    match DeviceTypeReg:
        case 0:
            print("PCI Express Endpoint")
        case 1:
            print("Legacy PCI Express Endpoint")
        case 9:
            print("RCiEP")
        case 10:
            print("Root Complex Event Collector")
        case 4:
            print("Root Port of PCI Express Root Complex")
        case 5:
            print("Upstream Port of PCI Express Switch")
        case 6:
            print("Downstream Port of PCI Express Switch")
        case 7:
            print("PCI Express to PCI/PCI-X Bridge")
        case 8:
            print("PCI/PCI-X to PCI Express Bridge")

    SlotImplementReg = ( PcieCapValue & BIT8 ) >> 8
    print("Slot Implemented+" if (SlotImplementReg == 1) else "Slot Implemented-" )

    IntMsgNum = ( PcieCapValue & (BIT9 | BIT10 | BIT11 | BIT12 | BIT13 ) ) >> 9
    print("IntMsgNum:",IntMsgNum)

def GetDeviceCap(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Device Capibilities:")
    DeviceCapOffset = CapHeaderOffset + OFFSET_DEVICE_CAP
    Row,Col = TransferOffsetToArray(DeviceCapOffset)
    DeviceCapValue = ReadByDword(HexDumpArray,Row,Col)

    MaxPayloadSize = DeviceCapValue & ( BIT0 | BIT1 | BIT2)
    match MaxPayloadSize:
        case 0:
            print("128 bytes max payload size")
        case 1:
            print("256 bytes max payload size")
        case 2:
            print("512 bytes max payload size")
        case 3:
            print("1024 bytes max payload size")
        case 4:
            print("2048 bytes max payload size")
        case 5:
            print("4096 bytes max payload size")
        case 6:
            print("Reserved")
        case 7:
            print("Reserved")

    PhantomFun = (DeviceCapValue & ( BIT3 | BIT4)) >> 3
    print("PhantomFun:",PhantomFun)

    L0Latency = (DeviceCapValue & ( BIT6 | BIT7 | BIT8)) >> 6
    match L0Latency:
        case 0:
            print("L0Latency:Maximum of 64 ns")
        case 1:
            print("L0Latency:Maximum of 128 ns")
        case 2:
            print("L0Latency:Maximum of 256 ns")
        case 3:
            print("L0Latency:Maximum of 512 ns")
        case 4:
            print("L0Latency:Maximum of 1 us")
        case 5:
            print("L0Latency:Maximum of 2 us")
        case 6:
            print("L0Latency:Maximum of 4 us")
        case 7:
            print("No limit")

    L1Latency = (DeviceCapValue & ( BIT9 | BIT10 | BIT11)) >> 9
    match L1Latency:
        case 0:
            print("L1Latency:Maximum of 1 us")
        case 1:
            print("L1Latency:Maximum of 2 us")
        case 2:
            print("L1Latency:Maximum of 4 us")
        case 3:
            print("L1Latency:Maximum of 8 us")
        case 4:
            print("L1Latency:Maximum of 16 us")
        case 5:
            print("L1Latency:Maximum of 32 us")
        case 6:
            print("L1Latency:Maximum of 64 us")
        case 7:
            print("No limit")

def GetDeviceControl(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Device Control:")
    DeviceControlOffset = CapHeaderOffset + OFFSET_DEVICE_CONTROL
    Row,Col = TransferOffsetToArray(DeviceControlOffset)
    DeviceControlValue = ReadByWord(HexDumpArray,Row,Col)

    print("CorrectableErrorReporting+" if(DeviceControlValue & BIT0) else "CorrectableErrorReporting-", "NonFatalErrorReporting+" if(DeviceControlValue & BIT1) else "NonFatalErrorReporting-","FatalErrorReporting+" if(DeviceControlValue & BIT2) else "FatalErrorReporting-","UnsupportedRequestReporting+" if(DeviceControlValue & BIT3) else "UnsupportedRequestReporting-", "AuxPowerEnabled+" if(DeviceControlValue & BIT10) else "AuxPowerEnabled-")
        
    MaxPayloadSize = ( DeviceControlValue & ( BIT5 | BIT6 | BIT7) ) >> 5
    match MaxPayloadSize:
        case 0:
            print("128 bytes max payload size")
        case 1:
            print("256 bytes max payload size")
        case 2:
            print("512 bytes max payload size")
        case 3:
            print("1024 bytes max payload size")
        case 4:
            print("2048 bytes max payload size")
        case 5:
            print("4096 bytes max payload size")
        case 6:
            print("Reserved")
        case 7:
            print("Reserved")

    MaxReadRequest = ( DeviceControlValue & ( BIT12 | BIT13 | BIT14) ) >> 12
    match MaxReadRequest:
        case 0:
            print("128 bytes max Read Request size")
        case 1:
            print("256 bytes max Read Request size")
        case 2:
            print("512 bytes max Read Request size")
        case 3:
            print("1024 bytes max Read Request size")
        case 4:
            print("2048 bytes max Read Request size")
        case 5:
            print("4096 bytes max Read Request size")
        case 6:
            print("Reserved")
        case 7:
            print("Reserved")

def GetDeviceStatus(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Device Status:")
    DeviceStatusOffset = CapHeaderOffset + OFFSET_DEVICE_STATUS
    Row,Col = TransferOffsetToArray(DeviceStatusOffset)
    DeviceStatusValue = ReadByWord(HexDumpArray,Row,Col)    

    print("CorrectableErrorDetected+" if(DeviceStatusValue & BIT0) else "CorrectableErrorDetected-", "NonFatalErrorDetected+" if(DeviceStatusValue & BIT1) else "NonFatalErrorDetected-", "FatalErrorDetected+" if(DeviceStatusValue & BIT2) else "FatalErrorDetected-", "UnsupportedErrorDetected+" if(DeviceStatusValue & BIT3) else "UnsupportedErrorDetected-", "AuxPowerDetected+" if(DeviceStatusValue & BIT4) else "AuxPowerDetected-","TransactionsPending+" if(DeviceStatusValue & BIT5) else "TransactionsPending-")                    

def GetLinkCap(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Link Capibilities:")
    LinkCapOffset = CapHeaderOffset + OFFSET_LINK_CAPABILITY
    Row,Col = TransferOffsetToArray(LinkCapOffset)
    LinkCapValue = ReadByDword(HexDumpArray,Row,Col)
    # print(f"LinkCapValue:{LinkCapValue:04X}")

    MaxLinkSpeedReg = LinkCapValue & (BIT0 | BIT1 | BIT2 | BIT3 )

    match MaxLinkSpeedReg:
        case 1:
            print("Maximum Link Speed: 2.5 GT/s")
        case 2:
            print("Maximum Link Speed: 5.0 GT/s")
        case 3:
            print("Maximum Link Speed: 8.0 GT/s")
        case 4:
            print("Maximum Link Speed: 16.0 GT/s")
        case 5:
            print("Maximum Link Speed: 32.0 GT/s")     
        case 6:
            print("Maximum Link Speed: 64.0 GT/s")

    MaxLinkWidthReg = (LinkCapValue & ( BIT4|BIT5|BIT6|BIT7|BIT8|BIT9) ) >> 4

    match MaxLinkWidthReg:
        case 1:
            print("Maximum Link Width: x1")
        case 2:
            print("Maximum Link Width: x2")
        case 4:
            print("Maximum Link Width: x4")
        case 8:
            print("Maximum Link Width: x8")
        case 16:
            print("Maximum Link Width: x16")     
        case 32:
            print("Maximum Link Width: x32")       

    ASPMSupport = (LinkCapValue & (BIT10 | BIT11)) >> 10 
    match ASPMSupport:
        case 0:
            print("No ASPM Support")
        case 1:
            print("L0s Supported")
        case 2:
            print("L1 Supported")
        case 3:
            print("L0s and L1 Supported")

    L0ExitLatency = (LinkCapValue & (BIT12 | BIT13 | BIT14)) >> 12
    match L0ExitLatency:
        case 0:
            print("L0ExitLatency: Less than 64 ns")
        case 1:
            print("L0ExitLatency: 64 ns to less than 128 ns")     
        case 2:
            print("L0ExitLatency: 128 ns to less than 256 ns")
        case 3:
            print("L0ExitLatency: 256 ns to less than 512 ns")
        case 4:
            print("L0ExitLatency: 512 ns to less than 1 μs")
        case 5:
            print("L0ExitLatency: 1 μs to less than 2 μs")
        case 6:
            print("L0ExitLatency: 2 μs-4 μs")
        case 7:
            print("L0ExitLatency: More than 4 μs")

    L1ExitLatency = (LinkCapValue & (BIT15 | BIT16 | BIT17)) >> 15 
    match L1ExitLatency:                              
        case 0:
            print("L1ExitLatency: Less than 1 ns")
        case 1:
            print("L1ExitLatency: 1 μs to less than 2 μs")     
        case 2:
            print("L1ExitLatency: 2 μs to less than 4 μs")
        case 3:
            print("L1ExitLatency: 4 μs to less than 8 μs")
        case 4:
            print("L1ExitLatency: 8 μs to less than 16 μs")
        case 5:
            print("L1ExitLatency: 16 μs to less than 32 μs")
        case 6:
            print("L1ExitLatency: 32 μs-64 μs")
        case 7:
            print("L1ExitLatency: More than 64 μs")

    ClockPowerMgmt = (LinkCapValue & BIT18) >> 18 
    SurpriseDownErrorReport = (LinkCapValue & BIT19) >> 19
    DataLinkLayerActiveReport = (LinkCapValue & BIT20) >> 20
    LinkBandWidthNotification = (LinkCapValue & BIT21) >> 21
    AspmOptionCom = (LinkCapValue & BIT22) >> 22

    print("ClockPowerMgmt+" if(ClockPowerMgmt) else "ClockPowerMgmt-", "SurpriseDownErrorReport+" if(SurpriseDownErrorReport) else "SurpriseDownErrorReport-", "DataLinkLayerActiveReport+" if(DataLinkLayerActiveReport) else "DataLinkLayerActiveReport-", "LinkBandWidthNotification+" if(LinkBandWidthNotification) else "LinkBandWidthNotification-", "AspmOptionCom+" if(AspmOptionCom) else "AspmOptionCom-")

def GetLinkControl(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Link Control:")
    LinkControlOffset = CapHeaderOffset + OFFSET_LINK_CONTROL
    Row,Col = TransferOffsetToArray(LinkControlOffset)
    LinkControlValue = ReadByWord(HexDumpArray,Row,Col)

    AspmControl = (LinkControlValue & (BIT0 | BIT1)) 
    ReadCompletionBoundary = (LinkControlValue & BIT3) >> 3
    LinkDisable = (LinkControlValue & BIT4) >> 4
    CommonClock = (LinkControlValue & BIT5) >> 5
    ExtendSynch = (LinkControlValue & BIT7) >> 7
    ClockPowerMgmt = (LinkControlValue & BIT8) >> 8

    match AspmControl:
        case 0:
            print("AspmControl: Disabled")
        case 1:
            print("AspmControl: L0s Entry Enabled")
        case 2:
            print("AspmControl: L1 Entry Enabled")
        case 3:
            print("AspmControl: L0s and L1 Entry Enabled")

    print("ReadCompletionBoundary: 128 byte" if(ReadCompletionBoundary) else "ReadCompletionBoundary: 64 byte", "LinkDisable+" if(LinkDisable) else "LinkDisable-", "CommonClock+" if(CommonClock) else "CommonClock-","ExtendSynch+" if(ExtendSynch) else "ExtendSynch-", "ClockPowerMgmt+" if(ClockPowerMgmt) else "ClockPowerMgmt-")                        

def GetLinkStatus(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Link Status:")
    LinkStatusOffset = CapHeaderOffset + OFFSET_LINK_STATUS
    Row,Col = TransferOffsetToArray(LinkStatusOffset)
    LinkStatusValue = ReadByWord(HexDumpArray,Row,Col)

    CurrentLinkSpeedReg = LinkStatusValue & (BIT0 | BIT1 | BIT2 | BIT3)

    match CurrentLinkSpeedReg:
        case 1:
            print("Current Link Speed: 2.5 GT/s")
        case 2:
            print("Current Link Speed: 5.0 GT/s")
        case 3:
            print("Current Link Speed: 8.0 GT/s")
        case 4:
            print("Current Link Speed: 16.0 GT/s")
        case 5:
            print("Current Link Speed: 32.0 GT/s")     
        case 6:
            print("Current Link Speed: 64.0 GT/s")

    CurrentLinkWidthReg = (LinkStatusValue & (BIT4 | BIT5 | BIT6 | BIT7 | BIT8 | BIT9 ) ) >> 4

    match CurrentLinkWidthReg:
        case 1:
            print("Current Link Width: x1")
        case 2:
            print("Current Link Width: x2")
        case 4:
            print("Current Link Width: x4")
        case 8:
            print("Current Link Width: x8")
        case 16:
            print("Current Link Width: x16")     
        case 32:
            print("Current Link Width: x32")

    LinkTrain = (LinkStatusValue & BIT11) >> 11
    SlotClock = (LinkStatusValue & BIT12) >> 12
    DataLinkActive = (LinkStatusValue & BIT13) >> 13
    BandWidthMgmt = (LinkStatusValue & BIT14) >> 14
    AutonomousBandWidthMgmt = (LinkStatusValue & BIT15) >> 15

    print("LinkTrain+" if(LinkTrain) else "LinkTrain-", "SlotClock+" if(SlotClock) else "SlotClock-", "DataLinkActive+" if(DataLinkActive) else "DataLinkActive-", "BandWidthMgmt+" if(BandWidthMgmt) else "BandWidthMgmt-", "AutonomousBandWidthMgmt+" if(AutonomousBandWidthMgmt) else "AutonomousBandWidthMgmt-")

def CheckUEStatus(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Uncorrectable Error Status:")
    
    UEStatusOffset = CapHeaderOffset + OFFSET_UE_STATUS
    Row,Col = TransferOffsetToArray(UEStatusOffset)
    UEStatusValue = ReadByDword(HexDumpArray,Row,Col)
    print(f"UEStatusValue:{UEStatusValue:08X}")

    DataLinkProErr = (UEStatusValue & BIT4) >> 4
    SurpriseDownErr = (UEStatusValue & BIT5) >> 5
    PoisonTLPReceived = (UEStatusValue & BIT12) >> 12
    CompleteTimeOut = (UEStatusValue & BIT14) >> 14
    CompleterAbort = (UEStatusValue & BIT15) >> 15
    UnexpectCompletion = (UEStatusValue & BIT16) >> 16
    ReceiverOverflow = (UEStatusValue & BIT17) >> 17
    MalformedTLP = (UEStatusValue & BIT18) >> 18
    ECRCErr = (UEStatusValue & BIT19) >> 19
    UnsupportRequest = (UEStatusValue & BIT20) >> 20
    MCBlockTLP = (UEStatusValue & BIT23) >> 23
    AtomicOPEgressBlock = (UEStatusValue & BIT24) >> 24
    DMWrRequestEgressBlock = (UEStatusValue & BIT27) >> 27
    IDECheckFailed = (UEStatusValue & BIT28) >> 28
    TLPTranslationEgressBlock = (UEStatusValue & BIT31) >> 31

    print("DataLinkProErr+" if(DataLinkProErr) else "DataLinkProErr-", "SurpriseDownErr+" if(SurpriseDownErr) else "SurpriseDownErr-", "PoisonTLPReceived+" if(PoisonTLPReceived) else "PoisonTLPReceived-", "CompleteTimeOut+" if(CompleteTimeOut) else "CompleteTimeOut-", "CompleterAbort+" if(CompleterAbort) else "CompleterAbort-", "UnexpectCompletion+" if(UnexpectCompletion) else "UnexpectCompletion-")
    print("ReceiverOverflow+" if(ReceiverOverflow) else "ReceiverOverflow-", "MalformedTLP+" if(MalformedTLP) else "MalformedTLP-", "ECRCErr+" if(ECRCErr) else "ECRCErr-", "UnsupportRequest+" if(UnsupportRequest) else "UnsupportRequest-", "MCBlockTLP+" if(MCBlockTLP) else "MCBlockTLP-", "AtomicOPEgressBlock+" if(AtomicOPEgressBlock) else "AtomicOPEgressBlock-", "DMWrRequestEgressBlock+" if(DMWrRequestEgressBlock) else "DMWrRequestEgressBlock-")
    print("IDECheckFailed+" if(IDECheckFailed) else "IDECheckFailed-", "TLPTranslationEgressBlock+" if(TLPTranslationEgressBlock) else "TLPTranslationEgressBlock-")
"""
    def GetVendor(self, pciid:str):
        self.__vendor = f"{self.__base}/vendor"
        with open(self.__vendor,'r') as file:
            VendorId = file.read()
            print("VendorId:",VendorId)                    
"""        


        
    