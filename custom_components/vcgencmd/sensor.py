"""VideoCore vcgencmd sensor integration."""
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from subprocess import Popen, PIPE


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ARMTempSensor(), ARMFreqSensor(), ARMVoltsSensor()])


class ARMVoltsSensor(Entity):
    """SoC voltage Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'ARM voltage'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "V"

    def update(self):
        """Fetch new state data for the sensor."""
        proc = Popen(["vcgencmd", "measure_volts"], stdout=PIPE, stderr=PIPE)
        res = proc.communicate()[0]
        self._state = float(res[5:-2])

class ARMFreqSensor(Entity):
    """SoC frequency Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'ARM frequency'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "MHz"

    def update(self):
        """Fetch new state data for the sensor."""
        proc = Popen(["vcgencmd", "measure_clock", "arm"], stdout=PIPE, stderr=PIPE)
        res = proc.communicate()[0]
        self._state = int(res[14:-1])/1000000

class ARMTempSensor(Entity):
    """SoC temperature Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'ARM temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor."""
        proc = Popen(["vcgencmd", "measure_temp"], stdout=PIPE, stderr=PIPE)
        res = proc.communicate()[0]
        self._state = float(res[5:-3])
