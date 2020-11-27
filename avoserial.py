import serial
import serial.tools.list_ports
import binascii
import time
import io
from datetime import datetime
time = 1
sample = 100
ser = 0

def initAvoSerial (name,baudrate):
    global ser
    ser = serial.Serial(name, baudrate)
    ser.flush()

def closeAvoSerial ():
    global ser
    ser.close()

def findPort(msp_or_ftdi):
    # Find first available EiBotBoard by searching USB ports.
    # Return serial port object.
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        return None
    if comports:
        com_ports_list = list(comports())
        ebb_port = None
        for port in com_ports_list:
            if port[1].startswith(msp_or_ftdi): # Burayi istedigimiz gibi degisebiliriz.
                ebb_port = port[0]  # Success; EBB found by name match.
                break  # Stop searching-- we are done.
        if ebb_port is None:
            for port in com_ports_list:
                if port[2].startswith("USB VID:PID=0451:F432"):
                    ebb_port = port[0]  # Success; EBB found by VID/PID match.
                    break  # stop searching-- we are done.
        return ebb_port
 
def debugPrint (inout,str):
    if (inout == 1):
        print("<<<")
    else:
        print("<<<")
    print(str)

def startMeasure ():
    sendMessage("START")

def startMeasureBy (*args):
    global time,sample
    if args:
        time= args[0]
        sendMessage("START,"+ str(format(time,'04d')))#TODO:Blog
    else:   
        sendMessage("START")

def sendMessage (str):
    message = bytes() 
    message += bytes(str,'utf-8')
    message +=bytes("\n",'utf-8')
    ser.write(message)
    debugPrint(1,message)

def readHeader ():
    message = bytes()
    message = ser.read_until(b'\n')
    debugPrint(0,message)

#read one sample data from device
def readData ():
    dt = datetime.now()
    message = bytes()
    message = ser.read_until(b'\n')
    gelen = str(message)[2:][:len(message)-2]
    if (gelen =="RESTARTED"): 
        message = ser.read_until(b'\n')
        gelen = str(message)[2:][:len(message)-2]
    if (gelen =='STARTED'): 
        returning_data = gelen   
    else:
        returning_data = dt.strftime('%H:%M:%S.%f') +"," + gelen
    return returning_data
