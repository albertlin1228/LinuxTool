# Standard Lib
import array

# Create Lib
import PciBusEnum

# Global variable
gPfaNumberArray = []
gPfaNumberIndex = 0
gHexVendor = {}
gHexDevice = {}

def PciEnumOperation():
    global gPfaNumberArray
    global gPfaNumberIndex
    global gHexVendor
    global gHexDevice

    for Segment in range(8):
        for Bus in range(256):
            for Dev in range(32):
                for Fun in range(8):
                    # PfaNumber = 0007:00:01.0
                    PfaNumber = f"{str(Segment).zfill(4)}:{str(Bus).zfill(2)}:{str(Dev).zfill(2)}.{str(Fun)}"
                    PciBusEnum.Device(PfaNumber)

                    if PciBusEnum.GlobalExistDevice == 1:
                        gPfaNumberArray.append(PfaNumber)
                        
                        # Save Vid and Did from string file of the /sys/bus/pci/devices/ to hex digit
                        DigitVendor = int(PciBusEnum.GlobalVendorId,16)
                        DigitDevice = int(PciBusEnum.GlobalDeviceId,16)
                        
                        gHexVendor[gPfaNumberIndex] = str(hex(DigitVendor))
                        gHexDevice[gPfaNumberIndex] = str(hex(DigitDevice))

                        print(f"Index {str(gPfaNumberIndex).zfill(2)} : {PfaNumber} VendorId: {DigitVendor:04X} DeviceId: {DigitDevice:04X}" )

                        gPfaNumberIndex += 1


# Main prompt

while True:
    print("Select Operation:\n0:Select PCI enum operation\n")
    Select = int(input("Selection:"))

    match Select:
        case 0:        
            gPfaNumberIndex = 0            
            PciEnumOperation()

            while True:
                print("==================================")
                InputVal = input("Which device?")
                
                if (InputVal == ""):
                    break
                
                WhichDevice = int(InputVal)
                print("==================================")

                while (WhichDevice <= gPfaNumberIndex):
                    HexDumpArray = PciBusEnum.ListPciRegContent(gHexVendor[WhichDevice],gHexDevice[WhichDevice])
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

                    # Check PCIe cap
                    CapHeaderOffset = PciBusEnum.PcieBaseFindCapId(HexDumpArray,0x10)
                    print(f"Capability Header Offset:{CapHeaderOffset:02X}")

                    # Check PCI/PCIe device
                    if(CapHeaderOffset == 0):
                        print("PCI device")
                    else:
                        print("PCIe device")

                        # Check maximum/current Link speed
                        PciBusEnum.GetLinkCap(HexDumpArray,CapHeaderOffset)

                        # Check maximum/current Link width
                        PciBusEnum.GetLinkStatus(HexDumpArray,CapHeaderOffset)


                    break # while (WhichDevice <= gPfaNumberIndex)