import os

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
"""
    def GetVendor(self, pciid:str):
        self.__vendor = f"{self.__base}/vendor"
        with open(self.__vendor,'r') as file:
            VendorId = file.read()
            print("VendorId:",VendorId)                    
"""        


        
    