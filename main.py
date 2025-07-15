# Standard Lib
import array

# Create Lib
import PciBusEnum

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
                print("Type 0(Device)")
                PciBusEnum.CheckBarRegister(HexDumpArray)
            else:
                print("Type 1(Bridge)")
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

                # List Pcie content
                PcieHexDumpArray = PciBusEnum.ListPcieRegContent(HexVendor[WhichDevice],HexDevice[WhichDevice])

                # Check AER cap
                CapHeaderOffset = PciBusEnum.PcieExtBaseFindCapId(PcieHexDumpArray,AER_CAP_ID)
                print(f"AER Capability Pointer:{CapHeaderOffset:04X}")

                # Check AER Extended Cap
                PciBusEnum.GetAERExtCap(PcieHexDumpArray,CapHeaderOffset)


            break # while (WhichDevice <= gPfaNumberIndex)


# Main prompt

while True:
    print("Select Operation:\n0:PCI device List\n1:ACPI table\n2:SMBIOS table\n")
    Select = int(input("Selection:"))

    match Select:
        case 0:
            PciDeviceList()        
