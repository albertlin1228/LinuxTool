import os
import errno
import subprocess
import time

def ReadCpuFreq(WhichCoreNumber, PathName):

    if os.path.exists(PathName):
        with open(PathName,'r') as file:
            try:
                Line = file.readline()
                Line = Line.strip()
                LineVal = int(Line,10) / 1000000
                return LineVal
            except OSError as e:
                if e.errno == errno.EBUSY:
                    print(f"Core{WhichCoreNumber} is Offline")
                    return 0

def ReadCpuGovernor(WhichCoreNumber, PathName):

    if os.path.exists(PathName):
        with open(PathName,'r') as file:
            try:
                Line = file.readline()
                Line = Line.strip()
                return Line
            except OSError as e:
                if e.errno == errno.EBUSY:
                    print(f"Core{WhichCoreNumber} is Offline")
                    return 0

def SetCpuFreq(WhichCoreNumber, PathName, FreqVal):

    SetFreqCmd = str("echo ") + str(FreqVal) + str(" > ") + str(PathName)
    #print("SetFreqCmd:",SetFreqCmd)
    subprocess.Popen(SetFreqCmd, stdout=subprocess.PIPE, text=True, shell=True)
    print(f"Set cpu{WhichCoreNumber} to {FreqVal}!")

                                
def SetGovernor(WhichCoreNumber, PathName, WhichGovernor):

    SetGovernorCmd = str("echo ") + str(WhichGovernor) + str(" > ") + str(PathName)
    #print("SetGovernorCmd:",SetGovernorCmd)

    Result = subprocess.Popen(SetGovernorCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    stdout, stderr = Result.communicate()

    if (stderr):
        print(f"Core{WhichCoreNumber} is Offline")
        return 0
    else:
        print(f"Set cpu{WhichCoreNumber} governor to {WhichGovernor}!")
        return 1
                                           

def ReadCoreByNumber(WhichCoreNumber):
    CpuNum = f"cpu{WhichCoreNumber}"

    # Scaling avaliable governor
    WhichGovernor = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/scaling_available_governors")    
    LineVal = ReadCpuGovernor(WhichCoreNumber, WhichGovernor)
    if LineVal == 0:
        return 0
    print(f"Core{WhichCoreNumber}:")     
    print(f"\tScaling avaliable governor:{LineVal}")

    # Scaling governor
    WhichGovernor = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/scaling_governor")    
    LineVal = ReadCpuGovernor(WhichCoreNumber, WhichGovernor)
    print(f"\tScaling governor:{LineVal}")

    # Cpu info cur freq
    CpuCurFreqPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/cpuinfo_cur_freq")
    LineVal = ReadCpuFreq(WhichCoreNumber, CpuCurFreqPath)
    print(f"\tCurrent frequency:{LineVal}GHz")

    # Cpu info max freq
    CpuMaxFreqPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/cpuinfo_max_freq")
    LineVal = ReadCpuFreq(WhichCoreNumber, CpuMaxFreqPath)
    print(f"\tMaximum frequency:{LineVal}GHz")

    # Cpu info min freq
    CpuMinFreqPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/cpuinfo_min_freq")    
    LineVal = ReadCpuFreq(WhichCoreNumber, CpuMinFreqPath)
    print(f"\tMinimum frequency:{LineVal}GHz")



def ReadAllCoreData(ReadNumbers):
    OfflineCore = []

    OfflineCoreNum =0

    for i in range(ReadNumbers):
        CpuNum = f"cpu{i}"

        AvaliableGovernor = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/scaling_available_governors")
        WhichGovernor = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/scaling_governor")     
        CpuCurFreqPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/cpuinfo_cur_freq")
        CpuMinFreqPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/cpuinfo_min_freq")
        CpuMaxFreqPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/cpuinfo_max_freq") 

        # Cpu info cur freq

        LineVal = ReadCpuGovernor(i, AvaliableGovernor)

        if LineVal:
            print(f"Core{i}:") 
            print(f"\tScaling avaliable governor:{LineVal}")

            LineVal = ReadCpuGovernor(i, WhichGovernor)
            print(f"\tScaling governor:{LineVal}")

            LineVal = ReadCpuFreq(i, CpuCurFreqPath)
            print(f"\tCurrent frequency:{LineVal}GHz") 
            
            LineVal = ReadCpuFreq(i, CpuMinFreqPath)
            print(f"\tMinimum frequency:{LineVal}GHz")

            LineVal = ReadCpuFreq(i, CpuMaxFreqPath)
            print(f"\tMaximum frequency:{LineVal}GHz") 
        else:
            OfflineCore.append(i)
            OfflineCoreNum += 1       

    return OfflineCoreNum, OfflineCore

def ListCurrentCoreNumber(CoreNum,ReadNumbers):

    print("==================================")
    if ReadNumbers == 1:
        OfflineCoreNum, OfflineCore = ReadAllCoreData(CoreNum)
        
        for i in range(OfflineCoreNum):
            print(f"Core{OfflineCore[i]} is offline")
    else:
        WhichCoreNumber = int(input("Read which core number?"))
        ReadCoreByNumber(WhichCoreNumber)

def WriteSingleCoreData(WhichCoreNum,FreqVal):
    
    CpuNum = f"cpu{WhichCoreNum}"
    ScalGovernorPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/scaling_governor")
    ScalingSpeedPath = str("/sys/devices/system/cpu/") + str(CpuNum) + str("/cpufreq/scaling_setspeed")
        
    Val = SetGovernor(WhichCoreNum, ScalGovernorPath, "userspace")
        
    if Val == 1:
        SetCpuFreq(WhichCoreNum, ScalingSpeedPath, FreqVal)
    
def WriteAllCoreData(TotalCoreNum, FreqVal):
    
    for i in range(TotalCoreNum):
        WriteSingleCoreData(i,FreqVal)
        time.sleep(0.01)

def WriteCoreNumber(TotalCoreNum,WriteNumbers):

    print("==================================")
    
    if WriteNumbers == 1:
        FreqVal = int(input("Input speed value:"))
        WriteAllCoreData(TotalCoreNum,FreqVal)
    elif WriteNumbers ==0:
        WhichCoreNum = int(input("Which core number:"))
        FreqVal = int(input("Speed value:"))
        WriteSingleCoreData(WhichCoreNum,FreqVal)