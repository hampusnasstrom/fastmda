from fastmda.schemas import DeviceInfo

device_info = {
    1: DeviceInfo(
        name="Some device",
        script='example_device.py',
        args={
            "com_port": "COM1"
        }
    )
}
device_dict = {}