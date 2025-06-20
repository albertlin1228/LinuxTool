# Standard Lib
import array

# Create Lib
import PciBusEnum

# Global variable
PfaNumberArray = []
PfaNumberIndex = 0

def PciEnumOperation():
    global PfaNumberArray
    global PfaNumberIndex

    for Segment in range(8):
        for Bus in range(256):
            for Dev in range(32):
                for Fun in range(8):
                    PfaNumber = f"{str(Segment).zfill(4)}:{str(Bus).zfill(2)}:{str(Dev).zfill(2)}.{str(Fun)}"
                    PciBusEnum.Device(PfaNumber)

                    if PciBusEnum.GlobalExistDevice == 1:
                        PfaNumberArray.append(PfaNumber)
                        print("Index",PfaNumberIndex,":",PfaNumber, " VendorId:",PciBusEnum.GlobalVendorId, "DeviceId:", PciBusEnum.GlobalDeviceId)
                        PfaNumberIndex += 1

# Main prompt y
print("Select Operation:\n0:Select PCI enum operation\n")
Select = int(input("Selection:"))

match Select:
    case 0:
        PciEnumOperation()
        
        while True:
            WhichDevice = int(input("Which device?"))

            while (WhichDevice <= PfaNumberIndex):
                """
                print("Device index",WhichDevice,":",PfaNumberArray[WhichDevice])
                SelectDevice = PciBusEnum.Device(PfaNumberArray[WhichDevice])
                SelectDevice.GetVendor(PfaNumberArray[WhichDevice])
                """
                break