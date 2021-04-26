# Import tk GUI
import tkinter as tk

# Build frame
window = tk.Tk()

MMIO_frame = tk.Frame(window)
MMIO_frame.pack(side=tk.TOP)

IO_frame = tk.Frame(window)
IO_frame.pack(side=tk.TOP)

PCI_frame = tk.Frame(window)
PCI_frame.pack(side=tk.TOP)

#Function

def CalculateMMIO(MmioAddr,MmioData):
    Addr=MmioAddr.get("1.0","end")
    print(Addr)
    Data=MmioData.get("1.0","end")
    print(Data)


def CreateMMIO():
    NewMmiowindow=tk.Toplevel(window)

    MmioAddr = tk.Text(NewMmiowindow,height=3)
    MmioData = tk.Text(NewMmiowindow,height=3)

    MmioAddr.pack()
    MmioData.pack()

    MmioHead = tk.Label(NewMmiowindow, text = "MMIO address")
    WriteButton = tk.Button(NewMmiowindow, text = "Write",command=lambda : CalculateMMIO(MmioAddr,MmioData))

    MmioHead.pack()
    WriteButton.pack()


def CreateIO():
    NewIowindow=tk.Toplevel(window)

def CreatePCI():
    NewPciwindow=tk.Toplevel(window)        

#Button behavior    

MMIO_button = tk.Button(MMIO_frame, text='MMIO address', fg='black', command=CreateMMIO)
MMIO_button.pack(side=tk.TOP)

IO_button = tk.Button(IO_frame, text='IO address', fg='black', command=CreateIO)
IO_button.pack(side=tk.TOP)

PCI_button = tk.Button(PCI_frame, text='List PCI Devices', fg='black', command=CreatePCI)
PCI_button.pack(side=tk.TOP)

window.mainloop()
