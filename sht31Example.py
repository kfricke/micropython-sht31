from machine import Pin, I2C
import sht31
i2c = I2C(scl=Pin(5), sda=Pin(4), freq =400000)
sensor = sht31.SHT31(i2c, addr=0x44)
sensor.get_temp_humi()