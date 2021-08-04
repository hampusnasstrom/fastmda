# Objects
## Device
An abstract class to be implemented by the user for each type of device that needs to be connected. The class needs to
implement the following methods:
```
get_controllers(self) -> List[Controller]
get_detectors(self) -> List[Detector]
```
These should return a list of instances of the `Controller` and `Detector` classes for each controller and detector 
connected to the device.

In addition the derived `Device` class needs to implement a connect and disconnect method.
### Detector

### Controller
