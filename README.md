# micropython-sht31
This repository contains a MicroPython "driver" implementationforo the SHT31
temperature and humidity sensor from Sensirion.

Currently only a reasonably small subset of the features the sensor is
implemented.

## Implemented
* Read the temperature and humidity at different "repeatability" (accuracy)
settings. With celsius and fahrenheit values.
* Only single shot data acquisition mode

## Not yet implemented
* Continous (periodic) temperature acquisition and the corresponding
break/stop command
* CRC check of the sensor readings
* Temperature alerts
* Resetting the sensor (nRESET pin)

## Example code:
```
from machine import Pin, I2C
import sht31

i2c = I2C(scl=Pin(5), sda=Pin(4), freq =400000)
sensor = sht31.SHT31(i2c, addr=0x44)

sensor.get_temp_humi()
```
