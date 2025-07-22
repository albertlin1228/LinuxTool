# Standard Lib
import array
import os

# Create Lib
import PciBusEnum
import ACPITable

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
        InputVal = input("Which device?")
                
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
                print(f"Type 0(Device) MultiFunction:{MultiFun}")
                PciBusEnum.CheckBarRegister(HexDumpArray)
            else:
                print(f"Type 1(Bridge) MultiFunction:{MultiFun}")
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
        InputVal = input("Which Table?")
                
        if (InputVal == ""):
            break
                
        WhichTable = int(InputVal)
        print("==================================")

        while (WhichTable <= Count):
            ACPITable.DumpAcpiTable(ACPITableArray[WhichTable])

        
            break # while (WhichTable <= Count):


# Main prompt

while True:
    print("Select Operation:\n0:PCI device List\n1:ACPI table\n2:SMBIOS table\n")
    Select = int(input("Selection:"))

    match Select:
        case 0:
            PciDeviceList()
        case 1:
            ACPITableList()
        
