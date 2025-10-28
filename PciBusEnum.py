import os
import subprocess
import CommonLib

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

def Device(PfaNumber):

    Path = "/sys/bus/pci/devices/"
    VendorId = 0
    DeviceId = 0

    FilePath = os.path.join(Path, str(PfaNumber))
    PathVendor = f"{FilePath}/vendor"
    PathDevice = f"{FilePath}/device"

    if not os.access(FilePath, os.F_OK):
        ExistDevice = 0
    else:
        ExistDevice = 1

        # Print VendorId
        with open(PathVendor,'r') as file:
            VendorId = file.read()
            
        # Print DeviceId
        with open(PathDevice,'r') as file:
            DeviceId = file.read()

    return ExistDevice,VendorId,DeviceId

def PciEnumOperation():
    PfaNumberArray = []
    HexVendor = {}
    HexDevice = {}

    PfaNumberIndex = 0

    for Segment in range(8):
        for Bus in range(256):
            for Dev in range(32):
                for Fun in range(8):
                    # ex: PfaNumber = 0007:00:01.0
                    PfaNumber = f"{str(Segment).zfill(4)}:{str(Bus).zfill(2)}:{str(Dev).zfill(2)}.{str(Fun)}"
                    ExistDevice,VendorId,DeviceId = Device(PfaNumber)

                    if ExistDevice == 1:
                        PfaNumberArray.append(PfaNumber)
                        
                        # Save Vid and Did from string file of the /sys/bus/pci/devices/ to hex digit
                        DigitVendor = int(VendorId,16)
                        DigitDevice = int(DeviceId,16)
                        
                        HexVendor[PfaNumberIndex] = str(hex(DigitVendor))
                        HexDevice[PfaNumberIndex] = str(hex(DigitDevice))
                        
                        LsPciCmd = f"sudo lspci -d {str(HexVendor[PfaNumberIndex])}:{str(HexDevice[PfaNumberIndex])}"
                        Line0Str = subprocess.Popen(LsPciCmd, stdout=subprocess.PIPE, text=True, shell=True)
                        Line0Str = Line0Str.stdout.readline()
                        Line0Str = Line0Str.strip()

                        print(f"({str(PfaNumberIndex).zfill(2)}) : VID: 0x{DigitVendor:04X} DID: 0x{DigitDevice:04X} | {Line0Str}" )

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
            print("    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
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
    
    print(f"[0x{OFFSET_PRI_BUS_NUMBER:02X} 01]Primary Bus: {int(HexDumpArray[Row0][Col0],16)} [0x{OFFSET_SEC_BUS_NUMBER:02X} 01]Second Bus: {int(HexDumpArray[Row1][Col1],16)} [0x{OFFSET_SUB_BUS_NUMBER:02X} 01]Subordinate Bus: {int(HexDumpArray[Row2][Col2],16)}" )

def CheckCmdReg(HexDumpArray):
    print("==================================")
    
    Row,Col = TransferOffsetToArray(OFFSET_COMMAND)

    Byte0 = int(HexDumpArray[Row][Col],16)
    Byte1 = int(HexDumpArray[Row][Col+1],16)
    Val = Byte1 << 8 | Byte0
    print(f"[0x04 02]Commad Register:0x{Val:04X}")

    print("(Bit 0)IoSpace+" if(Byte0 & CommonLib.BIT0) else "(Bit 0)IoSpace-","(Bit 1)MemorySpace+" if(Byte0 & CommonLib.BIT1) else "(Bit 1)MemorySpace-","(Bit 2)BusMaster+" if(Byte0 & CommonLib.BIT2) else "(Bit 2)BusMaster-","(Bit 6)ParityErrorResponse+" if(Byte0 & CommonLib.BIT6) else "(Bit 6)ParityErrorResponse-","(Bit 8)SERR+" if(Byte1 & CommonLib.BIT0) else "(Bit 8)SERR-")
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

def CheckBarRegister(HexDumpArray,DeviceType):
    Bar32ValueArray = {}
    Bar64ValueArray = {}

    #SetPciCmd = f"sudo setpci -d {str(HexVendor)}:{str(HexDevice)} {str(OFFSET_32_BAR0_TYPE)}.l"
    #RegisterDump = subprocess.run(SetPciCmd, capture_output=True, text=True, shell=True)
    #Bar0Value = int(RegisterDump.stdout,16)
    Row,Col = TransferOffsetToArray(OFFSET_32_BAR0_TYPE)

    Bar0Value = ReadByDword(HexDumpArray,Row,Col)

    if( ( (Bar0Value & CommonLib.BIT3) >> 3) == 1 ):
        Prefetchable = 1
    else:
        Prefetchable = 0

    if (Bar0Value & CommonLib.BIT0) == True:
        print("[0x10]Base Address Registers\n(Bit 0)1 IO space indicator")
    else:
        if (DeviceType == 0):
            if ((Bar0Value & (CommonLib.BIT1 | CommonLib.BIT2)) >> 1) == CommonLib.BIT1:
                print(f"[0x10]Base Address Registers\n(Bit 0)0 Memory space indicator\n(Bit 1:2)10 64 bits\n(Bit 3){Prefetchable:02b}")
                print("Prefetchable" if(Prefetchable == 1) else "Non Prefetchable")

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

            elif ((Bar0Value & (CommonLib.BIT1 | CommonLib.BIT2)) >> 1) == 0:
                print(f"[0x10]Base Address Registers\n(Bit 0)0 Memory space indicator\n(Bit 1:2)00 32 bits\n(Bit 3){Prefetchable:02b}")
                print("Prefetchable" if(Prefetchable == 1) else "Non Prefetchable")
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

        else: #if (DeviceType == 0):
            if ((Bar0Value & (CommonLib.BIT1 | CommonLib.BIT2)) >> 1) == CommonLib.BIT1:
                print(f"[0x10]Base Address Registers\n(Bit 0)0 Memory space indicator\n(Bit 1:2)10 64 bits\n(Bit 3){Prefetchable:02b}")
                print("Prefetchable" if(Prefetchable == 1) else "Non Prefetchable")
                print(f"BAR 0 : 0x{Bar0Value:08X}")
                Row,Col = TransferOffsetToArray(OFFSET_32_BAR0_TYPE + 4)
                BarValue = ReadByDword(HexDumpArray,Row,Col)

                Bar32ValueArray[1] = BarValue
                print(f"BAR 1 : 0x{Bar32ValueArray[1]:08X}")
            elif ((Bar0Value & (CommonLib.BIT1 | CommonLib.BIT2)) >> 1) == 0:
                print(f"[0x10]Base Address Registers\n(Bit 0)0 Memory space indicator\n(Bit 1:2)00 32 bits\n(Bit 3){Prefetchable:02b}")
                print("Prefetchable" if(Prefetchable == 1) else "Non Prefetchable")
                print(f"BAR 0 : 0x{Bar0Value:08X}")
                
                Row,Col = TransferOffsetToArray(OFFSET_32_BAR0_TYPE + 4)
                BarValue = ReadByDword(HexDumpArray,Row,Col)

                Bar32ValueArray[1] = BarValue
                print(f"BAR 1 : 0x{Bar32ValueArray[1]:08X}")
                
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
        CapHeaderOffset = int(HexDumpArray[Row][Col],16) & ~(CommonLib.BIT1 | CommonLib.BIT2)

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

    PcieCapOffset = CapHeaderOffset + OFFSET_PCIE_CAP
    Row,Col = TransferOffsetToArray(PcieCapOffset)
    PcieCapValue = ReadByWord(HexDumpArray,Row,Col)

    print(f"[0x{PcieCapOffset:02X} 02]Pcie Capibilities:0x{PcieCapValue:04X}")

    print(f"(Bit 4:7)Device/Port Type:")
    DeviceTypeReg = ( PcieCapValue & (CommonLib.BIT4 | CommonLib.BIT5 | CommonLib.BIT6 | CommonLib.BIT7 ) ) >> 4

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

    SlotImplementReg = ( PcieCapValue & CommonLib.BIT8 ) >> 8
    print("(Bit 8)")
    print("Slot Implemented+" if (SlotImplementReg == 1) else "Slot Implemented-" )

    IntMsgNum = ( PcieCapValue & (CommonLib.BIT9 | CommonLib.BIT10 | CommonLib.BIT11 | CommonLib.BIT12 | CommonLib.BIT13 ) ) >> 9
    print("(Bit 9:13)")
    print("IntMsgNum:",IntMsgNum)

def GetDeviceCap(HexDumpArray,CapHeaderOffset):
    print("==================================")

    DeviceCapOffset = CapHeaderOffset + OFFSET_DEVICE_CAP
    Row,Col = TransferOffsetToArray(DeviceCapOffset)
    DeviceCapValue = ReadByDword(HexDumpArray,Row,Col)

    print(f"[0x{DeviceCapOffset:02X} 04]Device Capibilities:0x{DeviceCapValue:04X}")

    MaxPayloadSize = DeviceCapValue & ( CommonLib.BIT0 | CommonLib.BIT1 | CommonLib.BIT2)
    print("(Bit 0:2)Max Payload Size:")
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

    PhantomFun = (DeviceCapValue & ( CommonLib.BIT3 | CommonLib.BIT4)) >> 3
    print("(Bit 3:4)Phantom Functions:")
    print("PhantomFun:",PhantomFun)

    print("(Bit 6:8)Endpoint L0s Acceptable Latency:")
    L0Latency = (DeviceCapValue & ( CommonLib.BIT6 | CommonLib.BIT7 | CommonLib.BIT8)) >> 6
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

    print("(Bit 9:11)Endpoint L1 Acceptable Latency:")
    L1Latency = (DeviceCapValue & ( CommonLib.BIT9 | CommonLib.BIT10 | CommonLib.BIT11)) >> 9
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
    
    DeviceControlOffset = CapHeaderOffset + OFFSET_DEVICE_CONTROL
    Row,Col = TransferOffsetToArray(DeviceControlOffset)
    DeviceControlValue = ReadByWord(HexDumpArray,Row,Col)
    print(f"[0x{DeviceControlOffset:02X} 02]Device Control:0x{DeviceControlValue:04X}")

    print("(Bit 0)CorrectableErrorReporting+" if(DeviceControlValue & CommonLib.BIT0) else "(Bit 0)CorrectableErrorReporting-", "(Bit 1)NonFatalErrorReporting+" if(DeviceControlValue & CommonLib.BIT1) else "(Bit 1)NonFatalErrorReporting-","(Bit 2)FatalErrorReporting+" if(DeviceControlValue & CommonLib.BIT2) else "(Bit 2)FatalErrorReporting-","(Bit 3)UnsupportedRequestReporting+" if(DeviceControlValue & CommonLib.BIT3) else "(Bit 3)UnsupportedRequestReporting-", "(Bit 10)AuxPowerEnabled+" if(DeviceControlValue & CommonLib.BIT10) else "(Bit 10)AuxPowerEnabled-")
        
    MaxPayloadSize = ( DeviceControlValue & ( CommonLib.BIT5 | CommonLib.BIT6 | CommonLib.BIT7) ) >> 5
    print("(Bit 5:7)Max Payload Size:")
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

    print("(Bit 12:14)Max Read Request Size:")
    MaxReadRequest = ( DeviceControlValue & ( CommonLib.BIT12 | CommonLib.BIT13 | CommonLib.BIT14) ) >> 12
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
    
    DeviceStatusOffset = CapHeaderOffset + OFFSET_DEVICE_STATUS
    Row,Col = TransferOffsetToArray(DeviceStatusOffset)
    DeviceStatusValue = ReadByWord(HexDumpArray,Row,Col)    
    print(f"[0x{DeviceStatusOffset:02X} 02]Device Status:0x{DeviceStatusValue:04X}")

    print("(Bit 0)CorrectableErrorDetected+" if(DeviceStatusValue & CommonLib.BIT0) else "(Bit 0)CorrectableErrorDetected-", "(Bit 1)NonFatalErrorDetected+" if(DeviceStatusValue & CommonLib.BIT1) else "(Bit 1)NonFatalErrorDetected-", "(Bit 2)FatalErrorDetected+" if(DeviceStatusValue & CommonLib.BIT2) else "(Bit 2)FatalErrorDetected-", "(Bit 3)UnsupportedErrorDetected+" if(DeviceStatusValue & CommonLib.BIT3) else "(Bit 3)UnsupportedErrorDetected-", "(Bit 4)AuxPowerDetected+" if(DeviceStatusValue & CommonLib.BIT4) else "(Bit 4)AuxPowerDetected-","(Bit 5)TransactionsPending+" if(DeviceStatusValue & CommonLib.BIT5) else "(Bit 5)TransactionsPending-")                    

def GetLinkCap(HexDumpArray,CapHeaderOffset):
    print("==================================")
    
    LinkCapOffset = CapHeaderOffset + OFFSET_LINK_CAPABILITY
    Row,Col = TransferOffsetToArray(LinkCapOffset)
    LinkCapValue = ReadByDword(HexDumpArray,Row,Col)
    print(f"[0x{LinkCapOffset:02X} 04]Link Capibilities:0x{LinkCapValue:04X}")

    MaxLinkSpeedReg = LinkCapValue & (CommonLib.BIT0 | CommonLib.BIT1 | CommonLib.BIT2 | CommonLib.BIT3 )

    print("(Bit 0:3)Max Link Speed:")
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

    MaxLinkWidthReg = (LinkCapValue & ( CommonLib.BIT4 | CommonLib.BIT5 | CommonLib.BIT6 | CommonLib.BIT7 | CommonLib.BIT8 | CommonLib.BIT9) ) >> 4

    print("(Bit 4:9)Max Link Width:")
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

    print("(Bit 10:11)ASPM Support:")
    ASPMSupport = (LinkCapValue & (CommonLib.BIT10 | CommonLib.BIT11)) >> 10 
    match ASPMSupport:
        case 0:
            print("No ASPM Support")
        case 1:
            print("L0s Supported")
        case 2:
            print("L1 Supported")
        case 3:
            print("L0s and L1 Supported")

    print("(Bit 12:14)L0s Exit Latency:")
    L0ExitLatency = (LinkCapValue & (CommonLib.BIT12 | CommonLib.BIT13 | CommonLib.BIT14)) >> 12
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

    print("(Bit 15:17)L1 Exit Latency:")
    L1ExitLatency = (LinkCapValue & (CommonLib.BIT15 | CommonLib.BIT16 | CommonLib.BIT17)) >> 15 
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

    ClockPowerMgmt = (LinkCapValue & CommonLib.BIT18) >> 18 
    SurpriseDownErrorReport = (LinkCapValue & CommonLib.BIT19) >> 19
    DataLinkLayerActiveReport = (LinkCapValue & CommonLib.BIT20) >> 20
    LinkBandWidthNotification = (LinkCapValue & CommonLib.BIT21) >> 21
    AspmOptionCom = (LinkCapValue & CommonLib.BIT22) >> 22

    print("(Bit 18)ClockPowerMgmt+" if(ClockPowerMgmt) else "(Bit 18)ClockPowerMgmt-", "(Bit 19)SurpriseDownErrorReport+" if(SurpriseDownErrorReport) else "(Bit 19)SurpriseDownErrorReport-", "(Bit 20)DataLinkLayerActiveReport+" if(DataLinkLayerActiveReport) else "(Bit 20)DataLinkLayerActiveReport-", "(Bit 21)LinkBandWidthNotification+" if(LinkBandWidthNotification) else "(Bit 21)LinkBandWidthNotification-", "(Bit 22)AspmOptionCom+" if(AspmOptionCom) else "(Bit 22)AspmOptionCom-")

def GetLinkControl(HexDumpArray,CapHeaderOffset):
    print("==================================")
    
    LinkControlOffset = CapHeaderOffset + OFFSET_LINK_CONTROL
    Row,Col = TransferOffsetToArray(LinkControlOffset)
    LinkControlValue = ReadByWord(HexDumpArray,Row,Col)
    print(f"[0x{LinkControlOffset:02X} 02]Link Control:0x{LinkControlValue:04X}")

    AspmControl = (LinkControlValue & (CommonLib.BIT0 | CommonLib.BIT1)) 
    ReadCompletionBoundary = (LinkControlValue & CommonLib.BIT3) >> 3
    LinkDisable = (LinkControlValue & CommonLib.BIT4) >> 4
    CommonClock = (LinkControlValue & CommonLib.BIT5) >> 5
    ExtendSynch = (LinkControlValue & CommonLib.BIT7) >> 7
    ClockPowerMgmt = (LinkControlValue & CommonLib.BIT8) >> 8

    print("(Bit 0:1)ASPM Control:")
    match AspmControl:
        case 0:
            print("AspmControl: Disabled")
        case 1:
            print("AspmControl: L0s Entry Enabled")
        case 2:
            print("AspmControl: L1 Entry Enabled")
        case 3:
            print("AspmControl: L0s and L1 Entry Enabled")

    print("(Bit 3)ReadCompletionBoundary: 128 byte" if(ReadCompletionBoundary) else "(Bit 3)ReadCompletionBoundary: 64 byte", "(Bit 4)LinkDisable+" if(LinkDisable) else "(Bit 4)LinkDisable-", "(Bit 5)CommonClock+" if(CommonClock) else "(Bit 5)CommonClock-","(Bit 7)ExtendSynch+" if(ExtendSynch) else "(Bit 7)ExtendSynch-", "(Bit 8)ClockPowerMgmt+" if(ClockPowerMgmt) else "(Bit 8)ClockPowerMgmt-")                        

def GetLinkStatus(HexDumpArray,CapHeaderOffset):
    print("==================================")
    
    LinkStatusOffset = CapHeaderOffset + OFFSET_LINK_STATUS
    Row,Col = TransferOffsetToArray(LinkStatusOffset)
    LinkStatusValue = ReadByWord(HexDumpArray,Row,Col)
    print(f"[0x{LinkStatusOffset:02X} 02]Link Status:0x{LinkStatusValue:04X}")

    CurrentLinkSpeedReg = LinkStatusValue & (CommonLib.BIT0 | CommonLib.BIT1 | CommonLib.BIT2 | CommonLib.BIT3)

    print("(Bit 0:3)Current Link Speed:")
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

    CurrentLinkWidthReg = (LinkStatusValue & (CommonLib.BIT4 | CommonLib.BIT5 | CommonLib.BIT6 | CommonLib.BIT7 | CommonLib.BIT8 | CommonLib.BIT9 ) ) >> 4

    print("(Bit 4:9)Current Link Width:")
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

    LinkTrain = (LinkStatusValue & CommonLib.BIT11) >> 11
    SlotClock = (LinkStatusValue & CommonLib.BIT12) >> 12
    DataLinkActive = (LinkStatusValue & CommonLib.BIT13) >> 13
    BandWidthMgmt = (LinkStatusValue & CommonLib.BIT14) >> 14
    AutonomousBandWidthMgmt = (LinkStatusValue & CommonLib.BIT15) >> 15

    print("(Bit 11)LinkTrain+" if(LinkTrain) else "(Bit 11)LinkTrain-", "(Bit 12)SlotClock+" if(SlotClock) else "(Bit 12)SlotClock-", "(Bit 13)DataLinkActive+" if(DataLinkActive) else "(Bit 13)DataLinkActive-", "(Bit 14)BandWidthMgmt+" if(BandWidthMgmt) else "(Bit 14)BandWidthMgmt-", "(Bit 15)AutonomousBandWidthMgmt+" if(AutonomousBandWidthMgmt) else "(Bit 15)AutonomousBandWidthMgmt-")

def CheckUEStatus(HexDumpArray,CapHeaderOffset):
    print("==================================")
    
    
    UEStatusOffset = CapHeaderOffset + OFFSET_UE_STATUS
    
    Row,Col = TransferOffsetToArray(UEStatusOffset)
    UEStatusValue = ReadByDword(HexDumpArray,Row,Col)

    print(f"[0x{UEStatusOffset:04X} 04]Uncorrectable Error Status:0x{UEStatusValue:08X}")

    DataLinkProErr = (UEStatusValue & CommonLib.BIT4) >> 4
    SurpriseDownErr = (UEStatusValue & CommonLib.BIT5) >> 5
    PoisonTLPReceived = (UEStatusValue & CommonLib.BIT12) >> 12
    CompleteTimeOut = (UEStatusValue & CommonLib.BIT14) >> 14
    CompleterAbort = (UEStatusValue & CommonLib.BIT15) >> 15
    UnexpectCompletion = (UEStatusValue & CommonLib.BIT16) >> 16
    ReceiverOverflow = (UEStatusValue & CommonLib.BIT17) >> 17
    MalformedTLP = (UEStatusValue & CommonLib.BIT18) >> 18
    ECRCErr = (UEStatusValue & CommonLib.BIT19) >> 19
    UnsupportRequest = (UEStatusValue & CommonLib.BIT20) >> 20
    MCBlockTLP = (UEStatusValue & CommonLib.BIT23) >> 23
    AtomicOPEgressBlock = (UEStatusValue & CommonLib.BIT24) >> 24
    DMWrRequestEgressBlock = (UEStatusValue & CommonLib.BIT27) >> 27
    IDECheckFailed = (UEStatusValue & CommonLib.BIT28) >> 28
    TLPTranslationEgressBlock = (UEStatusValue & CommonLib.BIT31) >> 31

    print("(Bit 4)DataLinkProErr+" if(DataLinkProErr) else "(Bit 4)DataLinkProErr-", "(Bit 5)SurpriseDownErr+" if(SurpriseDownErr) else "(Bit 5)SurpriseDownErr-", "(Bit 12)PoisonTLPReceived+" if(PoisonTLPReceived) else "(Bit 12)PoisonTLPReceived-", "(Bit 14)CompleteTimeOut+" if(CompleteTimeOut) else "(Bit 14)CompleteTimeOut-", "(Bit 15)CompleterAbort+" if(CompleterAbort) else "(Bit 15)CompleterAbort-", "(Bit 16)UnexpectCompletion+" if(UnexpectCompletion) else "(Bit 16)UnexpectCompletion-")
    print("(Bit 17)ReceiverOverflow+" if(ReceiverOverflow) else "(Bit 17)ReceiverOverflow-", "(Bit 18)MalformedTLP+" if(MalformedTLP) else "(Bit 18)MalformedTLP-", "(Bit 19)ECRCErr+" if(ECRCErr) else "(Bit 19)ECRCErr-", "(Bit 20)UnsupportRequest+" if(UnsupportRequest) else "(Bit 20)UnsupportRequest-", "(Bit 23)MCBlockTLP+" if(MCBlockTLP) else "(Bit 23)MCBlockTLP-", "(Bit 24)AtomicOPEgressBlock+" if(AtomicOPEgressBlock) else "(Bit 24)AtomicOPEgressBlock-", "(Bit 27)DMWrRequestEgressBlock+" if(DMWrRequestEgressBlock) else "(Bit 27)DMWrRequestEgressBlock-")
    print("(Bit 28)IDECheckFailed+" if(IDECheckFailed) else "(Bit 28)IDECheckFailed-", "(Bit 31)TLPTranslationEgressBlock+" if(TLPTranslationEgressBlock) else "(Bit 31)TLPTranslationEgressBlock-")
"""
    def GetVendor(self, pciid:str):
        self.__vendor = f"{self.__base}/vendor"
        with open(self.__vendor,'r') as file:
            VendorId = file.read()
            print("VendorId:",VendorId)                    
"""        


        
    