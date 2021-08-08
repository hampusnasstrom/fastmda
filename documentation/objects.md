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

## Measurement
An abstract class to be implemented by the user for custom measurements. 
The standard measurements like mapping over actuators also inherit from this class.
