# Objects
## Device
An abstract class to be implemented by the user for each type of device that needs to be connected. The class needs to
implement the following methods:
```
get_controllers(self) -> List[Actuator]
get_detectors(self) -> List[Detector]
```
These should return a list of instances of the `Actuator` and `Detector` classes for each controller and detector 
connected to the device. For details on the `Actuator` and `Detector` classes please see the respective headers below.

In addition, the derived `Device` class needs to implement a `connect`, `disconnect` and `is_connected` method:
```
connect(self) -> bool
disconnect(self) -> bool
is_connected(self) -> bool
```
For a detailed description of the class, see the documentation.

## Detector
An abstract class to be implemented by the user for each part of a device that returns data to the measurement, i.e. 
that can receive a "get" command.
The data can be of any dimension, from a sensor giving a single 0-dimensional value, a spectrometer giving a 
1-dimensional spectrum, an area detector or camera giving a 2-dimensional image.

## Actuator
An abstract class to be implemented by the user for each part of a device that can be actuated, i.e. that can receive
a "set" command.
