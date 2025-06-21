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
BIT1 = 2
BIT2 = 4
BIT3 = 8
BIT4 = 16
BIT5 = 32

# Pci configuration space offset
OFFSET_HEADER_TYPE = f"0xE" # Header type offset
OFFSET_32_BAR0_TYPE = f"0x10" # 32 bit BAR0 offset

OFFSET_64_BAR1_TYPE = f"0x18" # 64 bit BAR1 offset
OFFSET_64_BAR2_TYPE = f"0x20" # 64 bit BAR2 offset

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

def ListPciRegContent(HexVendor,HexDevice):
    LsPciCmd = f"sudo lspci -d {str(HexVendor)}:{str(HexDevice)} -xxx"
    #print("LsPciCmd:",LsPciCmd)
    RegisterDump = subprocess.run(LsPciCmd, capture_output=True, text=True, shell=True)
    print(RegisterDump.stdout)

def CheckTypeHeader(HexVendor,HexDevice):
    SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str(OFFSET_HEADER_TYPE)}.b" 
    #print("SetPciCmd:",SetPciCmd)  
    RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)       
    #print("HeaderTypeValue:",RegisterDump.stdout)
    #
    # Check Type0/Type1, Multifunction
    #
    HeaderLayout = int(RegisterDump.stdout) & 0x7F
    MultiFun = (int(RegisterDump.stdout) & 0x80) >> 7
    #print("HeaderLayout:",HeaderLayout,"MultiFun:",MultiFun)
    return HeaderLayout,MultiFun

def CheckBarRegister(HexVendor,HexDevice):
    Bar32ValueArray = {}
    Bar64ValueArray = {}

    SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str(OFFSET_32_BAR0_TYPE)}.l"
    RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)
    Bar0Value = int(RegisterDump.stdout,16)

    if (Bar0Value & BIT0) == True:
        print("IO space indicator")
    else:
        if ((Bar0Value & (BIT1 | BIT2)) >> 1) == BIT1:
            print("64 bits Memory space indicator")

            for BarIndex in range(6): 
                SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str( hex(int(OFFSET_32_BAR0_TYPE,16) + 4*BarIndex))}.l"
                #print("SetPciCmd:",SetPciCmd)
                RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)
                BarValue = int(RegisterDump.stdout,16)
                Bar64ValueArray[BarIndex] = BarValue

            Bar0Value = f"{str(hex(Bar64ValueArray[1]))} {str(hex(Bar64ValueArray[0]))}"
            print("BAR 0 :",Bar0Value)
            Bar1Value = f"{str(hex(Bar64ValueArray[3]))} {str(hex(Bar64ValueArray[2]))}"
            print("BAR 1 :",Bar1Value)
            Bar2Value = f"{str(hex(Bar64ValueArray[5]))} {str(hex(Bar64ValueArray[4]))}"
            print("BAR 2 :",Bar2Value)

        elif ((Bar0Value & (BIT1 | BIT2)) >> 1) == 0:
            print("32 bits Memory space indicator")
            print("BAR 0 :",hex(Bar0Value))
            Bar32ValueArray[0] = Bar0Value
            for BarIndex in range(1,6): 
                SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str( hex(int(OFFSET_32_BAR0_TYPE,16) + 4*BarIndex))}.l"
                #print("SetPciCmd:",SetPciCmd)
                RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)
                BarValue = int(RegisterDump.stdout,16)
                Bar32ValueArray[BarIndex] = BarValue
                print("BAR",BarIndex,":",hex(Bar32ValueArray[BarIndex]))
                
         
"""
    def GetVendor(self, pciid:str):
        self.__vendor = f"{self.__base}/vendor"
        with open(self.__vendor,'r') as file:
            VendorId = file.read()
            print("VendorId:",VendorId)                    
"""        


        
    