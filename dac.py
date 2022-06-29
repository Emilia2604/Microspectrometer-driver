import time
import smbus


bus=smbus.SMBus(1)

#ADR_MCP3424=0x63

def MCP4726(Vout):
    data1=(Vout>>4)
    data2=((Vout&15)<<4)
    data0=[data1,data2]
    print('Vout= ',Vout)
    bus.write_i2c_block_data(0x63,0x40,data0)
    

    