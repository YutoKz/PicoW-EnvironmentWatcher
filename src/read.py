import machine
from machine import Pin, UART

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / 65535

mhz19c = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))


def read_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature

def read_co2_level():
    # CO2濃度を読み取るコード
    data = bytearray([0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    mhz19c.write(data)
    mhz19c.readinto(data,len(data))
    co2 = data[2] * 256 + data[3]
    temp = data[4] - 48
    return co2

def read_mhz19c():
    # mhz19cを読み取る
    data = bytearray([0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    mhz19c.write(data)
    mhz19c.readinto(data,len(data))
    co2 = data[2] * 256 + data[3]
    temp = data[4] - 48
    print("temp:"+str(temp)+", co2: "+str(co2))
    return temp, co2
