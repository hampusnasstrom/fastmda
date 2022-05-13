# FastMDA Objects
The FastMDA can be run with already implemented devices and measurements. However, there are a set of base objects that
allows the user to implement new devices (detectors, motors, sensors, etc.) and custom measurements (run directly on the 
server side). 

All devices that are in charge of communicating need to be implemented by inheriting the `Device` super 
class. The detector(s) and actuator(s) controlled by this device is then retrieved through the `Device` object. The 
part of the device that you can _get_ data from is implemented by inheriting the `Detector` super class whilst the part 
of the device that you can _set_ the position of is implemented by inheriting the `Actuator` super class. 
One device will typically only have one detector or actuator but can in principle have any number of both of them.

Measurements can of course be implemented on the user side by sending the necessary commands to the relevant detectors 
and actuators. However, implementing the measurement directly on the server side has a number of advantages. 
One of the reasons is to decouple the measurement from the user interface and make sure that it keeps running in case of
any errors in the UI. A set of standard measurements such as time series and maps over actuators are already implemented
but the user can inherit from the `Measurement` class and implement their own if needed.

## Device
An abstract class to be implemented by the user for each type of device that needs to be connected. The class needs to
implement the `self.objects` attribute of the data type `fastmda.objects.DeviceObjects` with attributes:
```
actuators: Dict[int, Union[DiscreteActuator, ContinuousActuator]]
detectors: Dict[int, Detector]
```
For details on the `DiscreteActuator`, `ContinuousActuator` and `Detector` classes please see the respective headers 
below.

In addition, the derived `Device` class needs to implement a `connect`, `disconnect` and `is_connected` method:
```
connect(self) -> int
disconnect(self) -> int
is_connected(self) -> bool
```
<!--- connect and disconnect should be int so that they can return a code that explains why the connect didn't work -->
<!--- How about a "identify(self) -\> string" function, that returns some sort of identifier (name, serial number, ...)
 -->
<!--- How do you handle a device like this: A detector, that has a filter, that can be replaced manually? You would want
 to store the information about which filter is in somewhere. Maybe you would also want to take measurements dependent
  on which filter is in and maybe even ask the user at some point to change the filter now -->

For a detailed description of the class, see the documentation.

## Detector
An abstract class to be implemented by the user for each part of a device that returns data to the measurement, i.e. 
that can receive a "get" command.
The data can be of any dimension, from a sensor giving a single 0-dimensional value, a spectrometer giving a 
1-dimensional spectrum, an area detector or camera giving a 2-dimensional image.

## Actuator
An abstract class to be implemented by the user for each part of a device that can be actuated, i.e. that can receive
a "set" command.
### DiscreteActuator
An actuator with a discrete number of positions. Should implement to following functions:
```doctest
def get_position_values(self) -> List[str]:
    """
    Get a list of all the options as strings, should be overridden in subclass.

    :return: list of all the options as strings.
    :rtype: List[str]
    """

def get_position(self) -> int:
    """
    Get the index of the current position, should be overridden in subclass.

    :return: Index of current position.
    :rtype: int
    """

def _set_position(self, position_index: int):
    """
    Private method for setting the position of the actuator, should be overridden in subclass.

    :param position_index: Index of the position to set.
    :type position_index: int
    :return: None
    :rtype: None
    """
```
### ContinuousActuator
An actuator which can be set to a continuous position. Should implement to following functions:
```doctest
def get_position(self) -> float:
    """
    Method for getting the position of the actuator, should be overridden in subclass.

    :return: The position of the actuator.
    :rtype: float
    """

def get_hardware_limits(self) -> Tuple[float, float]:
    """
    Method for getting the hardware limits of the actuator, should be overridden in subclass.

    :return: A tuple of the (lower, upper) limit of the actuator.
    :rtype: Tuple[float, float]
    """

def _set_position(self, position: float):
    """
    Private method for setting the position of the actuator, should be overridden in subclass.

    :param position: Position to set the actuator to.
    :type position: float
    :return: None
    :rtype: None
    """
```

## Measurement
An abstract class to be implemented by the user for custom measurements. The class contains a sequence of operations 
performed by the `Actuators` and `Detectors`. The class needs to implement the following methods:
```

```
The standard measurements like mapping over actuators also inherit from this class.
