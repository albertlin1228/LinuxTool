# Import tk GUI
import tkinter as tk
import PciBusEnum

# Build frame
window = tk.Tk()

MmioFrame = tk.Frame(window)
MmioFrame.pack(side=tk.TOP)

IoFrame = tk.Frame(window)
IoFrame.pack(side=tk.TOP)

PciFrame = tk.Frame(window)
PciFrame.pack(side=tk.TOP)

#Function

def CalculateMmio(MmioAddr,MmioData):
    Addr=MmioAddr.get("1.0","end")
    print(Addr)
    Data=MmioData.get("1.0","end")
    print(Data)


def CreateMmioUi():
    NewMmiowindow=tk.Toplevel(window)

    MmioAddr = tk.Text(NewMmiowindow,height=3)
    MmioData = tk.Text(NewMmiowindow,height=3)

    MmioAddr.pack()
    MmioData.pack()

    MmioHead = tk.Label(NewMmiowindow, text = "Mmio address")
    WriteButton = tk.Button(NewMmiowindow, text = "Write",command=lambda : CalculateMmio(MmioAddr,MmioData))

    MmioHead.pack()
    WriteButton.pack()


def CreateIoUi():
    NewIowindow=tk.Toplevel(window)

def CreatePciUi():
    NewPciwindow=tk.Toplevel(window)
    PciBusEnum.PciEnum()

#Button behavior    

MmioButton = tk.Button(MmioFrame, text='Mmio address', fg='black', command=CreateMmioUi)
MmioButton.pack(side=tk.TOP)

IoButton = tk.Button(IoFrame, text='IO address', fg='black', command=CreateIoUi)
IoButton.pack(side=tk.TOP)

PciButton = tk.Button(PciFrame, text='List Pci Devices', fg='black', command=CreatePciUi)
PciButton.pack(side=tk.TOP)

window.mainloop()
