import time
import usb.core
import usb.util

PID = 0xea60
VID = 0x10c4

dev = usb.core.find(idVendor=VID, idProduct=PID)
if not dev:
        print("CP2104 was not found :(")
        exit(1)
print ("Yeeha! Found CP2104")

SET_REQUEST = 0x41
bReq = 0xFF
mhsReq = 0x07
wVal = 0x37E1

def writeMhs(value):
        wVal = 0xff00 | value
        dev.ctrl_transfer(SET_REQUEST, mhsReq, wVal, 0, [])

def writeGpio(value):
        print(value)
        wIndex = value << 8 | 0x00ff
        dev.ctrl_transfer(SET_REQUEST, bReq, wVal, wIndex, [])

def buildGpio(ledOn, enabled, driver):
        value = 0
        mhsValue = 0b11

        if  not ledOn:
                value = value | (1 << 2)
                mhsValue = mhsValue & ~(1)

        if not enabled:
                value = value | (1 << 1)
                mhsValue = mhsValue & ~(1 << 1)

        if not driver:
                value = value | (1 << 0)
                value =  value | (1 << 3)

        writeGpio(value)
        writeMhs(mhsValue)

buildGpio(True, False, True)