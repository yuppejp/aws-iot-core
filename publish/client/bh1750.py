import smbus

class Bh1750():
    def get_lux():
        bus = smbus.SMBus(1)
        addr = 0x23
        luxRead = bus.read_i2c_block_data(addr, 0x11)
        lux = luxRead[1] * 10
        return lux

if __name__ == '__main__':
    lux = Bh1750.get_lux()
    print("Lux: "+str(lux))
