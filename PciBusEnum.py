from periphery import MMIO

def PciEnum():
    for Bus in range(256):
        for Dev in range(32):
            for Fun in range(8):
                Address = 0x80000000 + (Bus << 20) + (Dev << 15) + (Fun << 12)
                #print("Address = ",Address)
                VidDid = MMIO(Address,0x4)
                print("VidDid = ", VidDid)