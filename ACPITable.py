import subprocess

def GetSignature(HexDumpArray):
    
    # Byte Offset 0x0, Byte Length 0x4
    Byte0 = int(HexDumpArray[0][0],16)
    Byte1 = int(HexDumpArray[0][1],16)
    Byte2 = int(HexDumpArray[0][2],16)
    Byte3 = int(HexDumpArray[0][3],16)

    Strcpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3)

    print(f"Signature: {HexDumpArray[0][0]} {HexDumpArray[0][1]} {HexDumpArray[0][2]} {HexDumpArray[0][3]} ({Strcpy})")

def GetLength(HexDumpArray):
    
    # Byte Offset 0x4, Byte Length 0x4
    Byte0 = int(HexDumpArray[0][4],16)
    Byte1 = int(HexDumpArray[0][5],16)
    Byte2 = int(HexDumpArray[0][6],16)
    Byte3 = int(HexDumpArray[0][7],16)

    LengthVal = (Byte3 << 24) | (Byte2 << 16) | (Byte1 << 8) | Byte0 

    print(f"Length: 0x{LengthVal:08X}")

def GetRevision(HexDumpArray):
    
    # Byte Offset 0x8, Byte Length 0x1
    print(f"Revision: {HexDumpArray[0][8]}")

def GetChecksum(HexDumpArray):
    
    # Byte Offset 0x9, Byte Length 0x1
    print(f"Checksum: {HexDumpArray[0][9]}")    

def GetOemId(HexDumpArray):
    
    # Byte Offset 0x10, Byte Length 0x6
    Byte0 = int(HexDumpArray[0][10],16)
    Byte1 = int(HexDumpArray[0][11],16)
    Byte2 = int(HexDumpArray[0][12],16)
    Byte3 = int(HexDumpArray[0][13],16)
    Byte4 = int(HexDumpArray[0][14],16)
    Byte5 = int(HexDumpArray[0][15],16)

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3) + chr(Byte4) + chr(Byte5)

    print(f"OEMID: {HexDumpArray[0][10]} {HexDumpArray[0][11]} {HexDumpArray[0][12]} {HexDumpArray[0][13]} {HexDumpArray[0][14]} {HexDumpArray[0][15]} ({StrCpy})")        

def GetOemTableId(HexDumpArray):
    
    # Byte Offset 0x16, Byte Length 0x8
    Byte0 = int(HexDumpArray[1][0],16)
    Byte1 = int(HexDumpArray[1][1],16)
    Byte2 = int(HexDumpArray[1][2],16)
    Byte3 = int(HexDumpArray[1][3],16)
    Byte4 = int(HexDumpArray[1][4],16)
    Byte5 = int(HexDumpArray[1][5],16)
    Byte6 = int(HexDumpArray[1][6],16)
    Byte7 = int(HexDumpArray[1][7],16)    

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3) + chr(Byte4) + chr(Byte5) + chr(Byte6) + chr(Byte7)

    print(f"OEMID Table ID: {HexDumpArray[1][0]} {HexDumpArray[1][1]} {HexDumpArray[1][2]} {HexDumpArray[1][3]} {HexDumpArray[1][4]} {HexDumpArray[1][5]} {HexDumpArray[1][6]} {HexDumpArray[1][7]} ({StrCpy})")

def GetOemRevision(HexDumpArray):
    
    # Byte Offset 0x24, Byte Length 0x4
    Byte0 = int(HexDumpArray[1][8],16)
    Byte1 = int(HexDumpArray[1][9],16)
    Byte2 = int(HexDumpArray[1][10],16)
    Byte3 = int(HexDumpArray[1][11],16)

    OemRevision = (Byte3 << 24) | (Byte2 << 16) | (Byte1 << 8) | Byte0 

    print(f"OEM Revision: {OemRevision}")

def GetCreaterId(HexDumpArray):
    
    # Byte Offset 0x28, Byte Length 0x4
    Byte0 = int(HexDumpArray[1][12],16)
    Byte1 = int(HexDumpArray[1][13],16)
    Byte2 = int(HexDumpArray[1][14],16)
    Byte3 = int(HexDumpArray[1][15],16)

    StrCpy = chr(Byte0) + chr(Byte1) + chr(Byte2) + chr(Byte3)

    print(f"Creater ID: {HexDumpArray[1][12]} {HexDumpArray[1][13]} {HexDumpArray[1][14]} {HexDumpArray[1][15]} ({StrCpy})")

def GetCreaterRevision(HexDumpArray):
    
    # Byte Offset 0x32, Byte Length 0x4
    Byte0 = int(HexDumpArray[2][0],16)
    Byte1 = int(HexDumpArray[2][1],16)
    Byte2 = int(HexDumpArray[2][2],16)
    Byte3 = int(HexDumpArray[2][3],16)

    CreaterRevision = (Byte3 << 24) | (Byte2 << 16) | (Byte1 << 8) | Byte0 

    print(f"Creater Revision: 0x{CreaterRevision:04X}")

def DumpTable(TableName):
    HexDumpArray = [[0]*16 for i in range(16)]

    DumpSpcrCmd = f"sudo hexdump -C /sys/firmware/acpi/tables/{TableName}"
    TableDump = subprocess.Popen(DumpSpcrCmd, stdout=subprocess.PIPE, text=True, shell=True)

    for RowIndex in range(16):

        ReadLine = TableDump.stdout.readline()
        #print("len(ReadLine):",len(ReadLine))

        print(ReadLine[0:78])

        for ColIndex in range(10,34,3):
            if( ColIndex >= len(ReadLine)):
                break
            if( ReadLine[ColIndex] == " "):
                break
            StrCpy = '0x' + ReadLine[ColIndex] + ReadLine[ColIndex+1]
            ArrayRow = RowIndex
            ArrayCol = (ColIndex-10)//3
            HexDumpArray[ArrayRow][ArrayCol]= hex(int(StrCpy,16))
            #print(f"HexDumpArray[{ArrayRow}][{ArrayCol}]:{HexDumpArray[ArrayRow][ArrayCol]}")

        for ColIndex in range(35,59,3):
            if( ColIndex >= len(ReadLine)):
                break
            if( ReadLine[ColIndex] == " "):
                break

            StrCpy = '0x' + ReadLine[ColIndex] + ReadLine[ColIndex+1]
            ArrayRow = RowIndex
            ArrayCol = (ColIndex-10)//3
            HexDumpArray[ArrayRow][ArrayCol]= hex(int(StrCpy,16))
            #print(f"HexDumpArray[{ArrayRow}][{ArrayCol}]:{HexDumpArray[ArrayRow][ArrayCol]}")

    """
    # Show content
    for RowIndex in range(ArrayRow+1):    
        for ColIndex in range(ArrayCol+1):
            print(f"{HexDumpArray[RowIndex][ColIndex]}")      
    """
    GetSignature(HexDumpArray)
    GetLength(HexDumpArray)
    GetRevision(HexDumpArray)
    GetChecksum(HexDumpArray)
    GetOemId(HexDumpArray)
    GetOemTableId(HexDumpArray)
    GetOemRevision(HexDumpArray)
    GetCreaterId(HexDumpArray)
    GetCreaterRevision(HexDumpArray)
        

def DumpAcpiTable(AcpiTableString):
    match AcpiTableString:
        case "SPCR":
            DumpTable("SPCR")
        case "MCFG":
            DumpTable("MCFG")
        case "GTDT":
            DumpTable("GTDT")
        case "APMT":
            DumpTable("APMT")
        case "EINJ":
            DumpTable("EINJ")
        case "APIC":
            DumpTable("APIC")
        case "PCCT":
            DumpTable("PCCT")
        case "SSDT2":
            DumpTable("SSDT2")
        case "HMAT":
            DumpTable("HMAT")
        case "IORT":
            DumpTable("IORT")
        case "SLIT":
            DumpTable("SLIT")
        case "SPMI":
            DumpTable("SPMI")
        case "SDEI":
            DumpTable("SDEI")
        case "DSDT":
            DumpTable("DSDT")
        case "SRAT":
            DumpTable("SRAT")
        case "DBG2":
            DumpTable("DBG2")
        case "HEST":
            DumpTable("HEST")
        case "SSDT3":
            DumpTable("SSDT3")
        case "FACP":
            DumpTable("FACP")
        case "SSDT1":
            DumpTable("SSDT1")
        case "RAS2":
            DumpTable("RAS2")
        case "AGDI":
            DumpTable("AGDI")
        case "PPTT":
            DumpTable("PPTT")