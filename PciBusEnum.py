import os
import subprocess
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

# Pci configuration space offset
OFFSET_COMMAND = 0x4            # Command offset
OFFSET_STATUS = 0x6             # Status offset
OFFSET_LINK_CAPABILITY = 0xC    # Link capability offset
OFFSET_HEADER_TYPE = 0xE        # Header type offset
OFFSET_32_BAR0_TYPE = 0x10      # 32 bit BAR0 offset
OFFSET_LINK_STATUS = 0x12       # Link status offset
OFFSET_PRI_BUS_NUMBER = 0x18    # Primary Bus offset
OFFSET_SEC_BUS_NUMBER = 0x19    # Second Bus offset
OFFSET_SUB_BUS_NUMBER = 0x1A    # Subordinate Bus offset

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

    WordVal = int(HexDumpArray[Row][Col+1],16)<<16 | int(HexDumpArray[Row][Col],16)

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

def GetLinkCap(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Link Cap:")
    LinkCapOffset = CapHeaderOffset + OFFSET_LINK_CAPABILITY
    Row,Col = TransferOffsetToArray(LinkCapOffset)
    LinkCapValue = ReadByWord(HexDumpArray,Row,Col)

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

def GetLinkStatus(HexDumpArray,CapHeaderOffset):
    print("==================================")
    print("Link Status:")
    LinkStatusOffset = CapHeaderOffset + OFFSET_LINK_STATUS
    Row,Col = TransferOffsetToArray(LinkStatusOffset)
    CurrentLinkSpeedReg = int(HexDumpArray[Row][Col],16) & 0xf

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

    CurrentLinkWidthReg = (int(HexDumpArray[Row][Col],16) & 0x3f0) >> 4

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

"""
    def GetVendor(self, pciid:str):
        self.__vendor = f"{self.__base}/vendor"
        with open(self.__vendor,'r') as file:
            VendorId = file.read()
            print("VendorId:",VendorId)                    
"""        


        
    