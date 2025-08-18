# Standard Lib
import os
import subprocess

# Create Lib
import PciBusEnum
import ACPITable
import CpuFreq

POWER_MGMT_ID = 0x1     # Power Mgmt id 
MSI_X_CAP_ID = 0x11     # MSI cap id
PCIE_CAP_ID = 0x10      # PCIe cap id 
AER_CAP_ID = 0x1        # AER cap id

# Global variable

def PciDeviceList():
    PfaNumberIndex = 0            
    PfaNumberIndex,HexVendor,HexDevice = PciBusEnum.PciEnumOperation()

    while True:
        print("==================================")
        InputVal = input("Which PCI device?")
                
        if (InputVal == ""):
            break
                
        WhichDevice = int(InputVal)
        print("==================================")

        while (WhichDevice <= PfaNumberIndex):
            HexDumpArray = PciBusEnum.ListPciRegContent(HexVendor[WhichDevice],HexDevice[WhichDevice])
            """
            print("Device index",WhichDevice,":",gPfaNumberArray[WhichDevice])
            SelectDevice = PciBusEnum.Device(gPfaNumberArray[WhichDevice])
            SelectDevice.GetVendor(gPfaNumberArray[WhichDevice])
            """
            # Check Type0/1 device
            HeaderLayout,MultiFun = PciBusEnum.CheckTypeHeader(HexDumpArray)

            print("==================================")
                    
            if HeaderLayout == 0:
                print(f"[0x0E 01]Type 0(Device) [Bit 7]MultiFunction:{MultiFun}")
                PciBusEnum.CheckBarRegister(HexDumpArray,0)
            else:
                print(f"[0x0E 01]Type 1(Bridge) [Bit 7]MultiFunction:{MultiFun}")
                PciBusEnum.CheckBarRegister(HexDumpArray,1)
                PciBusEnum.CheckBusRelation(HexDumpArray)

            PciBusEnum.CheckCmdReg(HexDumpArray)

            # Check MSI cap
            CapHeaderOffset = PciBusEnum.PcieBaseFindCapId(HexDumpArray,MSI_X_CAP_ID)
            print(f"MSI-X Capability Pointer:{CapHeaderOffset:02X}")
            print("==================================")

            # Check Power Management cap
            CapHeaderOffset = PciBusEnum.PcieBaseFindCapId(HexDumpArray,POWER_MGMT_ID)
            print(f"Power Management Capability Pointer:{CapHeaderOffset:02X}")
            print("==================================")

            # Check PCIe cap
            CapHeaderOffset = PciBusEnum.PcieBaseFindCapId(HexDumpArray,PCIE_CAP_ID)
            print(f"PCIe Capability Pointer:{CapHeaderOffset:02X}")

            # Check PCI/PCIe device
            if(CapHeaderOffset == 0):
                print("PCI device")
            else:
                # Check Pcie Cap
                PciBusEnum.GetPcieCapRegister(HexDumpArray,CapHeaderOffset)

                # Check Device Cap
                PciBusEnum.GetDeviceCap(HexDumpArray,CapHeaderOffset)

                # Check Device Control
                PciBusEnum.GetDeviceControl(HexDumpArray,CapHeaderOffset)

                # Check Device Status
                PciBusEnum.GetDeviceStatus(HexDumpArray,CapHeaderOffset)                        

                # Check Link Cap
                PciBusEnum.GetLinkCap(HexDumpArray,CapHeaderOffset)

                # Check Link Control
                PciBusEnum.GetLinkControl(HexDumpArray,CapHeaderOffset)

                # Check Link Status
                PciBusEnum.GetLinkStatus(HexDumpArray,CapHeaderOffset)

                CheckPcieExt = input("Check Pcie Extend Capability?(y/n)")

                if CheckPcieExt == "":
                    break

                while(CheckPcieExt == "y"):
                    
                    # List Pcie content
                    PcieHexDumpArray = PciBusEnum.ListPcieRegContent(HexVendor[WhichDevice],HexDevice[WhichDevice])
                    
                    # Check AER cap
                    CapHeaderOffset = PciBusEnum.PcieExtBaseFindCapId(PcieHexDumpArray,AER_CAP_ID)
                    print(f"AER Capability Pointer:{CapHeaderOffset:04X}")

                    # Check UE Status Register
                    PciBusEnum.CheckUEStatus(PcieHexDumpArray,CapHeaderOffset)

                    break  # while(CheckPcieExt == "y"):


            break # while (WhichDevice <= gPfaNumberIndex)

def ACPITableList():
    ACPITableArray = []

    TablePath = "/sys/firmware/acpi/tables"
    if not os.path.exists(TablePath):
        print("ACPI tables not found")
        return
    
    Count = 0
    for TableFile in os.listdir(TablePath):
        if ( (TableFile != "dynamic") and (TableFile != "data") ):
            ACPITableArray.append(TableFile)
            Count += 1
    
    for i in range(Count):
        print(f"Index:{i:02} - {ACPITableArray[i]}")

    while True:
        print("==================================")
        InputVal = input("Which ACPI Table?")
                
        if (InputVal == ""):
            break
                
        WhichTable = int(InputVal)
        print("==================================")

        while (WhichTable <= Count):
            ACPITable.DumpAcpiTable(ACPITableArray[WhichTable])

        
            break # while (WhichTable <= Count):

def SMBIOSTableList():

    EntryNum = 0

    print("TYPE 0 - Bios Information")
    print("TYPE 1 - System Information")
    print("TYPE 2 - Baseboard (or Module) Information")
    print("TYPE 3 - System Enclosure or Chassis")
    print("TYPE 4 - Processor Information")
    print("TYPE 7 - Cache Information")
    print("TYPE 8 - Port Connector Information")
    print("TYPE 9 - System Slots")
    print("TYPE 11 - OEM Strings")
    print("TYPE 13 - BIOS Language Information")
    print("TYPE 16 - Physical Memory Array")
    print("TYPE 17 - Memory Device")
    print("TYPE 19 - Memory Array Mapped Address")
    print("TYPE 24 - Hardware Security")
    print("TYPE 32 - System Boot Information")
    print("TYPE 33 - 64-Bit Memory Error Information")
    print("TYPE 38 - IPMI Device Information")
    print("TYPE 44 - Processor Additional Information")
    print("TYPE 45 - Firmware Inventory Information")
    print("TYPE 127 - End-Of-Table")
    print("==================================")

    while True:

        InputVal = input("Which type of SMBIOS Table?")
                
        if (InputVal == ""):
            break
                
        for Type in range(128):
            for Entry in range(20):
                TypeNum = f"{str(Type)}-{str(Entry)}"
                FileOpen = os.path.join("/sys/firmware/dmi/entries/", str(TypeNum))

                if os.access(FileOpen, os.F_OK):
                    #print(f"Find {TypeNum}")
                    EntryNum += 1
                     

        WhichTable = int(InputVal)
        print("==================================")

        while (WhichTable <= Type):
            for Type in range(128):
                for Entry in range(20):
                    TypeNum = f"{str(Type)}-{str(Entry)}"
                    FileOpen = os.path.join("/sys/firmware/dmi/entries/", str(TypeNum))
                    
                    if Type == WhichTable:

                        SmbiosTableHexDumpCmd = f"hexdump -C /sys/firmware/dmi/entries/{TypeNum}/raw"

                        if os.access(FileOpen, os.F_OK):
                            SmbiosStr = subprocess.run(SmbiosTableHexDumpCmd, capture_output=True, text=True, shell=True)
                            print(SmbiosStr.stdout)

            SmbiosTableCmd = f"sudo dmidecode -t {WhichTable}"
            SmbiosStr = subprocess.run(SmbiosTableCmd, capture_output=True, text=True, shell=True)
            print(SmbiosStr.stdout)

        
            break # while (WhichTable <= Count):  

def CpuFreqSetting():

    TablePath = "/sys/devices/system/cpu/enabled"
    if os.path.exists(TablePath):
        with open(TablePath,'r') as file:
            CoreNumStr = file.read()

    print("==================================")

    # core number, ex: 0-191
    StartCoreNum = CoreNumStr[0]
    EndCoreNum = str(CoreNumStr[2]) + str(CoreNumStr[3]) + str(CoreNumStr[4])

    CoreNum = int(EndCoreNum) - int(StartCoreNum) + 1

    print(f"Start Core Number:{StartCoreNum}\nEnd Core Number:{EndCoreNum}\nCore Numbers:{CoreNum}")
    
    while True:
        print("==================================")
        ReadOrWrite = input("(0) Read\n(1) Write\nWhich selection?")

        if ReadOrWrite == '':
            break

        ReadOrWrite = int(ReadOrWrite)

        if ReadOrWrite == 0:
            print("(0) Read single core\n(1) Read all cores")
            ReadNumbers = input("Which selection?")
            
            if ReadNumbers == "":
                break
            
            ReadNumbers = int(ReadNumbers)

            if ReadNumbers:
                CpuFreq.ListCurrentCoreNumber(CoreNum, 1)
            else:
                CpuFreq.ListCurrentCoreNumber(CoreNum, 0)

        elif ReadOrWrite == 1:
            print("(0) Write single core\n(1) Write all cores\n(2) Write governor")
            WriteNumbers = input("Which selection?")

            if(WriteNumbers == ""):
                break

            WriteNumbers = int(WriteNumbers)

            if WriteNumbers == 0:
                CpuFreq.WriteCoreNumber(CoreNum, 0)
            elif WriteNumbers == 1:
                CpuFreq.WriteCoreNumber(CoreNum, 1)
            elif WriteNumbers == 2:
                CpuFreq.WriteCoreNumber(CoreNum, 2)     

# Main prompt
while True:
    print("==================================")
    print("Select Operation:\n 0:PCI device List\n 1:ACPI table\n 2:SMBIOS table\n 3:CPU frequency setting")
    Select = input("Selection:")

    if Select == '':
        break

    Select = int(Select)

    match Select:
        case 0:
            PciDeviceList()
        case 1:
            ACPITableList()
        case 2:
            SMBIOSTableList()
        case 3:
            CpuFreqSetting()