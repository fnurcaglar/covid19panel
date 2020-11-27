from avoserial import *
import threading
print(findPort("USB"))
initAvoSerial("COM21", 57600)
#read thread
def read():
    while True:
        data = readData()
        print(data)
#write thread
def write():
    while True:
        if input() == '1':
            startMeasure()
        if input() == '2':
            startMeasureBy(2000)
        if input() == '3':
            startMeasureBy(50)
            
tread = threading.Thread(target=read)
twrite = threading.Thread(target=write)
tread.start()
twrite.start()
#closeAvoSerial()