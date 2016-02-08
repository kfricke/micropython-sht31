from machine import I2C

R_HIGH   = const(1)
R_MEDIUM = const(2)
R_LOW    = const(3)

class SHT31(object):
    """
    This class implements an interface to the SHT31 temprature and humidity
    sensor from Sensirion.
    """

    # This static map helps keeping the heap and program logic cleaner
    _map_cs_r = {
    	True: {
            R_HIGH : b'\x2c\x06',
            R_MEDIUM : b'\x2c\x0d',
            R_LOW: b'\x2c\x10'
            },
        False: {
            R_HIGH : b'\x24\x00',
            R_MEDIUM : b'\x24\x0b',
            R_LOW: b'\x24\x16'
            }
        }

    def __init__(self, i2c, addr=0x44):
        """
        Initialize a sensor object on the given I2C bus and accessed by the
        given address.
        """
        if i2c == None or i2c.__class__ != I2C:
            raise Exception('I2C object needed as argument!')
        self._i2c = i2c
        self._addr = addr

    def _send(self, buf):
        """
        Sends the given bufer object over I2C to the sensor.
        """
        self._i2c.send(buf, self._addr)

    def _recv(self, n=2):
        """
        Read bytes from the sensor using I2C. The byte count can be specified
        as an argument. Default is to receive two bytes.
        Returns a bytearray for the result.
        """
        return self._i2c.recv(n, self._addr)

    def _read_raw(self, r=R_HIGH, cs=True):
        """
        Read the raw temperature and humidity from the sensor and skips CRC
        checking.
        Returns a tuple for both values in that order.
        """
        if r not in (R_HIGH, R_MEDIUM, R_LOW):
            raise Exception('Wrong repeatabillity value given!')
        self._send(self._map_cs_r[cs][r])
        raw = self._recv(6)
        return (raw[0] << 8) + raw[1], (raw[3] << 8) + raw[4]

    def read_c(self, r=R_HIGH, cs=True):
        """
        Read the temperature in degree celsius and relative humidity.
        Returns a tuple for both values in that order.
        """
        t, h = self._read_raw(r, cs)
        return -45 + (175 * (t / 65535)), 100 * (h / 65535)

    def read_f(self, r=R_HIGH, cs=True):
        """
        Read the temperature in degree fahrenheit and relative humidity.
        Returns a tuple for both values in that order.
        """
        t, h = self._read_raw(r, cs)
        return -49 + (315 * (t / 65535)), 100 * (h / 65535)
