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
                        HexVendor = hex(DigitVendor)
                        HexDevice = hex(DigitDevice)
                        
                        gHexVendor[gPfaNumberIndex] = HexVendor
                        gHexDevice[gPfaNumberIndex] = HexDevice

                        print("Index",gPfaNumberIndex,":",PfaNumber," VendorId:",HexVendor.zfill(4)," DeviceId:",HexDevice.zfill(4) )

                        gPfaNumberIndex += 1


# Main prompt y
print("Select Operation:\n0:Select PCI enum operation\n")
Select = int(input("Selection:"))

match Select:
    case 0:
        PciEnumOperation()
        
        while True:
            WhichDevice = int(input("Which device?"))

            while (WhichDevice <= gPfaNumberIndex):
                PciBusEnum.ListPciRegContent(gHexVendor[WhichDevice],gHexDevice[WhichDevice])
                """
                print("Device index",WhichDevice,":",gPfaNumberArray[WhichDevice])
                SelectDevice = PciBusEnum.Device(gPfaNumberArray[WhichDevice])
                SelectDevice.GetVendor(gPfaNumberArray[WhichDevice])
                """

                while True:
                    HeaderLayout,MultiFun = PciBusEnum.CheckTypeHeader(gHexVendor[WhichDevice],gHexDevice[WhichDevice])
                    if HeaderLayout == 0:
                        print("Type 0/Pci device")
                        PciBusEnum.CheckBarRegister(gHexVendor[WhichDevice],gHexDevice[WhichDevice])
                    else:
                        print("Type 1/Pci bridge")    

                    break

                break